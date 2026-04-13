# Set up an environment
.PHONY: setup
setup: setup-python setup-pre-commit

.PHONY: setup-system
setup-system: setup-python-system setup-pre-commit

# Set up the python environment (default: uv-managed .venv).
.PHONY: setup-python
setup-python:
	bash ./dev/setup.sh --deps "development"

# Set up with system-site install (opt-in; not for PEP 668 / Homebrew Python).
.PHONY: setup-python-system
setup-python-system:
	bash ./dev/setup.sh --deps "development" --system

# Set up the pre-commit hooks.
.PHONY: setup-pre-commit
setup-pre-commit:
	uv run pre-commit install

# Check all the coding style.
.PHONY: lint
lint: run-pre-commit

# Run the pre-commit hooks.
.PHONY: run-pre-commit
run-pre-commit:
	uv run pre-commit run --all-files

# Update the pre-commit hooks.
.PHONY: update-pre-commit
update-pre-commit:
	uv run pre-commit autoupdate

# Run the unit tests.
.PHONY: test
test:
	uv run bash ./dev/test_python.sh

# Build the package
.PHONY: build
build: clean lint test
	uv run bash -x ./dev/build.sh

# Clean the environment
.PHONY: clean
clean:
	uv run bash ./dev/clean.sh

# Publish to pypi
.PHONY: publish
publish:
	uv run bash ./dev/publish.sh "pypi"

# Publish to testpypi
.PHONY: test-publish
test-publish:
	uv run bash ./dev/publish.sh "testpypi"
