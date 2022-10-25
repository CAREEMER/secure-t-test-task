# Run tests
## This commands include testing alembic migrations
```shell
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml exec -it backend pytest --test-alembic
docker-compose -f docker-compose.test.yml down -v
```

# Migrations
## Create migration
```shell
cd src
alembic revision --autogenerate -m "migration_name"
```
## Upgrade db schema
```shell
alembic upgrade head
```

## Downgrade db schema
```shell
alembic downgrade -1
```

# Run server
```shell
cd src
python main.py
```