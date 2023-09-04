from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from src.config import ConfigManager



async def run_scheduled_tasks(db: AsyncIOMotorDatabase = Depends(config.get_db)):
    now = datetime.now()
    tasks = [task_doc async for task_doc in db.tasks.find({"nextRunTime": {"$lte": now}})]

    for task in tasks:
        # Here, we'll just print the command for demonstration purposes
        # In a real application, you would do more depending on the type and nature of the task.
        print(f"Running task with command: {task['command']}")
        # Update the nextRunTime in the database or remove the task if it's a one-time task
