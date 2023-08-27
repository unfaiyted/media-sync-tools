import { defineStore } from 'pinia';
import { Task } from "@/models";
import * as TaskAPI from "@/api/tasks";  // Assuming the file you provided above is named `taskAPI.ts`

export const useTaskStore = defineStore({
    id: 'tasks',
    state: () => ({
        tasks: [] as Task[],
        selectedTask: null as Task | null,
    }),
    actions: {
        async fetchAllTasks() {
            this.tasks = await TaskAPI.fetchAllTasks();
        },
        async fetchTaskById(taskId: string) {
            this.selectedTask = await TaskAPI.fetchTaskById(taskId);
        },
        async createTask(task: Task): Promise<Task> {
            const newTask = await TaskAPI.createTask(task);
            this.tasks.push(newTask);
            return newTask;
        },
        async updateTask(taskId: string, task: Task) {
            const updatedTask = await TaskAPI.updateTask(taskId, task);
            const index = this.tasks.findIndex(t => t.taskName === taskId);  // Assuming `taskName` is a unique identifier.
            if (index !== -1) {
                this.tasks[index] = updatedTask;
            }
        },
        async deleteTask(taskId: string) {
            await TaskAPI.deleteTask(taskId);
            this.tasks = this.tasks.filter(task => task.taskName !== taskId);  // Remove the task from state.
        },
        async triggerTaskOnDemand(taskId: string) {
            const result = await TaskAPI.triggerTaskOnDemand(taskId);
            console.log(result.message);  // Handle or show feedback accordingly.
        },
    },
});
