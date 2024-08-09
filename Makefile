run:
	@docker compose up

stop:
	@docker compose down

enter:
	@docker compose run demo bash

lint:
	@docker compose run demo -c " \
		echo --- RUFF --- "
		&& ruff check \
		&& echo --- MYPY --- \
		&& mypy ."

lint-autofix:
	@docker compose run demo -c " \
		echo --- RUFF --- "
		&& ruff check --fix"

test:
	@docker compose run demo pytest
