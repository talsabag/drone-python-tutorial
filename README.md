# Drone Seed Project : Python Tutorial

[![Build Status](https://ci.cloudlockng.com/api/badges/talsabag/drone-python-tutorial/status.svg)](https://ci.cloudlockng.com/talsabag/drone-python-tutorial)

This project is nothing special, just simply and example REST Service written in `python`.

This service is used as a seed project for creating a [drone CI/CD pipeline](https://drone.io).

The development environment uses [Docker](http://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). This makes it super easy to get up and running with a configuration that would closely mirror production.

With Docker/Compose installed, use the following steps to launch for the first time:

* `docker-compose up` to start the web app. This will download and provision two containers: one running PostgreSQL and one running the Flask app. This will take a while, but once it completes subsequent launches will be much faster. (NOTE: if you are using the Vagrant VM that was provisioned in the first step, change into the `/vagrant` directory before running `docker-compose up`.)

* When `docker-compose up` completes, the app should be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

**Note, as the project tutorial progresses, you will see the value of understanding docker-compose, and docker in the usage of drone to build a pipeline. Drone mirrors the syntax of docker-compose almost exactly - with little variation**

Environment Variables
====================

There are just a couple of configurations managed as environment variables. In the development environment, these are injected by Docker Compose and managed in the `docker-compose.yml` file.

* `DATABASE_URL` - This is the connection URL for the PostgreSQL database. It is not used in the **development environment**.
* `DEBUG` - This toggle debug mode for the app to True/False.
* `SECRET_KEY` - This is a secret string that you make up. It is used to encrypt and verify the authentication token on routes that require authentication.

These are also injected when using the `docker-compose.test.yml` file.

Project Organization
====================

* Application-wide settings are stored in `config.py` at the root of the repository. These items are accessible on the `config` dictionary property of the `app` object. Example: `debug = app.config['DEBUG']`
* The directory `service/app` contains the API application
* URL mapping is managed in `service/app/routes.py`
* Functionality is organized in packages. Example: `service/app/users` or `service/app/utils`.
* Tests are contained in each package. Example: `service/app/users/tests.py`
* The directory `integ-tests\*` contains integration tests leveraging `nosetests` - which are to be run from a SUT system.
* `migrations\*` contains alembic migration code for the database which can also be run from the SUT system.
* `docker\Dockerfile` contains the logic to build up a binary distribution of the service in a docker container
* `docker-compose.yml` file contains the basic services - and will allow you to bring up the environment for use.
* `docker-compose.test.yml` file contains the basic services plus a SUT instances - while allows for integration testing.
* `MANIFEST.in` contains distribution packaging requirements; which work with `setup.py` and the `requirements.txt`, and `test-requirements.txt` respectively.

Running Unit Tests
====================

Tests are ran with [nose](https://nose.readthedocs.org/en/latest/) from inside the `docker-compose` web container:

```
  docker-compose -f docker-compose.yml run web /env/bin/nosetests -v /app/test/unit
```

Running Functional Tests
====================

Tests are ran with [nose](https://nose.readthedocs.org/en/latest/) from inside the `docker-compose` web container:

```
  docker-compose -f docker-compose.yml run web /env/bin/nosetests -v /app/test/functional
```

**NOTE** you might need to run this twice as the DB might take a second to init...

Running Integration Testing
====================

Integration Tests are ran from a System Under Test (SUT) with [nose](https://nose.readthedocs.org/en/latest/) from inside the `docker-compose.test` *sut* container:

```
  docker-compose -f docker-compose.yml -f docker-compose.test.yml run sut /env/bin/nosetests -v /app/test/integration
```

This simulates making API calls from outside of the `web` service container. Note the `web` service container will use both the `database` and `redis` service containers actually simulating an e2e test as well.

Running Database Migrations
====================

Migrations for the provided models are part of the project. To generate new migrations use `Flask-Migrate`:

```
  docker-compose -f docker-compose.yml -f docker-compose.test.yml run sut /env/bin/python /app/service/run.py db upgrade
  docker-compose -f docker-compose.yml -f docker-compose.test.yml run sut /env/bin/python /app/service/run.py db migrate
```


API Routes
====================

This API uses token-based authentication. A token is obtained by registering a new user (`/api/v1/user`) or authenticating an existing user (`/api/v1/authenticate`). Once the client has the token, it must be included in the `Authorization` header of all requests.


### Register a new user
---
**POST:**
```
/api/v1/user
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "123456"
}
```

**Response:**
```json
{
    "id": 2,
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxMDk2ODA5NCwiaWF0IjoxNDA5NzU4NDk0fQ.eyJpc19hZG1pbiI6ZmFsc2UsImlkIjoyLCJlbWFpbCI6InRlc3QyQHRlc3QuY29tIn0.goBHisCajafl4a93jfal0sD5pdjeYd5se_a9sEkHs"
}
```

**Status Codes:**
* `201` if successful
* `400` if incorrect data provided
* `409` if email is in use

**Example:**
```
curl -H "Content-Type: application/json" -X POST -d '{"email": "something@email.com","password": "123456"}' http://localhost:5000/api/v1/user
```

### Authenticate a user
---

**POST:**
```
/api/v1/authenticate
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "123456"
}
```

**Response:**
```json
{
    "id": 2,
    "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxMDk2ODA5NCwiaWF0IjoxNDA5NzU4NDk0fQ.eyJpc19hZG1pbiI6ZmFsc2UsImlkIjoyLCJlbWFpbCI6InRlc3QyQHRlc3QuY29tIn0.goBHisCajafl4a93jfal0sD5pdjeYd5se_a9sEkHs"
}
```

**Status Codes:**
* `200` if successful
* `401` if invalid credentials

**Example:**
```
curl -H "Content-Type: application/json" -X POST -d '{"email": "something@email.com","password": "123456"}' http://localhost:5000/api/v1/authenticate
```

### Get the authenticated user
---

**GET:**
```
/api/v1/user
```

**Response:**
```json
{
    "id": 2,
    "email": "test2@test.com",
}
```

**Status Codes:**
* `200` if successful
* `401` if not authenticated

**Example:**

*The token show below is returned from the previous POST authorize API call*
```
curl -H "Authorization: eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwNDQ5NjcwOSwiaWF0IjoxNTAzMjg3MTA5fQ.eyJpc19hZG1pbiI6ZmFsc2UsImlkIjoxLCJlbWFpbCI6InNvbWV0aGluZ0BlbWFpbC5jb20ifQ.TcD7N62bfcDEyOzS4_8KnT9v9iQwZCJipxxtSiPf5tQ" -X GET http://localhost:5000/api/v1/user
```
