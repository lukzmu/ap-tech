![Codecov](https://img.shields.io/codecov/c/github/lukzmu/ap-tech)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/lukzmu/ap-tech/main.yml)
![GitHub License](https://img.shields.io/github/license/lukzmu/ap-tech)


# Device Monitor

This project is part of a recruitment task for AP-Tech.

## Task

![Demo Image](/docs/demo.png)

- [x] Methods `start`, `stop` and `get_statuses` on `DeviceMonitor`.
- [x] Thread safe methods and main thread methods,
- [x] Possible to add new devices without code changes,
- [x] Sample simulation script that writes out data every second,
- [x] 100% coverage in tests.

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Commands

| **Command** | **Description** |
| :--- | :--- |
| `make run`| Runs the package demo |
| `make stop` | Stops the package demo |
| `make enter` | Enter the container |
| `make lint` | Check code for linting errors |
| `make lint-autofix` | Automatically fix linting errors |
| `make test` | Run project tests |
| `make test-cov` | Check code coverage |
