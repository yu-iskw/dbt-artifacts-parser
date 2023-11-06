# Set up an environment
.PHONY: setup
setup: setup-python setup-pre-commit

# Set up the python environment.
.PHONY: setup-python
setup-python:
	bash ./dev/setup.sh --deps "develop"

# Set up the pre-commit hooks.
.PHONY: setup-pre-commit
setup-pre-commit:
	pre-commit install

# Check all the coding style.
.PHONY: lint
lint: run-pre-commit lint-shell lint-python

# Run the pre-commit hooks.
.PHONY: run-pre-commit
run-pre-commit:
	pre-commit run --all-files

# Update the pre-commit hooks.
.PHONY: update-pre-commit
update-pre-commit:
	pre-commit autoupdate

# Check the coding style for the shell scripts.
.PHONY: lint-shell
lint-shell:
	shellcheck ./dev/*.sh

# Check the coding style for the python files.
.PHONY: lint-python
lint-python:
	bash ./dev/lint_python.sh

# Format source codes
.PHONY: format
format: format-python

# Format python codes
.PHONY: format-python
format-python:
	bash ./dev/format_python.sh

# Run the unit tests.
.PHONY: test
test:
	bash ./dev/test_python.sh

# Build the package
.PHONY: build
build: clean lint test
	flit build

# Clean the environment
.PHONY: clean
clean:
	bash ./dev/clean.sh

# Publish to pypi
.PHONY: publish
publish:
	bash ./dev/publish.sh "pypi"

# Publish to testpypi
.PHONY: test-publish
test-publish:
	bash ./dev/publish.sh "testpypi"
