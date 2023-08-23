import { Task, TaskPayload } from "@/models";  // Assume you have defined these models.
import { apiClient } from "@/api/index";

export const createTask = async (task: Task): Promise<Task> => {
    const response = await apiClient.post('/tasks/', task);
    return response.data;
}

export const fetchAllTasks = async (): Promise<Task[]> => {
    const response = await apiClient.get('/tasks/all');
    return response.data;
}

export const fetchTaskById = async (taskId: string): Promise<Task> => {
    const response = await apiClient.get(`/tasks/${taskId}`);
    return response.data;
};

export const updateTask = async (taskId: string, task: Task): Promise<Task> => {
    const response = await apiClient.put(`/tasks/${taskId}`, task);
    return response.data;
}

export const deleteTask = async (taskId: string): Promise<void> => {
    await apiClient.delete(`/tasks/${taskId}`);
}

export const triggerTaskOnDemand = async (taskId: string): Promise<{ status: string, message: string }> => {
    const response = await apiClient.post(`/tasks/${taskId}/trigger`);
    return response.data;
}

// If you have other task-related functionalities or specialized tasks, you can continue to add them here.
