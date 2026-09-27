import time

from .celery_app import celery_app
from .database import SessionLocal
from .models import User


@celery_app.task
def process_user(user_id: int):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return {
                "status": "failed",
                "message": f"User {user_id} not found",
            }

        # Simulate a slow/background operation.
        time.sleep(10)

        user.status = "processed"
        db.commit()

        return {
            "status": "success",
            "user_id": user_id,
            "message": "User processed successfully",
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
