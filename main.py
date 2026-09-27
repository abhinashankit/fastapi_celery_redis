from fastapi import FastAPI
from celery.result import AsyncResult

from .celery_app import celery_app
from .tasks import process_user


app = FastAPI(title="FastAPI + Celery + Redis")


@app.get("/")
def home():
    return {"message": "FastAPI + Celery + Redis is running"}


@app.post("/tasks/process-user/{user_id}")
def create_task(user_id: int):
    task = process_user.delay(user_id)

    return {
        "message": "Task queued successfully",
        "task_id": task.id,
        "status": "queued",
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task.status,
    }

    if task.ready():
        response["result"] = task.result

    return response
