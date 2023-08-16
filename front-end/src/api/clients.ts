import axios from "axios";
import {Client, ClientField, ConfigClientFieldsValue} from "@/models";
import { generateGuid } from "@/utils/numbers";
import {apiClient} from "@/api/index";


export const fetchClients = async () => {
    return (await apiClient.get('/client/')).data;
}

export const createClient = async (client: Client) => {
    client.clientId = generateGuid();
    return await apiClient.post('/client', client);
}

export const deleteClient = async (clientId: string) => {
    return await apiClient.delete(`/client/${clientId}`);
}

export const updateClient = async (updatedClient: Client) => {
    return await apiClient.put(`/client/${updatedClient.clientId}`, updatedClient);
}
// ... other imports

export const createClientField = async (clientField: ClientField) => {
    clientField.clientFieldId = generateGuid();
    console.log("clientField", clientField);
    return await apiClient.post('/client/field/', clientField);
}

export const fetchClientField = async (clientFieldId: string) => {
    return (await apiClient.get(`/client/field/${clientFieldId}`)).data;
}

export const fetchClientFieldByClientId = async (clientId: string | undefined) => {
    if(!clientId) {
        console.error("Client ID is blank");
        return;
    }
    return (await apiClient.get(`/client/field/client/${clientId}`)).data;
}

export const updateClientField = async (updatedClientField: ClientField) => {
    return (await apiClient.put(`/client/field/${updatedClientField.clientFieldId}`, updatedClientField)).data;
}

export const deleteClientField = async (clientFieldId: string | undefined) => {
      if (!clientFieldId) {
                console.error("Client Field Id blank", clientFieldId );
                return;
      }
    return await apiClient.delete(`/client/field/${clientFieldId}`);
}

export const updateConfigClientFieldsValue = async (data: ConfigClientFieldsValue): Promise<ConfigClientFieldsValue> => {
    if (data.configClientFieldsId) {
        const response = await apiClient.put(`/config/client-fields-value/${data.configClientFieldsId}`, data);
        return response.data;
    } else {
        const response = await apiClient.post('/config/client-fields-value/', data);
        return response.data;
    }
}
