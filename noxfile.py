"""Nox sessions for supported Python versions."""

from __future__ import annotations

import nox

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]

nox.options.default_venv_backend = "uv"


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Run the test suite in an isolated uv-backed environment."""
    env = {"UV_PROJECT_ENVIRONMENT": str(session.virtualenv.location)}
    session.run_install("uv", "sync", "--frozen", "--all-extras", env=env)
    session.run("bash", "dev/test_python.sh", external=True, env=env)
