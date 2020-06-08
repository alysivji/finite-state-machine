install:
	pip install -r requirements_dev.txt

test:
	pytest

test-cov:
	pytest --cov simple_state_machine/ --cov examples/

test-covhtml:
	pytest --cov simple_state_machine/ --cov examples/ --cov-report html && open ./htmlcov/index.html
