// Interceptor -> intercepts any requests you are going 
// send. Automatically add headers

// Axios interceptor -> Check you have access

import axios from "axios";
import { ACCESS_TOKEN } from "./constants";
import { refreshAuth } from "./tokenManager";


const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL // From the .env file!
});

api.interceptors.request.use(
    (config) => { // request config
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}` // This is how you pass a JWT access token
        }
        return config;
    },
    (error) => {

        // If error calling API, check for refresh token:
        // If error, try to reauthenticate?
        return Promise.reject(error);
    }
)

// Solution for response interceptor by: https://medium.com/@velja/token-refresh-with-axios-interceptors-for-a-seamless-authentication-experience-854b06064bde
// This is to attempt to automatically refresh the access token

api.interceptors.response.use(
    (response) => { return response }, // Return response if no error
    async (error) => {
        const originalRequest = error.config // Retain original request to send again
        if (!error.response) {return Promise.reject(error);}
        else if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true; // The request has been retried, set to true
            try {
                // Attempt to refresh the authorization (refreshAuth() function will update local storage)
                console.log("SENDING REQUEST (api.ts)");
                const accessToken = await refreshAuth();
                if (accessToken !== null) {
                    // api.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
                    return api(originalRequest); // Send original request again
                } else {
                    window.location.href = '/login'
                    return Promise.reject("ERROR in REFRESH TOKEN");
                }
            } catch (error) {
                console.log("ERROR!")
                console.log(error);
                window.location.href = '/login'; // Go back to login page
                return Promise.reject(error);
            }
        } else {
            return Promise.reject("Failed at re-authentication.");
        }
    }
)


export default api; // Export the api object
