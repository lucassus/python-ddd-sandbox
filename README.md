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

## Layout

* `infrastructure`
  * `migrations` 
  * `tables.py`
* `modules`
  * `accounts`
    * `adapters`
      * `mappers.py`
      * `repository.py`
      * `unit_of_work.py`
    * `domain`
      * `ports`
        * `abstract_repository.py`
        * `abstract_unit_fo_work.py`
      * `use_cases`
        * `change_user_email_address.py`
        * `register_user.py`
    * `entrypoints`
      * `routers.py`
      * `schemas.py`
  * `projects`
    * `adapters`
      * ...
    * `domain`
      * `entities`
        * `project.py`
        * `task.py`
      * `use_cases`
        * `create_project.py`
        * `create_example_project.py`
        * `create_task.py`
        * `complete_task.py`
        * `incomplete_task.py`
    * `entrypoints`
      * ...
  * `projects`
    * `domain`
      * `project`
        * __init__.py
        * aggregate_root.py
        * task.py
        * factories.py
        * repository.py
* `query`
* `shared_kernel`

## Resources

* https://www.youtube.com/watch?v=Ru2T4fu3bGQ
