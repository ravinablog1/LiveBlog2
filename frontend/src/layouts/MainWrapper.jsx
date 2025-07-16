import React from 'react';
import '../styles/main.css';

function MainWrapper({ children }) {
    return (
        <div className="main-wrapper">
            {children}
        </div>
    );
}

export default MainWrapper;
