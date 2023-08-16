# Python Clean Architecture and Domain Driven Development sandbox app 

## Preparing and running the app

* `make venv`
* `make install`
* `make seed`
* `make server-dev`

http://localhost:8000/queries/docs
http://localhost:8000/commands/docs

## Linting and testing

* `make lint`
* `make test`
* `make test-watch`

```
curl http://localhost:8000/commands/users -X POST -H "Content-Type: application/json" -d '{"email": "test@email.com", "password": "passwdowrd"}' --silent
curl http://localhost:8000/queries/projects/1/tasks --silent | jq
```

## Other useful commands

* `pip list --outdated`
* `libyear -r requirements.txt`

## Books that inspired me to create this project

* [Architecture Patterns with Python](https://www.cosmicpython.com/)
* [Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
* [Domain-Driven Design: Tackling Complexity in the Heart of Software](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
* [Domain-Driven Design Distilled](https://www.amazon.com/Domain-Driven-Design-Distilled-Vaughn-Vernon/dp/0134434420)
* [Implementing Domain-Driven Design](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)

## Other valuable resources

* https://www.youtube.com/watch?v=Ru2T4fu3bGQ
