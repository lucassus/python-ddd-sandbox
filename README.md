# Python Clean Architecture and Domain Driven Development sandbox app 

## Preparing and running the app

* Install [uv](https://docs.astral.sh/uv/) — it manages the Python 3.14 toolchain and dependencies
* `uv sync` (creates `.venv` from `uv.lock`, installing Python 3.14 if needed)
* `make seed`
* `make server-dev`

http://localhost:8000/docs
http://localhost:8000/api/docs

## Linting and testing

* `make lint-all` (ruff lint + format check + ty type check)
* `make format` (ruff format + autofix)
* `make test`
* `make test-watch`

```
curl http://localhost:8000/api/users -X POST -H "Content-Type: application/json" -d '{"email": "test@email.com", "password": "passwdowrd"}' --silent
curl http://localhost:8000/api/projects/1/tasks --silent | jq
```

## Other useful commands

* `uv pip list --outdated`
* `uv lock --upgrade` (refresh the lockfile to the latest compatible versions)

## Books that inspired me to create this project

* [Architecture Patterns with Python](https://www.cosmicpython.com/)
* [Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
* [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
* [Domain-Driven Design Distilled](https://www.amazon.com/Domain-Driven-Design-Distilled-Vaughn-Vernon/dp/0134434420)
* [Implementing Domain-Driven Design](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)

## Other valuable resources

* https://www.youtube.com/watch?v=Ru2T4fu3bGQ
* [FastAPI Best Practices and Conventions](https://github.com/zhanymkanov/fastapi-best-practices)
