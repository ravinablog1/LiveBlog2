import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiInstance from "../../utils/axios";

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        const handleLogout = async () => {
            try {
                // Get refresh token before clearing storage
                const refreshToken = localStorage.getItem("refresh_token");
                
                // Call logout API if refresh token exists
                if (refreshToken) {
                    try {
                        await apiInstance.post("/users/logout/", {
                            refresh: refreshToken
                        });
                    } catch (error) {
                        console.log("Logout API call failed:", error);
                        // Continue with local logout even if API fails
                    }
                }
                
                // Clear all authentication data from localStorage
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                localStorage.removeItem("user");
                
                // Clear any other user-related data
                localStorage.clear();
                
                // Show success message (optional)
                console.log("Logged out successfully");
                
                // Redirect to home page
                navigate("/", { replace: true });
                
            } catch (error) {
                console.error("Logout error:", error);
                // Even if there's an error, clear local storage and redirect
                localStorage.clear();
                navigate("/", { replace: true });
            }
        };

        handleLogout();
    }, [navigate]);

    return (
        <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh',
            flexDirection: 'column'
        }}>
            <div className="spinner"></div>
            <p style={{ marginTop: '1rem' }}>Logging out...</p>
        </div>
    );
}

export default Logout;
