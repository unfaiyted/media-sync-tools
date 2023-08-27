// ScheduleType.ts
export enum ScheduleType {
    INTERVAL = 'interval',
    CRON = 'cron',
    DATE = 'date'
}

// TaskState.ts
export enum TaskState {
    RUNNING = 'running',
    PAUSED = 'paused',
    FAILED = 'failed',
    CANCELLED = 'cancelled',
    CREATED = 'created',
    COMPLETED = 'completed',
    // Add other states as necessary
}

// TaskPriority.ts
export enum TaskPriority {
    LOW = 'low',
    MEDIUM = 'medium',
    HIGH = 'high'
}

// LogType.ts
export enum LogType {
    INFO = 'info',
    WARNING = 'warning',
    ERROR = 'error'
}

// TaskSchedule.ts
export interface TaskSchedule {
    type: ScheduleType;
    details: Record<string, string | number>;
    timeZone?: string;
}

// TaskStatus.ts
export interface TaskStatus {
    lastRunTime?: Date;
    nextRunTime: Date;
    state: TaskState;
    error?: string;
}

// TaskMetadata.ts
export interface TaskMetadata {
    createdBy: string;
    createdOn: Date;
    lastModified: Date;
    tags?: string[];
    priority: TaskPriority;
}

// TaskLog.ts
export interface TaskLog {
    timestamp: Date;
    message: string;
    type: LogType;
}


// TaskPayload.ts
export interface TaskPayload {
    apiKey?: string;
    endpointUrl?: string;
    filePath?: string;
    parameters?: Record<string, any>;
    additionalConfig?: Record<string, any>;
}

// Task.ts
export interface Task {
    taskName: string;
    taskId: string;
    taskDescription: string;
    schedule: TaskSchedule;
    status: TaskStatus;
    metadata: TaskMetadata;
    logs: TaskLog[];
    payload?: TaskPayload;
}
