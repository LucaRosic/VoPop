// A wrapper for a protected route.
// Need to have an authorization token before we are able
// to access this route.

import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants";
import { ReactNode, useEffect, useState } from "react";


interface Props {
    children: ReactNode; // React element as child
  }

function ProtectedRoute({children} : Props) {
    const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false));
    }, [])

    const refreshToken = async () => {
        // Get refresh token
        const refreshToken = localStorage.getItem(REFRESH_TOKEN)
        // After getting refresh token, TRY to send that token to the refresh api endpoint
        try {
            // Sending refresh (refreshToken) payload to this api end point (dont forget trailing slash)
            // Base URL is already handled (base url for Django server)
            console.log("Protected Route Refresh Token!")
            const res = await api.post("/api/token/refresh/", {refresh: refreshToken}); // Get response on POST request
            if (res.status === 200) { // Response was success
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    }

    const auth = async () => {
        // Check if we have an authorization token
        // If we have one check if it expired or not
        // If it is expired, get a new one with the refresh token
        // If we cannot refresh, user needs to get re-authorized

        const token = localStorage.getItem(ACCESS_TOKEN); // localStorage is the local storage within users web browser
        if (!token) {
            setIsAuthorized(false); // Set authorization to false
            return;
        }
        const decoded = jwtDecode(token); // Decode token
        const tokenExpiration = decoded.exp;
        const now = Date.now() / 1000 // Divide by 1000 to get time in seconds (not in miliseconds)

        if (tokenExpiration === undefined || tokenExpiration < now) {
            // Token has expired
            await refreshToken();
        } else {
            setIsAuthorized(true);
        }
    }

    if (isAuthorized === null) {
        return <div>Loading...</div>
    }

    // If authorized, return children else navigate back to login
    return isAuthorized ? children : <Navigate to="/login"/>


}

export default ProtectedRoute;