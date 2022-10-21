create migration
alembic revision --autogenerate -m "migration_name"

upgrade db schema
alembic upgrade head
