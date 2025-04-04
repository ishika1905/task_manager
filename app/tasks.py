from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app import auth, database, models, schemas

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_active_user),
):
    # If task is being assigned to someone, verify user exists
    if task.assigned_to_id:
        assigned_user = db.query(models.User).filter(models.User.id == str(task.assigned_to_id)).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    db_task = models.Task(**task.dict(), created_by_id=str(user.id))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=list[schemas.Task])
def get_tasks(
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_active_user),
):
    if user.role == "admin":
        return db.query(models.Task).all()
    elif user.role == "manager":
        return db.query(models.Task).filter(models.Task.assigned_to_id == str(user.id)).all()
    else:
        return db.query(models.Task).filter(models.Task.created_by_id == str(user.id)).all()

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: UUID,
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_active_user),
):
    db_task = db.query(models.Task).filter(models.Task.id == str(task_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    authorized = (
        user.role == "admin" or
        (user.role == "manager" and db_task.assigned_to_id == str(user.id)) or
        (user.role == "user" and db_task.created_by_id == str(user.id))
    )

    if not authorized:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    # Validate assigned_to_id if provided
    if task.assigned_to_id:
        assigned_user = db.query(models.User).filter(models.User.id == str(task.assigned_to_id)).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    for key, value in task.dict().items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    db: Session = Depends(database.get_db),
    user: models.User = Depends(auth.get_current_active_user),
):
    db_task = db.query(models.Task).filter(models.Task.id == str(task_id)).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete tasks")

    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
