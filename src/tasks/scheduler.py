from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config import ConfigManager
from .tasks import execute_task
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()


async def check_and_execute_tasks():
    config = await ConfigManager().get_manager()
    log = config.get_logger(__name__)
    db = config.get_db()  # Get your database connection, similar to what's in your routes
    now = datetime.now()

    # Fetch tasks ready for execution
    tasks_ready = await db.scheduledTasks.find({"nextExecution": {"$lte": now}}).to_list(None)

    for task in tasks_ready:
        log.debug(f"Executing task with payload", task=task)
        await execute_task(task['taskType'], task.get('payload'))

        # Update task's lastExecuted and nextExecution in the database
        task['lastExecuted'] = now
        if task['schedule'] == "daily":
            task['nextExecution'] = now + timedelta(days=1)
        # If there are other schedules, handle them accordingly.
        await db.scheduledTasks.replace_one({"_id": task["_id"]}, task)


# In your scheduler setup
def start_scheduler():
    # Check every minute for tasks ready to be executed
    trigger = IntervalTrigger(minutes=1)
    scheduler.add_job(check_and_execute_tasks, trigger)
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
