help: ## help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## install development requirements
	pip install -r requirements_dev.txt

install-localdev:  ## install library for local development; pip install -e .
	flit install --symlink

test: ## run tests
	pytest $(args)

test-cov: ## run tests with coverage
	pytest --cov finite_state_machine/ --cov examples/

test-covhtml: ## run tests with coverage; view in browser
	pytest --cov finite_state_machine/ --cov examples/ --cov-report html && open ./htmlcov/index.html

changelog:  ## generate changelog v=""
	python ./scripts/generate_changelog.py --version=$(v)
