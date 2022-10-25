# Secure-T test task
## Run tests
### This commands include testing alembic migrations
```shell
docker-compose -f docker-compose.test.yml -p test up -d --build
docker-compose -f docker-compose.test.yml -p test exec -it backend alembic upgrade head
docker-compose -f docker-compose.test.yml -p test exec -it backend pytest --test-alembic
docker-compose -f docker-compose.test.yml -p test down -v
```

## Run server
```shell
docker-compose up -d
cd src
poetry shell
poetry install
python main.py
```

## Run migrations
### Create migration
```shell
cd src
alembic revision --autogenerate -m "migration_name"
```

### Upgrade db schema
```shell
alembic upgrade head
```

### Downgrade db schema
```shell
alembic downgrade -1
```