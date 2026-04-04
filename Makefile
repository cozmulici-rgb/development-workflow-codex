PYTHON ?= python3

.PHONY: validate package boundary-check boundary-generate

validate:
	$(PYTHON) scripts/validate_repo.py

package:
	$(PYTHON) scripts/package_plugin.py

boundary-check:
	@if [ -z "$(POLICY)" ]; then echo "POLICY is required"; exit 2; fi
	$(PYTHON) scripts/write_boundary_guard.py verify --policy "$(POLICY)"

boundary-generate:
	@if [ -z "$(PLAN_DIR)" ]; then echo "PLAN_DIR is required"; exit 2; fi
	$(PYTHON) scripts/generate_boundary_policy.py "$(PLAN_DIR)"
