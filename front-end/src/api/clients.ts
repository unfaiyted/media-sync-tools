import axios from "axios";
import {Client, ClientField, ConfigClientFieldsValue, FilterTypes} from "@/models";
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
    if (data.configClientFieldValueId) {
        const response = await apiClient.put(`/config/client-fields-value/${data.configClientFieldId}`, data);
        return response.data;
    } else {
        const response = await apiClient.post('/config/client-fields-value/', data);
        return response.data;
    }
}

export const createFilterType = async (filterType: FilterTypes): Promise<FilterTypes> => {
    filterType.filterTypeId = generateGuid();
    const response = await apiClient.post('/client/filter/', filterType);
    return response.data;
}

export const fetchFilterTypes = async (clientId: string): Promise<FilterTypes[]> => {
    const response = await apiClient.get(`/client/filter/client/${clientId}`);
    return response.data;
}

export const updateFilterType = async (updatedFilterType: FilterTypes): Promise<FilterTypes> => {
    const response = await apiClient.put(`/client/filter/${updatedFilterType.filterTypeId}`, updatedFilterType);
    return response.data;
}

export const deleteFilterType = async (filterTypeId: string): Promise<void> => {
    await apiClient.delete(`/client/filter/${filterTypeId}`);
}
