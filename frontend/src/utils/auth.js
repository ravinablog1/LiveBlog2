// Importing the useAuthStore hook from the '../store/auth' file to manage authentication state
import { useAuthStore } from "../store/auth";

// Importing the axios library for making HTTP requests
import axios from "./axios";

// Importing jwt_decode to decode JSON Web Tokens
import jwt_decode from "jwt-decode";

// Importing the Cookies library to handle browser cookies
import Cookies from "js-cookie";

// Importing Swal (SweetAlert2) for displaying toast notifications
import Swal from "sweetalert2";

// Configuring global toast notifications using Swal.mixin
const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 1500,
    timerProgressBar: true,
});

// Function to handle user login
export const login = async (email, password) => {
    try {
        console.log("Making login request to:", "users/login/");
        console.log("Request data:", { username: email, password: "***" });
        
        // Making a POST request to the correct login endpoint
        const { data, status } = await axios.post("users/login/", {
            username: email, // Backend expects username field
            password,
        });

        console.log("Login API response:", { data, status });

        // If the request is successful (status code 200), set authentication user and display success toast
        if (status === 200) {
            setAuthUser(data.access, data.refresh);

            // Dispatch custom event to notify Header component
            window.dispatchEvent(new Event('userLoggedIn'));

            // Displaying a success toast notification
            Toast.fire({
                icon: "success",
                title: "Signed in successfully",
            });
        }

        // Returning data and error information
        return { data, error: null };
    } catch (error) {
        console.error("Login API error:", error);
        console.error("Error response:", error.response?.data);
        
        // Handling errors and returning data and error information
        return {
            data: null,
            error: error.response?.data?.detail || 
                   error.response?.data?.error || 
                   (typeof error.response?.data === 'string' ? error.response.data : "Something went wrong"),
        };
    }
};

// Function to handle user registration
export const register = async (full_name, email, password, password2) => {
    try {
        // Making a POST request to register a new user
        const { data } = await axios.post("user/register/", {
            full_name,
            email,
            password,
            password2,
        });

        // Logging in the newly registered user and displaying success toast
        await login(email, password);

        // Displaying a success toast notification
        Toast.fire({
            icon: "success",
            title: "Signed Up Successfully",
        });

        // Returning data and error information
        return { data, error: null };
    } catch (error) {
        // Handling errors and returning data and error information
        return {
            data: null,
            error: error.response.data || "Something went wrong",
        };
    }
};

// Function to handle user logout
export const logout = () => {
    // Removing access and refresh tokens from cookies
    Cookies.remove("access_token");
    Cookies.remove("refresh_token");
    
    // Also remove from localStorage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    
    // Reset user state
    useAuthStore.getState().setUser(null);

    // Displaying a success toast notification
    Toast.fire({
        icon: "success",
        title: "You have been logged out.",
    });
};

// Function to set the authenticated user on page load
export const setUser = async () => {
    // Retrieving access and refresh tokens from cookies
    const accessToken = Cookies.get("access_token");
    const refreshToken = Cookies.get("refresh_token");

    // Checking if tokens are present
    if (!accessToken || !refreshToken) {
        return;
    }

    // If access token is expired, refresh it; otherwise, set the authenticated user
    if (isAccessTokenExpired(accessToken)) {
        const response = await getRefreshToken(refreshToken);
        setAuthUser(response.access, response.refresh);
    } else {
        setAuthUser(accessToken, refreshToken);
    }
};

// Function to set the authenticated user and update user state
export const setAuthUser = (access_token, refresh_token) => {
    // Setting access and refresh tokens in cookies with expiration dates
    Cookies.set("access_token", access_token, {
        expires: 1, // Access token expires in 1 day
        secure: true,
    });

    Cookies.set("refresh_token", refresh_token, {
        expires: 7, // Refresh token expires in 7 days
        secure: true,
    });

    // Also store in localStorage for Header component
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);

    // Decoding access token to get user information
    const user = jwt_decode(access_token) ?? null;

    // If user information is present, update user state; otherwise, set loading state to false
    if (user) {
        useAuthStore.getState().setUser(user);
        // Also store user in localStorage
        localStorage.setItem("user", JSON.stringify(user));
    }
    useAuthStore.getState().setLoading(false);
};

// Function to refresh the access token using the refresh token
export const getRefreshToken = async () => {
    // Retrieving refresh token from cookies and making a POST request to refresh the access token
    const refresh_token = Cookies.get("refresh_token");
    const response = await axios.post("users/token/refresh/", {
        refresh: refresh_token,
    });

    // Returning the refreshed access token
    return response.data;
};

// Function to check if the access token is expired
export const isAccessTokenExpired = (accessToken) => {
    try {
        // Decoding the access token and checking if it has expired
        const decodedToken = jwt_decode(accessToken);
        return decodedToken.exp < Date.now() / 1000;
    } catch (err) {
        // Returning true if the token is invalid or expired
        return true;
    }
};
