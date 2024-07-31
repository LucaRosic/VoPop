// Interceptor -> intercepts any requests you are going 
// send. Automatically add headers

// Axios interceptor -> Check you have access

import axios from "axios";
import { ACCESS_TOKEN } from "./constants";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL // From the .env file!
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}` // This is how you pass a JWT access token
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
)

export default api; // Export the api object
