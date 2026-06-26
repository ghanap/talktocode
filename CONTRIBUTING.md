# Contributing to the Software Bug Assistant

Welcome! We appreciate your interest in contributing to the Software Bug Assistant. This document outlines the process for contributing to the project to ensure a smooth, secure, and high-quality development workflow.

## 1. Getting Started

1.  **Fork and Clone:** Fork the repository to your own GitHub account and clone it to your local machine.
2.  **Install Dependencies:** We use Python 3.11+. Install the required dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```
3.  **Set Up Pre-Commit Hooks:** We enforce code quality strictly at the local level. Ensure you have the pre-commit hooks installed so your code is checked before every commit:
    ```bash
    pip install pre-commit
    pre-commit install
    ```

## 2. Branching Strategy

We follow a standard feature-branch workflow. Please **never** commit directly to the `main` branch.
*   **Feature Branches:** Prefix your branches with `feat/` (e.g., `feat/add-new-mcp-tool`).
*   **Bugfix Branches:** Prefix your branches with `fix/` (e.g., `fix/database-timeout`).
*   **Documentation:** Prefix with `docs/` (e.g., `docs/update-readme`).

## 3. Development Standards

Before you submit a Pull Request, ensure your code meets the following standards. Our GitLab CI pipeline will strictly enforce these:
*   **Formatting & Linting:** We use `ruff`. Run `ruff format .` and `ruff check --fix .` locally.
*   **Type Checking:** We use `mypy`. Ensure your code passes static type analysis.
*   **Testing:** We use `pytest`. All new features must be accompanied by unit tests. Run `pytest tests/` locally to ensure no regressions.
*   **Security:** Avoid hardcoding any secrets (API keys, passwords). The pipeline runs `bandit` to scan for security vulnerabilities.

## 4. The CI/CD Pipeline

When you push your branch and open a Merge Request/Pull Request, our automated pipeline will trigger. It consists of 5 strict stages:
1.  **Prepare:** Validates the environment.
2.  **Format:** Enforces Ruff code quality.
3.  **Type Check:** Enforces strict static typing.
4.  **Security:** Scans for vulnerabilities.
5.  **Test:** Runs the entire test suite.

*Your PR will not be reviewed or merged unless all 5 stages display a green checkmark.*

## 5. Submitting Your Changes

1.  Commit your changes with clear, descriptive commit messages.
2.  Push your branch to your fork.
3.  Open a Pull Request against the `main` branch of the upstream repository.
4.  Link any relevant issues (e.g., `Closes #42`) in your PR description.
5.  Wait for the automated CI pipeline to pass and a maintainer to review your code.

Thank you for helping us make the Software Bug Assistant better!
