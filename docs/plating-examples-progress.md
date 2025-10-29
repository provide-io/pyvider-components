# Plating Example Fix Progress

## Work Completed
- Resolved variable collisions across Terraform/OpenTofu example files and rebuilt the generated examples from updated `.plating` sources.

## Phase 1: Initial Analysis & Lens JQ Fix
- Identified duplicate local variable names across 15+ example directories.
- Fully remediated the `lens_jq` example set by adding file-specific prefixes (`basic_`, `adv_`, `comp_`, `lens_`), converting JQ strings to double-quoted formats, and updating all references.
- Verified `lens_jq` with `tofu init && tofu plan`.

## Phase 2: Updates to .plating Templates
- Edited templates under `src/pyvider/components/functions/collection_functions.plating/examples/`, `numeric_functions.plating/examples/`, `string_manipulation.plating/examples/`, and `type_conversion_functions.plating/examples/`.
- Applied automated prefixing to handle variable collisions and regenerated 115 example files.

## Current Status
- ✅ Passing (7/25): `add`, `format_size`, `lens_jq`, `pluralize`, `subtract`, `tostring`, `truncate`.
- ❌ Failing (18/25): `contains`, `divide`, `format`, `join`, `length`, `lookup`, `lower`, `max`, `min`, `multiply`, `replace`, `round`, `split`, `sum`, `to_camel_case`, `to_kebab_case`, `to_snake_case`, `upper`.

## Root Causes of Remaining Failures
1. Prefix automation cannot distinguish between dictionary keys (should not change) and local declarations (must change).
2. Complex, multi-line JQ expressions require manual quote and escape handling.

## Next Steps
1. For each failing example directory, manually adjust the matching `.plating` source:
   - Prefixed variables inside `locals {}` only.
   - Normalize JQ filter strings to double quotes.
   - Update references, regenerate examples, and validate with `tofu init && tofu plan`.
2. Target templates located in `src/pyvider/components/functions/*/examples/`.

## Recommendations
1. Implement smarter prefixing logic with Terraform-aware parsing.
2. Add a validation script to detect duplicate variable names across generated examples.
3. Gate CI on the validation script to prevent regressions.
4. Document example naming conventions (e.g., function-specific prefixes) for future contributors.
