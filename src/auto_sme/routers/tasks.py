"""Tasks router — CRUD for scheduled tasks."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from auto_sme.dependencies import verify_api_key
from auto_sme.crud import create_task, get_tasks
from auto_sme.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tasks", dependencies=[Depends(verify_api_key)])

class TaskCreate(BaseModel):
    name: str
    cron: str
    action: str  # sms_alert, inventory_check, sales_report
    payload: Optional[dict] = None

class Task(TaskCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(
        db=db,
        name=task.name,
        cron=task.cron,
        action=task.action,
        payload=task.payload
    )

@router.get("", response_model=List[Task])
async def list_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    return get_tasks(db, status=status)
