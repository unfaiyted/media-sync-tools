from __future__ import annotations

from pydantic import BaseModel, Field

from datetime import datetime
from typing import List, Optional, Dict, Any, Union

# Main Task Schedule Model
class TaskSchedule(BaseModel):
    type: str = Field(..., description="The type of schedule (interval, cron, date)")
    details: Dict[str, Union[str, int]] = Field(..., description="Details of the scheduling type")
    timeZone: Optional[str] = Field("UTC", description="Timezone for the task schedule")

# Status of a Task
class TaskStatus(BaseModel):
    lastRunTime: datetime
    nextRunTime: datetime
    state: str = Field(..., description="State of the task (running, paused, failed, etc.)")
    error: Optional[str] = Field(None, description="Error details if the task failed")

# Metadata for Task
class TaskMetadata(BaseModel):
    createdBy: str
    createdOn: datetime
    lastModified: datetime
    tags: List[str] = Field(..., description="Tags associated with the task")
    priority: str = Field(..., description="Priority of the task (low, medium, high)")

# Task logs
class TaskLog(BaseModel):
    timestamp: datetime
    message: str
    type: str = Field(..., description="Log type (info, warning, error)")

# Payload for Task
class TaskPayload(BaseModel):
    apiKey: Optional[str]
    endpointUrl: Optional[str]
    filePath: Optional[str]
    parameters: Optional[Dict[str, Any]]
    additionalConfig: Optional[Dict[str, Any]]

# Main Task Model
class Task(BaseModel):
    taskName: str
    taskDescription: str
    schedule: TaskSchedule
    status: TaskStatus
    metadata: TaskMetadata
    logs: List[TaskLog]
    payload: Optional[TaskPayload]
