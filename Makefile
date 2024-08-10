run:
	@docker compose run demo python examples/simulation.py

stop:
	@docker compose down

enter:
	@docker compose run demo bash

lint:
	@docker compose run demo bash -c " \
		echo --- RUFF --- \
		&& ruff check \
		&& echo --- MYPY --- \
		&& mypy device_monitor"

lint-autofix:
	@docker compose run demo bash -c " \
		echo --- RUFF --- \
		&& ruff check --fix"

test:
	@docker compose run demo pytest --disable-warnings

test-cov:
	@docker compose run demo pytest --cov=device_monitor tests
