# Investigation: 3 Failing Private State Tests

## Summary

3 tests in pyvider-components were failing due to a **bug in pyvider-cty** that incorrectly marked entire CtyObjects as `is_unknown=True` when they contain any unknown fields.

**Status**: ✅ RESOLVED - Fix was already in place, needed editable install
**Root Cause**: `CtyObject.validate()` wasn't explicitly setting `is_unknown=False` at object level
**Fix Location**: pyvider-cty/src/pyvider/cty/types/structural/object.py:154
**Impact**: Resources with computed fields that use `a_unknown()` during plan phase
**Severity**: Medium - Limited to specific use case (plan→apply with computed fields)

**Resolution Date**: 2025-10-25
**All 3 tests now passing**: ✅
**Regression tests added**: 4 new tests in pyvider-cty ✅
**updateem script fixed**: Now uses editable installs ✅

## Failing Tests

1. `tests/resources/test_comprehensive_private_state_suite.py::TestPrivateStateResourceLifecycle::test_private_state_verifier_resource_works`
2. `tests/resources/test_comprehensive_private_state_suite.py::TestTimedTokenResource::test_timed_token_lifecycle`
3. `tests/test_e2e_encryption_lifecycle.py::test_private_state_verifier_lifecycle`

**Common Pattern**: All 3 tests use resources with private state and computed fields marked as unknown during plan phase.

## Root Cause Analysis

### The Bug

When a CtyObject contains mixed known/unknown fields (e.g., known config values + unknown computed fields), the marshal/unmarshal cycle incorrectly marks the **entire object** as `is_unknown=True`.

### Evidence

```python
# Before marshal/unmarshal (from plan phase)
Object: is_unknown=False
  ├─ input_value: is_unknown=False, value="test-verification"  ✅
  └─ decrypted_token: is_unknown=True, value=UNREFINED_UNKNOWN  ✅

# After marshal/unmarshal (in apply phase)
Object: is_unknown=True  ← ❌ BUG! Should be False
  ├─ input_value: is_unknown=False, value="test-verification"  ✅
  └─ decrypted_token: is_unknown=True, value=UNREFINED_UNKNOWN  ✅
```

### Impact Chain

1. **Plan Phase**: Resource creates planned_state with known + unknown fields
   ```python
   base_plan["decrypted_token"] = a_unknown(a_str())  # Mark as unknown
   ```

2. **Marshal**: `PlanResourceChangeHandler` marshals planned_state to msgpack
   - Individual fields maintain their unknown status ✅
   - But something in msgpack encoding loses object-level known status ❌

3. **Unmarshal**: `ApplyResourceChangeHandler` unmarshals planned_state
   - CtyObject now has `is_unknown=True` at object level ❌
   - Fields still have correct known/unknown status ✅

4. **Conversion**: `BaseResource._handle_cty_value()` checks object
   ```python
   if cty_value.is_unknown and not isinstance(cty_value.type, CtyObject | ...):
       return None
   ```
   - CtyObject passes the type check, so falls through
   - But later conversion still treats it as unknown and returns None

5. **Operation Detection**: `BaseResource.apply()` checks planned_state
   ```python
   is_create = ctx.state is None  # ✅ True (no prior state)
   is_delete = ctx.planned_state is None  # ❌ True (should be False!)
   ```
   - `ctx.planned_state is None` → DELETE detected
   - Should be CREATE, not DELETE

6. **Test Failure**: Apply returns empty state for DELETE
   ```python
   final_state = unmarshal(apply_response.new_state, schema=schema.block)
   assert final_state.value["input_value"]  # TypeError: None has no subscript
   ```

## Code Locations

### Bug Location
**File**: Likely in `pyvider/src/pyvider/cty/codec.py` or msgpack encoding/decoding
**Issue**: When serializing CtyObject with unknown fields, incorrectly sets object-level unknown flag

### Symptom Location
**File**: `pyvider/src/pyvider/resources/base.py:45-50`
```python
@classmethod
def _handle_cty_value(cls, cty_value: CtyValue, target_cls: type) -> Any | None:
    if cty_value.is_null:
        return None
    if cty_value.is_unknown and not isinstance(cty_value.type, CtyObject | CtyList | CtySet | CtyTuple):
        return None
    return cls._cty_to_attrs_recursive(cty_value.value, target_cls)
```

**Current Logic**:
- Returns None for unknown primitives ✅
- Passes through unknown objects to recursive processing ✅
- But downstream conversion still fails for unknown objects ❌

### Affected Resources
**File**: `pyvider-components/src/pyvider/components/resources/private_state_verifier.py`
**Pattern**:
```python
async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]) -> tuple[dict[str, Any], PrivateState]:
    base_plan["decrypted_token"] = a_unknown(a_str())  # ← Creates unknown field
    private_state = VerifierPrivateState(secret_token=f"SECRET_FOR_{...}")
    return base_plan, private_state
```

## Proposed Solutions

### Option 1: Fix Marshal/Unmarshal (Recommended)
**Location**: `pyvider/src/pyvider/cty/codec.py` (or wherever msgpack encoding happens)
**Change**: Preserve object-level `is_unknown=False` when only individual fields are unknown

**Pros**:
- Fixes root cause
- Correct behavior for all use cases
- Aligns with Terraform's type system semantics

**Cons**:
- Requires understanding msgpack encoding internals
- May affect other code paths
- Needs extensive testing

### Option 2: Workaround in _handle_cty_value
**Location**: `pyvider/src/pyvider/resources/base.py:45`
**Change**: Check if unknown CtyObject has field data (dict) and process it
```python
if cty_value.is_unknown:
    if isinstance(cty_value.type, CtyObject) and isinstance(cty_value.value, dict):
        # Object structure is known, only fields are unknown - process normally
        return cls._cty_to_attrs_recursive(cty_value.value, target_cls)
    if not isinstance(cty_value.type, CtyObject | CtyList | CtySet | CtyTuple):
        return None
```

**Pros**:
- Simple, localized change
- Low risk
- Doesn't require understanding msgpack internals

**Cons**:
- Workaround, not a true fix
- May hide other issues
- Doesn't fix the root cause

### Option 3: Change Resource Pattern
**Location**: Resource implementations
**Change**: Don't use `a_unknown()` for computed fields during plan
```python
async def _create(self, ctx: ResourceContext, base_plan: dict[str, Any]):
    # Don't set computed fields in plan phase
    # base_plan["decrypted_token"] = a_unknown(a_str())  # Remove this
    private_state = VerifierPrivateState(secret_token=f"SECRET_FOR_{...}")
    return base_plan, private_state

async def _create_apply(self, ctx: ResourceContext) -> tuple[VerifierState, None]:
    # Set computed values during apply phase
    final_state = VerifierState(
        input_value=ctx.config.input_value,
        decrypted_token=ctx.private_state.secret_token  # Set here instead
    )
    return final_state, None
```

**Pros**:
- Avoids triggering the bug
- May be the "correct" pattern anyway

**Cons**:
- Requires changing resource implementations
- Doesn't fix the underlying bug
- May not work for all computed field scenarios

## Testing the Bug

Reproduce with:
```python
python3 << 'EOF'
from pyvider.cty import CtyValue, CtyString, CtyObject
from pyvider.conversion import marshal, unmarshal
from pyvider.schema import s_resource, a_str

schema = s_resource({
    "input_value": a_str(required=True),
    "decrypted_token": a_str(computed=True)
})

# Create object with mixed known/unknown fields
obj_value = {
    "input_value": CtyValue(vtype=CtyString(), value="test-value"),
    "decrypted_token": CtyValue(vtype=CtyString(), value=CtyValue.unknown(CtyString()).value, is_unknown=True)
}
cty_val = CtyValue(vtype=schema.block.to_cty_type(), value=obj_value)

print(f"Before marshal: is_unknown={cty_val.is_unknown}")  # False ✅

marshaled = marshal(cty_val, schema=schema.block)
unmarshaled = unmarshal(marshaled, schema=schema.block)

print(f"After unmarshal: is_unknown={unmarshaled.is_unknown}")  # True ❌
EOF
```

**Expected**: `After unmarshal: is_unknown=False`
**Actual**: `After unmarshal: is_unknown=True`

## Debug Logging Added

For investigation, added debug logging in:

**File**: `pyvider/src/pyvider/protocols/tfprotov6/handlers/apply_resource_change.py:161-178`
```python
logger.debug(
    "Converting planned_state to attrs instance",
    operation="create_resource_context",
    planned_state_cty_is_none=planned_state_cty is None,
    is_unknown=planned_state_cty.is_unknown if hasattr(planned_state_cty, 'is_unknown') else None,
)
logger.debug(
    "Planned state converted",
    operation="create_resource_context",
    planned_state_instance_is_none=planned_state_instance is None,
)
```

**Purpose**: Shows when planned_state CtyValue is unknown and conversion returns None

**Remove after fix**: These debug logs can be removed once issue is resolved

## ✅ Resolution

**The fix was already present in pyvider-cty** at line 154 of `src/pyvider/cty/types/structural/object.py`:

```python
# Don't mark the entire object as unknown just because some fields are unknown
# Terraform expects field-level unknown tracking, not object-level
# The object itself is only unknown if explicitly passed as unknown
return CtyValue(vtype=self, value=validated_attrs, is_unknown=False)
```

**The issue was that pyvider-cty was not installed in editable mode**, so the fix wasn't being used.

### Steps Taken

1. **Installed pyvider-cty in editable mode**: `uv pip install -e pyvider-cty`
2. **Verified all 3 tests pass**: All tests now pass with the fix active ✅
3. **Removed investigation debug logging** from `apply_resource_change.py` ✅
4. **Added trace logging** in `resources/base.py` for future debugging (minimal performance impact) ✅
5. **Added regression tests** in `pyvider-cty/tests/object/test_object_unknown_fields.py` (4 tests) ✅
6. **Fixed updateem script** to use `-e` and proper relative paths for all local packages ✅

### Regression Tests Added

Created `pyvider-cty/tests/object/test_object_unknown_fields.py` with comprehensive coverage:

- **test_object_with_unknown_field_is_not_unknown** - Validates object-level is_unknown is False when object contains unknown fields
- **test_object_unknown_fields_marshal_unmarshal** - Tests marshal/unmarshal cycle preserves correct status (simulates Terraform plan→apply)
- **test_object_all_fields_unknown** - Ensures object with all unknown fields still has is_unknown=False at object level
- **test_explicitly_unknown_object** - Verifies explicitly unknown CtyValue objects remain unknown

All 4 regression tests pass ✅

### updateem Script Fix

The `updateem` script was installing packages from built artifacts instead of editable mode. Fixed to:
- Use proper bash script format with shebang
- Change to script directory before running
- Use relative paths (`./pyvider` instead of `pyvider`)
- Install all packages with `-e` flag for editable mode

This ensures all local development packages are always installed in editable mode, so changes take effect immediately.

### What Was NOT Needed

- ❌ No workaround needed in `_handle_cty_value`
- ❌ No changes to resource implementations
- ❌ No changes to msgpack encoding/decoding

The bug was simply that CtyObject.validate() wasn't explicitly setting `is_unknown=False`, which is now fixed.

## Files Changed During Resolution

### pyvider (framework)
- `src/pyvider/protocols/tfprotov6/handlers/apply_resource_change.py` - Debug logging added then removed ✅
- `src/pyvider/resources/base.py` - Added trace logging in `_handle_cty_value()` for future debugging ✅

### pyvider-cty (core library)
- `src/pyvider/cty/types/structural/object.py:154` - Fix already present (explicit `is_unknown=False`) ✅
- `tests/object/test_object_unknown_fields.py` - **NEW** - Regression tests (4 tests) ✅

### pyvider-components
- `FAILING_TESTS_INVESTIGATION.md` - Updated with resolution ✅

### Infrastructure
- `/Users/tim/code/gh/provide-io/updateem` - Fixed to install all packages in editable mode ✅

## Additional Notes

### Not Related To
- Multi-provider refactoring (completed successfully)
- Missing `prior_state` in test requests (protobuf defaults work correctly)
- Provider registration or discovery issues

### Related Terraform Behavior
Terraform's type system allows objects to be "known" while containing unknown fields. This is normal during planning:
- Object structure: Known
- Some field values: Known
- Other field values: Unknown (computed during apply)

The pyvider marshal/unmarshal should preserve this semantic correctly.

---

## Quick Reference

### For Developers

If you encounter similar "planned_state is None" or "operation_type=delete instead of create" issues:

1. **Check if object contains unknown fields** - Look for resources using `a_unknown()` in plan phase
2. **Verify pyvider-cty is installed in editable mode** - Run `uv pip show pyvider-cty` and check for "editable_project_location"
3. **Use updateem script** - Always use `bash updateem` instead of manual `uv pip install` to ensure editable mode
4. **Run regression tests** - `pytest tests/object/test_object_unknown_fields.py` in pyvider-cty

### Key Learnings

- **Terraform's type system allows objects to be "known" while containing unknown fields** - This is normal during planning
- **Object-level is_unknown must be explicitly set to False** - Don't rely on default/inherited values
- **Editable installs are critical for local development** - Built packages won't reflect source code changes
- **Marshal/unmarshal cycles preserve field-level unknown status** - But object-level status must be correct before marshaling

---

**Date**: 2025-10-25
**Investigated By**: Claude Code
**Framework**: pyvider 0.1.0
**Components**: pyvider-components 0.1.0
