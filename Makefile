run-local:
	uv run migrate.py
	uv run fastapi dev app.py

container:
	docker-compose build
	docker-compose up -d

container-migrate:
	docker exec -t ap1 python migrate.py