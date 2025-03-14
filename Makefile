run-local:
	uv run migrate.py
	uv run fastapi dev app.py