import api from "./api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants"

export const refreshAuth = async () => {
    /*
        Function to get another ACCESS TOKEN using a REFRESH TOKEN. 

        Returns:
            (bool): Boolean signifying successful or unsuccessful attempt at getting access token

    */


    // Get the refresh token:
    const refreshToken = localStorage.getItem(REFRESH_TOKEN);

    // After getting refresh token, TRY to send token to the refresh API endpoint to reauthenticate
    console.log("SENDING REFRESH");
    const res = await api.post("/api/token/refresh/", {refresh: refreshToken});
    if (res.status === 200) { // Response was a success
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        return res.data.access; // Successful authentication 
    } else {
        localStorage.clear();
        return null; // Unsucessful authentication
    }

}


