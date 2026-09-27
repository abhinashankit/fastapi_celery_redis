# FastAPI + Celery + Redis + SQLite

## Architecture

FastAPI -> Redis -> Celery Worker -> SQLite

Redis is used as the Celery broker and result backend.

## 1. Install dependencies

```bash
python -m venv venv
```

Linux/macOS:
```bash
source venv/bin/activate
```

Windows:
```powershell
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

## 2. Start Redis

Make sure Redis is installed and running.

```bash
redis-server
```

Default Redis URL:

```text
redis://localhost:6379/0
```

## 3. Initialize SQLite

From the project root:

```bash
python -m app.init_db
```

This creates `test.db` and the `users` table.

You can add a test user using SQLite:

```bash
sqlite3 test.db
```

Then:

```sql
INSERT INTO users (name, status) VALUES ('Abinash', 'pending');
.quit
```

The first user will normally have ID 1.

## 4. Start FastAPI

```bash
uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## 5. Start the Celery worker

Open another terminal in the project root:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

## 6. Create a background task

Call:

```http
POST /tasks/process-user/1
```

Example response:

```json
{
  "message": "Task queued successfully",
  "task_id": "some-task-id",
  "status": "queued"
}
```

FastAPI returns immediately. The Celery worker performs the slow work in the background.

## 7. Check task status

```http
GET /tasks/{task_id}
```

While running:

```json
{
  "task_id": "some-task-id",
  "status": "PENDING"
}
```

After completion:

```json
{
  "task_id": "some-task-id",
  "status": "SUCCESS",
  "result": {
    "status": "success",
    "user_id": 1,
    "message": "User processed successfully"
  }
}
```

## Production note

SQLite is suitable for development and small workloads. For multiple workers or higher concurrent writes, PostgreSQL is recommended.

Also, rotate the SECRET_KEY if the key included in this example is a real production secret.
