import { useState, useEffect } from 'react';

const useUserData = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const user = localStorage.getItem('user_data');
        
        if (token && user) {
            try {
                const parsedUser = JSON.parse(user);
                setUserData(parsedUser);
            } catch (error) {
                console.error('Error parsing user data:', error);
            }
        }
    }, []);

    return userData;
};

export default useUserData;
