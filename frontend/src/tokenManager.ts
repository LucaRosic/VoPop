import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants"
import { jwtDecode } from "jwt-decode";

export const refreshAuth = async () => {
    /*
        Function to get another ACCESS TOKEN using a REFRESH TOKEN. 

        Returns:
            (bool): Boolean signifying successful or unsuccessful attempt at getting access token

    */


    // Get the refresh token:
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);

    // After getting refresh token, TRY to send token to the refresh API endpoint to reauthenticate
    
    // This must not be with api defined before (axios interceptors cause infinite loop), this must be with normal axios request
    try {
        console.log("SENDING REFRESH");
        const config = {
            headers: {
                'Content-Type' : `application/json`
            }
        }
        const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {refresh:refreshToken}, config);
        console.log(`API URL: ${import.meta.env.VITE_API_URL}`);
        // const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {refresh: refreshToken});

        console.log(`STATUS OBTAINED: ${res.status}`);
        if (res.status === 200) { // Response was a success
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            return res.data.access; // Successful authentication 
        } else {
            return null; // Unsucessful authentication
        }
    } catch (error) {
        console.log("Error for REFRESH API it seems...");
        console.log(error);
        return null;
    }
    

}

// First check if user is alreay logged in
export const isLoggedIn = async () => {

    await refreshAuth(); // Get token refreshed

    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) {
        // No token exists
        console.log("TOKEN DOES NOT EXIST")
        return false;
    }

    // Check if authenticated
    const decoded = jwtDecode(token);
    const tokenExpiration = decoded.exp;
    const now = Date.now() / 1000; // Divide by 1000 to get time in seconds
    if (tokenExpiration === undefined || tokenExpiration < now) {
        console.log("TOKEN EXPIRED")
        // Try
        return false;
    } else {
        console.log("TOKEN STILL VALID");
        return true;
    }
}


