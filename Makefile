DC = docker compose
APP_FILE = docker-compose.yaml
EXEC = docker exec -it
ENV = --env-file .env

# === All Project ===
.PHONY: all stop clean tests

all:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

stop:
	${DC} -f ${APP_FILE} down

clean:
	${DC} -f ${APP_FILE} down --volumes --remove-orphans

tests:
	uv run pytest

migrate.up:
	uv run alembic revision --autogenerate -m "$(message)"
	uv run alembic upgrade head

migrate.down:
	uv run alembic down -1