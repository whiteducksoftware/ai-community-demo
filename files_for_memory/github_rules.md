# GitHub Interaction Rules for Agentic Developers

This document outlines the best practices and conventions for how our "agentic developers" (automated agents managed by the orchestrator) should interact with the GitHub repository for the Simple Task Management Web Application project. Adhering to these rules ensures consistency, clarity, and effective collaboration, even when dealing with automated contributions.

## 1. Branching Strategy

* **Main Branch:** `main` (protected branch). All pull requests must target this branch.
* **Feature Branches:** All new development (features, bug fixes, improvements) must be done on dedicated branches.
    * **Naming Convention:** `feature/ISSUE-NUMBER-short-description` or `bugfix/ISSUE-NUMBER-short-description`.
    * **Example:** `feature/STM-001-add-task-creation`
* **No Direct Commits to `main`:** Agentic developers are strictly forbidden from pushing directly to the `main` branch.

## 2. Commit Messages

* **Format:** Conventional Commits are preferred for clear history.
    * `<type>(<scope>): <subject>`
    * `<body>` (optional)
    * `<footer>` (optional, e.g., "Closes #ISSUE-NUMBER")
* **Types:**
    * `feat`: A new feature
    * `fix`: A bug fix
    * `docs`: Documentation only changes
    * `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semicolons, etc.)
    * `refactor`: A code change that neither fixes a bug nor adds a feature
    * `perf`: A code change that improves performance
    * `test`: Adding missing tests or correcting existing tests
    * `build`: Changes that affect the build system or external dependencies
    * `ci`: Changes to our CI configuration files and scripts
    * `chore`: Other changes that don't modify src or test files
    * `revert`: Reverts a previous commit
* **Scope:** Optional, specifies the part of the codebase affected (e.g., `frontend`, `backend`, `database`).
* **Subject:** Concise, imperative mood, less than 72 characters.
* **Example:**
    ```
    feat(frontend): Implement task creation form

    Adds a new React component for inputting task titles and descriptions.
    Includes basic validation for title field.

    Closes #STM-001
    ```

## 3. Pull Request (PR) Structure

* **Purpose:** All code changes must go through a Pull Request.
* **Title:** Should clearly describe the PR's