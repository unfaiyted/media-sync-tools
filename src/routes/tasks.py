from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from src.models.tasks import Task

from src.config import ConfigManager
from src.tasks.tasks import execute_task

router = APIRouter()
config = ConfigManager.get_manager()


# Assuming you've already defined the Pydantic models in the same file (or you can import them)

# This is an in-memory storage of tasks for demonstration purposes.
# In a real-world application, this would be replaced with database operations.
tasks_db = []

@router.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    tasks_db.append(task)
    return task

@router.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks_db

@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_id] = task
    return task

@router.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db.pop(task_id)

@router.post("/tasks/{task_id}/trigger")
async def trigger_task_on_demand(task_id: str, db: AsyncIOMotorDatabase = Depends(config.get_db)):
    # Fetch the task from the database
    task = await db.scheduledTasks.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        # Execute the task immediately
        await execute_task(task['taskType'], task.get('payload'))
        return {"status": "success", "message": "Task triggered successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error triggering task: {str(e)}"}
