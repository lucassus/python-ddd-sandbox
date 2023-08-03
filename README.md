# Python Clean Architecture sandbox app 

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
* `pip-compile --upgrade-package pytest`

## Resources

* https://www.youtube.com/watch?v=Ru2T4fu3bGQ
