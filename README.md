# ProductDNA Task Manager API

Django REST API for managing **Tasks** and **Tags** with a many-to-many relationship.

**Assessment contact:** ossama.harach@productdna.com

## Features

- Full CRUD for tasks and tags
- Tasks return nested tag data; tags can be linked by ID or created inline via `tag_names`
- HTTP Basic Authentication (all API endpoints require authentication)
- Duplicate tag names rejected at model and serializer level
- Filter tasks: `?status=pending` and `?tag=work`

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base URL: `http://127.0.0.1:8000/api/`

## Authentication

Use the superuser credentials with HTTP Basic Auth:

```bash
curl -u username:password http://127.0.0.1:8000/api/tasks/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/tasks/` | List / create tasks |
| GET/PUT/PATCH/DELETE | `/api/tasks/{id}/` | Retrieve / update / delete task |
| GET/POST | `/api/tags/` | List / create tags |
| GET/PUT/PATCH/DELETE | `/api/tags/{id}/` | Retrieve / update / delete tag |

### Create task with nested tags

```json
POST /api/tasks/
{
  "title": "Deploy release",
  "description": "Production deployment",
  "status": "in_progress",
  "tag_names": [{"name": "work"}, {"name": "release"}]
}
```

### Link existing tags by ID

```json
POST /api/tasks/
{
  "title": "Review PR",
  "status": "pending",
  "tag_ids": [1, 2]
}
```

### Filter tasks

```
GET /api/tasks/?status=pending
GET /api/tasks/?tag=work
```

### Task status values

- `pending`
- `in_progress`
- `done`

## Tests

```bash
python manage.py test
```

## Tech stack

- Django 5.x
- Django REST Framework
- django-filter
- SQLite (development)
