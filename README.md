# Task Management REST API

A complete Flask REST API for task management with JWT authentication, CRUD operations, filtering, sorting, pagination, validation, rate limiting, CORS, Swagger/OpenAPI documentation, Postman collection and unit tests.

## Features

- User registration and JWT login
- Access and refresh tokens
- Task CRUD
- Filtering by status, priority and category
- Sorting
- Pagination
- Search
- Input validation
- Consistent JSON responses
- Rate limiting
- CORS
- Swagger/OpenAPI specification
- Postman collection
- Pytest unit tests

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 2. Install packages

```bash
python -m pip install -r requirements.txt
```

### 3. Run

```bash
python run.py
```

API:

`http://127.0.0.1:5000`

### 4. Test

```bash
pytest -v
```

## Main endpoints

- POST `/api/auth/register`
- POST `/api/auth/login`
- POST `/api/auth/refresh`
- POST `/api/auth/logout`
- GET `/api/users/me`
- GET `/api/tasks`
- POST `/api/tasks`
- GET `/api/tasks/<id>`
- PUT `/api/tasks/<id>`
- PATCH `/api/tasks/<id>`
- DELETE `/api/tasks/<id>`
- GET `/api/tasks/search?q=keyword`

See `docs/api.md`, `docs/swagger.yaml` and `docs/postman_collection.json`.

## GitHub

Do not commit the virtual environment, database, `.env`, or Python cache files.


## Windows / VS Code quick start

1. Extract the ZIP and open the `week9-task-api` folder in VS Code.
2. Open Terminal in VS Code.
3. Create a virtual environment once, if `venv` does not exist:
   `py -m venv venv`
4. Activate it in PowerShell:
   `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`
   `.env\Scripts\Activate.ps1`
5. Install packages:
   `python -m pip install -r requirements.txt`
6. Run the API:
   `python run.py`
7. In a second terminal, run tests:
   `python -m pytest -v`

If `(venv)` is already visible in the terminal, do not run `python -m venv venv` again.
The in-memory rate-limit storage warning is expected for local development; production
deployments should configure a persistent backend such as Redis and use secure environment secrets.
