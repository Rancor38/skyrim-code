# Purpose
This file provides coding standards and context for GitHub Copilot and AI agents contributing to this project.

# Up-to-date Practices
- Always refer to the **latest official AWS documentation** when using SDKs, services, and runtime environments.
- Replace **deprecated methods** with up-to-date alternatives; resolve deprecation warnings immediately.

# Code Quality Guidelines
- Avoid unnecessary comments; write **self-documenting code**.
- Do **not log internal errors to the client**. Use secure and private server-side logging instead.
- Use **clear and descriptive variable names**.
  - Do **not** use reserved keywords.
  - Avoid generic names like `temp`, `foo`, `bar`, unless contextually appropriate.
  - Always address deprecation warnings in code and documentation.
  - Run `npm audit fix --force` to address vulnerabilities.
  - Fix syntax and linting issues before committing.

# File Size & Structure
- Each file must be **< 700 lines**.
- Refactor large files into **modular components**, grouped by purpose.
  - Use clearly named directories to organize related functionality.
- Keep the workspace **tidy and logically organized**.

# Execution Requirements
- All scripts and executables must be **runnable from the root directory**.
  - If not directly, provide a **proxy or wrapper script** (e.g., Makefile, shell script, CLI entry point).
  - Use relative imports and avoid hardcoded paths.
  - Code functionality should be functional from frontend to backend to be considered complete.

# Project Structure Example
.
├── scripts/         # Utility and CLI scripts
├── services/        # AWS integrations, microservices
├── handlers/        # Request/response logic
├── utils/           # Shared helpers
├── config/          # Configuration and environment setup
├── tests/           # Unit and integration tests
├── Makefile         # Proxy for common commands
├── README.md
└── .copilot/context.txt  # You are here.

# Summary
Be clean, current, and consistent. Structure and maintain code for long-term readability and maintainability.