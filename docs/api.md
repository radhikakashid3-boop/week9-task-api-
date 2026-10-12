# Task Management REST API

Base URL: `http://127.0.0.1:5000`

## Authentication

### Register
`POST /api/auth/register`

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "secret123"
}
```

### Login
`POST /api/auth/login`

```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

Copy the returned `access_token` and send:

`Authorization: Bearer <access_token>`

## Tasks

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `PUT /api/tasks/{id}`
- `PATCH /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
- `GET /api/tasks/search?q=api`

### Filtering
`GET /api/tasks?status=pending&priority=high`

### Sorting
`GET /api/tasks?sort_by=due_date&sort_order=asc`

### Pagination
`GET /api/tasks?page=1&per_page=10`

## Users

`GET /api/users/me`

## Status Codes

- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 409 Conflict
- 429 Too Many Requests
- 500 Internal Server Error
