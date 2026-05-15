# ProductDNA Task Manager API

Django REST API for managing **Tasks** and **Tags** with a many-to-many relationship.

**Assessment contact:** ossama.harach@productdna.com

<img width="1903" height="424" alt="image" src="https://github.com/user-attachments/assets/47da095e-d793-4934-a646-d3b6c8ff8177" />
<img width="1907" height="401" alt="image" src="https://github.com/user-attachments/assets/8793b999-80f4-465e-bbb9-2319b42a80df" />
<img width="1195" height="613" alt="image" src="https://github.com/user-attachments/assets/bfa6d782-f125-4106-bcec-293bf8763410" />
<img width="1222" height="888" alt="image" src="https://github.com/user-attachments/assets/8b3e9e33-2e3c-4348-84b1-d1b422fc2fb2" />
<img width="1193" height="468" alt="image" src="https://github.com/user-attachments/assets/e544b0bc-5e0a-4e86-8989-193f024f87dd" />


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
