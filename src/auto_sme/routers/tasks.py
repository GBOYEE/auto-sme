"""Tasks router — CRUD for scheduled tasks."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime
from auto_sme.dependencies import verify_api_key

router = APIRouter(prefix="/tasks", dependencies=[Depends(verify_api_key)])

# In-memory store for MVP; will be replaced with DB
_tasks_db: List[dict] = []

class TaskCreate(BaseModel):
    name: str
    cron: str
    action: str  # sms_alert, inventory_check, sales_report
    payload: Optional[dict] = None

class Task(TaskCreate):
    id: str
    created_at: datetime

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, api_key: str = Depends(lambda: None)):
    # TODO: use agent-core to interpret natural language if needed
    new_task = {
        "id": str(uuid.uuid4()),
        "name": task.name,
        "cron": task.cron,
        "action": task.action,
        "payload": task.payload or {},
        "created_at": datetime.utcnow(),
    }
    _tasks_db.append(new_task)
    # TODO: schedule via automation-engine
    return new_task

@router.get("", response_model=List[Task])
async def list_tasks(status: Optional[str] = None, api_key: str = Depends(lambda: None)):
    if status == "active":
        # Filter by cron presence (dummy)
        return [t for t in _tasks_db if t.get("cron")]
    return _tasks_db
