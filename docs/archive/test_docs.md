# Testing Terraform Provider Documentation Locally

## Option 1: Using terraform-plugin-docs (Official HashiCorp Tool)

### Install
```bash
# Install via Go
go install github.com/hashicorp/terraform-plugin-docs/cmd/tfplugindocs@latest

# Or download binary from releases
# https://github.com/hashicorp/terraform-plugin-docs/releases
```

### Validate Documentation
```bash
cd /REDACTED_ABS_PATH

# Validate all documentation files
tfplugindocs validate

# Check specific categories
tfplugindocs validate --allowed-resource-subcategories "Utilities,Lens,Test Mode"
```

### Generate Preview
```bash
# Generate documentation (creates docs/ directory)
tfplugindocs generate

# The tool will show any issues with:
# - Missing frontmatter fields
# - Invalid subcategory values
# - Incorrect file structure
```

## Option 2: Use MkDocs to Preview (If Available)

Check if pyvider-components has mkdocs configured:
```bash
ls mkdocs.yml
```

If yes:
```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Serve documentation locally at http://127.0.0.1:8000
mkdocs serve

# Build static site
mkdocs build
```

## Option 3: Manual Verification (What We'll Do Now)

### Check All Subcategories
```bash
# Verify all files have subcategories
grep -r "subcategory:" docs/ | sort

# Count by category
grep -r "subcategory:" docs/ | cut -d'"' -f2 | sort | uniq -c

# Verify specific files
head -10 docs/data-sources/lens_jq.md
head -10 docs/resources/private_state_verifier.md
```

### Check Frontmatter Structure
```bash
# Ensure all files have proper frontmatter
for file in docs/data-sources/*.md docs/resources/*.md docs/functions/*.md; do
  if ! head -1 "$file" | grep -q "^---$"; then
    echo "Missing frontmatter: $file"
  fi
done
```

## Option 4: Preview in Browser (Simple HTML)

Create a simple index.html to browse the documentation structure:
```bash
cd /REDACTED_ABS_PATH

# Generate a simple HTML preview
cat > docs/preview.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
  <title>Pyvider Provider Documentation Preview</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    .category { margin: 20px 0; }
    .category h2 { color: #333; }
    .subcategory { margin-left: 20px; }
    .subcategory h3 { color: #666; }
    ul { list-style: none; }
    li { margin: 5px 0; }
    a { color: #0366d6; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Pyvider Provider Documentation</h1>
  
  <div class="category">
    <h2>Resources</h2>
    <div class="subcategory">
      <h3>Test Mode</h3>
      <ul>
        <li><a href="resources/private_state_verifier.md">pyvider_private_state_verifier</a></li>
      </ul>
    </div>
    <div class="subcategory">
      <h3>Utilities</h3>
      <ul>
        <li><a href="resources/file_content.md">pyvider_file_content</a></li>
        <li><a href="resources/local_directory.md">pyvider_local_directory</a></li>
      </ul>
    </div>
  </div>
  
  <div class="category">
    <h2>Data Sources</h2>
    <div class="subcategory">
      <h3>Lens</h3>
      <ul>
        <li><a href="data-sources/lens_jq.md">pyvider_lens_jq</a></li>
      </ul>
    </div>
    <div class="subcategory">
      <h3>Test Mode</h3>
      <ul>
        <li><a href="data-sources/mixed_map_test.md">pyvider_mixed_map_test</a></li>
        <li><a href="data-sources/simple_map_test.md">pyvider_simple_map_test</a></li>
      </ul>
    </div>
    <div class="subcategory">
      <h3>Utilities</h3>
      <ul>
        <li><a href="data-sources/env_variables.md">pyvider_env_variables</a></li>
        <li><a href="data-sources/file_info.md">pyvider_file_info</a></li>
      </ul>
    </div>
  </div>
</body>
</html>
HTML

open docs/preview.html
```

