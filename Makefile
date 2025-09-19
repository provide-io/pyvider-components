.PHONY: docs-clean docs-functions docs-resources docs-data-sources docs-all docs-serve docs-check

# Variables
DOCS_DIR = docs
PLATING_CMD = python -c "import sys; sys.path.append('../plating/src'); from plating.api import PlatingAPI; api = PlatingAPI()"

# Clean all documentation
docs-clean:
	@echo "🧹 Cleaning documentation directory..."
	rm -rf $(DOCS_DIR)/*
	mkdir -p $(DOCS_DIR)/functions $(DOCS_DIR)/resources $(DOCS_DIR)/data_sources
	@echo "✅ Documentation directory cleaned"

# Generate function documentation (individual files)
docs-functions: docs-clean
	@echo "📚 Generating function documentation..."
	@python3 -c "\
import sys; sys.path.append('../plating/src'); \
from plating.api import PlatingAPI; \
from pathlib import Path; \
api = PlatingAPI(); \
files = api.generate_function_documentation('$(DOCS_DIR)/functions'); \
written = api.write_generated_files(files); \
print(f'✅ Generated {len(written)} function documentation files')"

# Generate resource documentation
docs-resources:
	@echo "📦 Generating resource documentation..."
	@python3 -c "\
import sys; sys.path.append('../plating/src'); \
from plating.api import PlatingAPI; \
from pathlib import Path; \
api = PlatingAPI(); \
files = api.generate_resource_documentation('$(DOCS_DIR)/resources'); \
written = api.write_generated_files(files); \
print(f'✅ Generated {len(written)} resource documentation files')"

# Generate data source documentation
docs-data-sources:
	@echo "📊 Generating data source documentation..."
	@python3 -c "\
import sys; sys.path.append('../plating/src'); \
from plating.api import PlatingAPI; \
from pathlib import Path; \
api = PlatingAPI(); \
files = api.generate_resource_documentation('$(DOCS_DIR)/data_sources'); \
written = api.write_generated_files(files); \
print(f'✅ Generated {len(written)} data source documentation files')"

# Generate all documentation
docs-all: docs-functions docs-resources docs-data-sources
	@echo "🎉 All documentation generated successfully!"
	@echo "📁 Files generated:"
	@find $(DOCS_DIR) -name "*.md" | wc -l | xargs echo "   Total files:"
	@echo "📍 Location: $(PWD)/$(DOCS_DIR)"

# Check what documentation was generated
docs-check:
	@echo "📋 Documentation files generated:"
	@find $(DOCS_DIR) -name "*.md" | sort
	@echo ""
	@echo "📊 Summary:"
	@echo "  Functions: $$(find $(DOCS_DIR)/functions -name "*.md" 2>/dev/null | wc -l)"
	@echo "  Resources: $$(find $(DOCS_DIR)/resources -name "*.md" 2>/dev/null | wc -l)"
	@echo "  Data Sources: $$(find $(DOCS_DIR)/data_sources -name "*.md" 2>/dev/null | wc -l)"
	@echo "  Total: $$(find $(DOCS_DIR) -name "*.md" 2>/dev/null | wc -l)"

# Show sample content from generated docs
docs-sample:
	@echo "📖 Sample content from generated documentation:"
	@for file in $$(find $(DOCS_DIR) -name "*.md" | head -3); do \
		echo ""; \
		echo "=== $$file ==="; \
		head -15 "$$file"; \
		echo "..."; \
	done

# Help
help:
	@echo "📚 Pyvider Components Documentation Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  docs-clean       - Clean documentation directory"
	@echo "  docs-functions   - Generate function documentation"
	@echo "  docs-resources   - Generate resource documentation"
	@echo "  docs-data-sources- Generate data source documentation"
	@echo "  docs-all         - Generate all documentation"
	@echo "  docs-check       - Check what documentation was generated"
	@echo "  docs-sample      - Show sample content from generated docs"
	@echo "  help             - Show this help message"
	@echo ""
	@echo "Example usage:"
	@echo "  make docs-functions  # Generate individual function .md files"
	@echo "  make docs-all        # Generate everything"
	@echo "  make docs-check      # See what was generated"