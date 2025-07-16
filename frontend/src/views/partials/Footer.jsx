import React from "react";
import { Link } from "react-router-dom";

function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <div className="row">
                    <div className="col-md-6">
                        <h4>Django React Blog</h4>
                        <p>A modern blog platform built with Django and React.</p>
                    </div>
                    <div className="col-md-6">
                        <h4>Quick Links</h4>
                        <ul style={{ listStyle: "none", padding: 0 }}>
                            <li><Link to="/" style={{ color: "#fff", textDecoration: "none" }}>Home</Link></li>
                            <li><Link to="/about/" style={{ color: "#fff", textDecoration: "none" }}>About</Link></li>
                            <li><Link to="/contact/" style={{ color: "#fff", textDecoration: "none" }}>Contact</Link></li>
                        </ul>
                    </div>
                </div>
                <div className="text-center" style={{ marginTop: "2rem", borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: "1rem" }}>
                    <p>&copy; {new Date().getFullYear()} Django React Blog. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
