import React from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";

function About() {
    return (
        <>
            <Header />
            {/* Hero Section */}
            <section className="mt-5">
                <div className="container">
                    <div className="row">
                        <div className="col-md-9 mx-auto text-center">
                            <h1 className="fw-bold">About LiveBlog</h1>
                            <p className="lead">
                                Discover the story behind our innovative blogging platform
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Main Content */}
            <section className="pt-4 pb-5">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-9 mx-auto">
                            <h2>About LiveBlog Platform</h2>
                            <p className="lead">
                                LiveBlog is a cutting-edge real-time blogging platform designed for modern journalists, content creators, 
                                and organizations who need to deliver breaking news and live event coverage with instant updates and 
                                seamless audience engagement.
                            </p>
                            
                            <div className="row mt-5">
                                <div className="col-md-6">
                                    <h3>Our Mission</h3>
                                    <p>
                                        To empower content creators with the tools they need to share their stories in real-time, 
                                        fostering meaningful connections between writers and readers in an increasingly digital world.
                                    </p>
                                    
                                    <h3>Key Features</h3>
                                    <ul>
                                        <li>Real-time content publishing</li>
                                        <li>Interactive comment system</li>
                                        <li>Mobile-responsive design</li>
                                        <li>SEO optimization</li>
                                        <li>Social media integration</li>
                                    </ul>
                                </div>
                                <div className="col-md-6">
                                    <h3>Our Story</h3>
                                    <p>
                                        Founded in 2024, LiveBlog emerged from the need for a more dynamic and engaging 
                                        blogging experience. Our team of developers and content strategists recognized 
                                        the gap between traditional blogging platforms and the fast-paced digital landscape.
                                    </p>
                                    
                                    <h3>Technology Stack</h3>
                                    <p>
                                        Built with modern technologies including React for the frontend and Django for 
                                        the backend, LiveBlog ensures optimal performance, security, and scalability.
                                    </p>
                                </div>
                            </div>
                            
                            <div className="mt-5 p-4 bg-light rounded">
                                <h4>Join Our Community</h4>
                                <p>
                                    Whether you're a seasoned blogger or just starting your writing journey, 
                                    LiveBlog provides the perfect platform to share your voice with the world.
                                </p>
                                <div className="d-flex gap-3">
                                    <a href="/register/" className="btn btn-primary">
                                        Get Started
                                    </a>
                                    <a href="/contact/" className="btn btn-outline-primary">
                                        Contact Us
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default About;
