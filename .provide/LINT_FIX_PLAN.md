# Lint Fix Plan: pyvider-components

**Total Violations:** 35
**Generated:** 2025-11-16
**Priority:** MEDIUM (component library)

---

## Violation Summary

| Code | Count | Description | Auto-fixable |
|------|-------|-------------|--------------|
| ANN201 | 10 | Missing return type (public fn) | Manual |
| ANN001 | 7 | Missing type annotation | Manual |
| ANN206 | 5 | Missing return type (__exit__) | Manual |
| ANN204 | 3 | Missing return type (__init__) | Manual |
| C901 | 2 | Function too complex | Manual |
| B007 | 2 | Unused loop control variable | Manual |
| ANN202 | 2 | Missing return type (private fn) | Manual |
| SIM108 | 1 | Use ternary operator | Yes (unsafe) |
| RUF003 | 1 | Ambiguous comment character | Manual |
| ANN003 | 1 | Missing **kwargs annotation | Manual |
| ANN002 | 1 | Missing *args annotation | Manual |

---

## Files Requiring Fixes

### Root-Level Scripts (Consider archiving)
- `fix_variable_conflicts.py` - 14 violations (ANN001, ANN201, B007)

### Scripts Directory
- `scripts/build_docs_and_examples.py`
- `scripts/validate_docs.py`

### Source Code (src/pyvider/components/)
- `capabilities/api.py` - ANN206 (__exit__ return type)
- `capabilities/core.py` - ANN206 (__exit__ return type)
- `data_sources/env_variables.py`
- `data_sources/http_api.py`
- `data_sources/nested_data_test_suite.py`
- `functions/collection_functions.py`
- `functions/lens_jq.py`
- `functions/numeric_functions.py`
- `provider.py`

### Tests (13 violations)
- `tests/resources/test_comprehensive_private_state_suite/test_encryption.py`
- `tests/resources/test_tdd_private_state*.py`
- `tests/resources/test_tdd_resource_context_contract.py`

---

## Fix Strategy by Category

### Phase 1: Quick Wins

**Estimated time:** 5 minutes

```bash
cd /Users/tim/code/gh/provide-io/pyvider-components
ruff check --fix .
ruff check --fix --unsafe-fixes .
```

Auto-fixes:
- SIM108 (1) - Ternary operator

**Expected reduction:** ~1 violation (3%)

---

### Phase 2: Archive Root-Level Scripts

**Estimated time:** 5 minutes

`fix_variable_conflicts.py` has 14 violations and appears to be a utility script. Consider:

```bash
# Option A: Archive
mkdir -p .archive/utility-scripts
mv fix_variable_conflicts.py .archive/utility-scripts/

# Option B: Exclude from ruff
# Add to pyproject.toml:
# [tool.ruff]
# exclude = ["fix_variable_conflicts.py"]
```

**Immediate reduction:** 14 violations (40%)

---

### Phase 3: Type Annotations (ANN*)

**Location:** src/pyvider/components/
**Estimated time:** 30 minutes

**ANN206 - Missing __exit__ return type (5 occurrences):**
```python
# BEFORE
def __exit__(self, exc_type, exc_val, exc_tb):

# AFTER
from types import TracebackType
def __exit__(
    self,
    exc_type: type[BaseException] | None,
    exc_val: BaseException | None,
    exc_tb: TracebackType | None,
) -> bool | None:
```

**ANN204 - Missing __init__ return type (3 occurrences):**
```python
# BEFORE
def __init__(self, param):

# AFTER
def __init__(self, param: str) -> None:
```

**ANN201/ANN202 - Public/private function returns:**
```python
# BEFORE
def find_plating_examples():
def get_local_vars(content):

# AFTER
def find_plating_examples() -> list[Path]:
def get_local_vars(content: str) -> list[str]:
```

---

### Phase 4: Loop Variables (B007)

**Location:** `fix_variable_conflicts.py`
**Estimated time:** 5 minutes

```python
# BEFORE
for root, dirs, files in os.walk(SRC_DIR):

# AFTER
for root, _dirs, _files in os.walk(SRC_DIR):
```

---

### Phase 5: Complex Functions (C901)

**Estimated time:** 30-60 minutes
**2 violations**

Refactor functions exceeding complexity threshold. Extract helper functions to reduce branching.

---

### Phase 6: Ambiguous Comment (RUF003)

**Estimated time:** 2 minutes

```python
# BEFORE - Ambiguous Unicode in comment
# Some comment with 'fancy' quotes

# AFTER - Use standard ASCII quotes
# Some comment with 'standard' quotes
```

---

## Recommended Execution Order

1. **Archive/exclude root scripts** - 40% reduction immediately
2. **Run auto-fix** - Quick wins
3. **Add __exit__ type annotations** - Common pattern
4. **Add __init__ return types** - Simple fixes
5. **Fix remaining ANN issues** - Code quality
6. **Refactor C901** - Optional, time-intensive

---

## Commands

```bash
# Check current state
cd /Users/tim/code/gh/provide-io/pyvider-components
ruff check . 2>&1 | tail -10

# Archive problematic script
mkdir -p .archive/utility-scripts
mv fix_variable_conflicts.py .archive/utility-scripts/

# Auto-fix
ruff check --fix .

# Format
ruff format .

# Type check
mypy src/

# Verify
ruff check . 2>&1 | grep "Found"
```

---

## Alternative: Relax Rules

```toml
[tool.ruff.lint.per-file-ignores]
"fix_variable_conflicts.py" = ["ANN001", "ANN201", "B007"]
"scripts/**" = ["ANN001", "ANN201"]
"**/capabilities/*.py" = ["ANN206"]  # __exit__ annotations complex

[tool.ruff.lint]
ignore = [
    "ANN204",  # __init__ return type optional
    "C901",    # Allow complex functions
]
```

---

## Success Criteria

- [ ] Root-level utility scripts archived or excluded
- [ ] All __exit__ methods properly annotated
- [ ] All __init__ methods have -> None
- [ ] Public functions have return type annotations
- [ ] Loop variables prefixed with underscore
- [ ] Total violations: 0 or documented exceptions
