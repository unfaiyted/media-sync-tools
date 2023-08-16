import * as login from './modules/login';
import * as index from './modules/index';
import axios from "axios";
import {API_URL} from "@/utils/constants";
import * as clients from './clients';
import * as configs from './configs';

export default Object.assign({}, login, index, clients, configs);
export const apiClient = axios.create({
    baseURL: API_URL,
    timeout: 10000,  // Optional: timeout for requests
    // any other default configs you want
});

// Handle response errors centrally
apiClient.interceptors.response.use(
    response => response,
    error => {
        console.error("API error:", error);
        throw error;
    }
);

