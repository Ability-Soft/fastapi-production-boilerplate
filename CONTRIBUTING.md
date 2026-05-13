# Contributing to AbilitySoft FastAPI Boilerplate

First off, thank you for considering contributing to an AbilitySoft project! It's people like you who make our tools better for everyone.

## 🌈 Our Standards

We aim for world-class quality. This means:
- **Clean Code**: Follow PEP 8 and our `ruff` configuration.
- **Type Safety**: All new code must be fully type-hinted and pass `mypy`.
- **Tested Logic**: No feature is complete without passing tests.
- **Documentation**: Update the README or relevant docs if you change how something works.

## 🚀 Getting Started

1. **Fork the repo** and create your branch from `main`.
2. **Setup your environment**:
   ```bash
   make install
   pre-commit install
   ```
3. **Make your changes**. Ensure you follow the established architecture (Routers → Services → Repositories).
4. **Run the quality suite**:
   ```bash
   make lint
   make test
   ```

## 📨 Pull Request Process

1. Use the provided PR template.
2. Link any relevant issues.
3. Ensure the CI pipeline passes.
4. Once approved, your PR will be merged into `main`.

## 💎 Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for formatting and linting.
Run `make format` before committing.

## ❓ Questions?

Feel free to open an issue or contact the AbilitySoft team at info@abilitysoft.net.
