[![codecov](https://codecov.io/gh/lukzmu/ap-tech/graph/badge.svg?token=VZ1R9DVT79)](https://codecov.io/gh/lukzmu/ap-tech)

# Device Monitor

This project is part of a recruitment task for AP-Tech.

## Task

![Demo Image](/docs/demo.png)

- [x] Methods `start`, `stop` and `get_statuses` on `DeviceMonitor`.
- [x] Thread safe methods and main thread methods,
- [x] Possible to add new devices without code changes,
- [x] Sample simulation script that writes out data every second,
- [ ] Test it all out!

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
