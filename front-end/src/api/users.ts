import axios from "axios";
import {Config, ConfigClient, User} from "@/models";
import { generateGuid } from "@/utils/numbers";
import {apiClient} from "@/api/index";


export const createUser = async (user: User) => {
    if (!user.userId) {
        user.userId = generateGuid();
    }

    return await apiClient.post('/user/', user);
}

export const fetchUser = async (userId: string) => {
    return await apiClient.get(`/user/${userId}`);
}

export const fetchUsers = async () => {
    return (await apiClient.get(`/user/`)).data;
}

export const updateUser = async (updatedUser: User) => {
    return await apiClient.put(`/user/${updatedUser.userId}`, updatedUser);
}

export const deleteUser = async (userClientId: string | undefined) => {
    if(!userClientId) {
        console.error("Config ID is blank");
        return;
    }
    return await apiClient.delete(`/user/${userClientId}`);
}

