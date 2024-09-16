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
    
    try {
        console.log("SENDING REFRESH");
        
        // Send request to refresh access token
        const res = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {refresh:refreshToken});
        
        console.log(`API URL: ${import.meta.env.VITE_API_URL}`);
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

export const isLoggedIn = async () => {
    /*
        Function to check if user is already logged in 

        Returns:
            (bool): Boolean signifying whether use is logged in or not

    */

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


