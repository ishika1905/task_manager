from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
from app.utils.email import send_email_reminder

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(
    background_tasks: BackgroundTasks,  # ✅ FIXED: Moved to the start
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_task = models.Task(**task.dict(), created_by_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Send email if due date is within 24 hours
    if new_task.due_date:
        time_diff = new_task.due_date - datetime.utcnow()
        if timedelta(hours=0) < time_diff <= timedelta(hours=24):
            assigned_user = db.query(models.User).filter(models.User.id == new_task.assigned_to_id).first()
            if assigned_user:
                background_tasks.add_task(
                    send_email_reminder,
                    assigned_user.email,
                    new_task.title,
                    new_task.due_date.strftime("%Y-%m-%d %H:%M:%S")
                )

    return new_task
