import React from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";

function Contact() {
    return (
        <>
            <Header />
            <section className="mt-5">
                <div className="container">
                    <div className="row">
                        <div className="col-md-9 mx-auto text-center">
                            <h1 className="fw-bold">Contact us</h1>
                        </div>
                    </div>
                </div>
            </section>
            {/* =======================
Inner intro END */}
            {/* =======================
Contact info START */}
            <section className="pt-4">
                <div className="container">
                    <div className="row">
                        <div className="col-xl-9 mx-auto">
                            <iframe
                                className="w-100 h-300 grayscale"
                                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.9663095343008!2d-74.00425878428698!3d40.74076684379132!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259bf5c1654f3%3A0xc80f9cfce5383d5d!2sGoogle!5e0!3m2!1sen!2sin!4v1586000412513!5m2!1sen!2sin"
                                height={500}
                                style={{ border: 0 }}
                                aria-hidden="false"
                                tabIndex={0}
                            />
                            <div className="row mt-5">
                                <div className="col-sm-6 mb-5 mb-sm-0">
                                    <h3>Technical Support</h3>
                                    <address>LiveBlog Development Team<br/>
                                    Tech Innovation Hub<br/>
                                    123 Developer Street, Suite 456<br/>
                                    San Francisco, CA 94105</address>
                                    <p>
                                        Technical Support:{" "}
                                        <a href="tel:+1-555-TECH-HELP" className="text-reset">
                                            <u>+1 (555) TECH-HELP</u>
                                        </a>
                                    </p>
                                    <p>
                                        Email Support:{" "}
                                        <a href="mailto:support@liveblog.dev" className="text-reset">
                                            <u>support@liveblog.dev</u>
                                        </a>
                                    </p>
                                    <p>
                                        Bug Reports:{" "}
                                        <a href="mailto:bugs@liveblog.dev" className="text-reset">
                                            <u>bugs@liveblog.dev</u>
                                        </a>
                                    </p>
                                    <p>
                                        Support Hours: Monday to Friday
                                        <br />
                                        9:00 AM to 6:00 PM PST
                                        <br />
                                        <small className="text-muted">Response time: Within 24 hours</small>
                                    </p>
                                </div>
                                <div className="col-sm-6">
                                    <h3>Business & Partnerships</h3>
                                    <p>Interested in enterprise solutions, API access, or partnership opportunities? Get in touch with our business development team.</p>
                                    <address>LiveBlog Business Division<br/>
                                    Media Innovation Center<br/>
                                    789 Business Plaza, Floor 12<br/>
                                    New York, NY 10001</address>
                                    <p>
                                        Business Inquiries:{" "}
                                        <a href="tel:+1-555-BIZ-LIVE" className="text-reset">
                                            <u>+1 (555) BIZ-LIVE</u>
                                        </a>
                                    </p>
                                    <p>
                                        Partnership Email:{" "}
                                        <a href="mailto:partnerships@liveblog.dev" className="text-reset">
                                            <u>partnerships@liveblog.dev</u>
                                        </a>
                                    </p>
                                    <p>
                                        Enterprise Sales:{" "}
                                        <a href="mailto:enterprise@liveblog.dev" className="text-reset">
                                            <u>enterprise@liveblog.dev</u>
                                        </a>
                                    </p>
                                    <p>
                                        Business Hours: Monday to Friday
                                        <br />
                                        8:00 AM to 7:00 PM EST
                                        <br />
                                        <small className="text-muted">Custom solutions available</small>
                                    </p>
                                </div>
                            </div>
                            <hr className="my-5" />
                            <div className="row mb-5">
                                <div className="col-12">
                                    <h2 className="fw-bold">Get in Touch</h2>
                                    <p>Have questions about LiveBlog? Need help getting started? Want to report a bug or suggest a feature? We'd love to hear from you!</p>
                                    {/* Form START */}
                                    <form className="contact-form" id="contact-form" name="contactform" method="POST">
                                        {/* Main form */}
                                        <div className="row">
                                            <div className="col-md-6">
                                                {/* name */}
                                                <div className="mb-3">
                                                    <input required="" id="con-name" name="name" type="text" className="form-control" placeholder="Your Name" />
                                                </div>
                                            </div>
                                            <div className="col-md-6">
                                                {/* email */}
                                                <div className="mb-3">
                                                    <input required="" id="con-email" name="email" type="email" className="form-control" placeholder="Your Email" />
                                                </div>
                                            </div>
                                            <div className="col-md-12">
                                                {/* Subject */}
                                                <div className="mb-3">
                                                    <select required="" id="con-subject" name="subject" className="form-control">
                                                        <option value="">Select Subject</option>
                                                        <option value="technical-support">Technical Support</option>
                                                        <option value="bug-report">Bug Report</option>
                                                        <option value="feature-request">Feature Request</option>
                                                        <option value="business-inquiry">Business Inquiry</option>
                                                        <option value="partnership">Partnership Opportunity</option>
                                                        <option value="general">General Question</option>
                                                    </select>
                                                </div>
                                            </div>
                                            <div className="col-md-12">
                                                {/* Message */}
                                                <div className="mb-3">
                                                    <textarea 
                                                        required="" 
                                                        id="con-message" 
                                                        name="message" 
                                                        cols={40} 
                                                        rows={6} 
                                                        className="form-control" 
                                                        placeholder="Tell us about your question, issue, or how we can help you with LiveBlog..." 
                                                        defaultValue={""} 
                                                    />
                                                </div>
                                            </div>
                                            {/* submit button */}
                                            <div className="col-md-12 text-start">
                                                <button className="btn btn-primary w-100" type="submit">
                                                    Send Message <i className="fas fa-paper-plane"></i>
                                                </button>
                                                <small className="text-muted mt-2 d-block">
                                                    We typically respond within 24 hours during business days
                                                </small>
                                            </div>
                                        </div>
                                    </form>
                                    {/* Form END */}
                                    
                                    {/* Additional Help Section */}
                                    <div className="mt-5 p-4 bg-light rounded">
                                        <h4>Quick Help Resources</h4>
                                        <div className="row">
                                            <div className="col-md-4">
                                                <h6><i className="fas fa-book text-primary me-2"></i>Documentation</h6>
                                                <p className="small">Check our comprehensive guides and API documentation</p>
                                            </div>
                                            <div className="col-md-4">
                                                <h6><i className="fas fa-video text-success me-2"></i>Video Tutorials</h6>
                                                <p className="small">Watch step-by-step tutorials on using LiveBlog features</p>
                                            </div>
                                            <div className="col-md-4">
                                                <h6><i className="fas fa-comments text-info me-2"></i>Community Forum</h6>
                                                <p className="small">Connect with other LiveBlog users and developers</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>{" "}
                        {/* Col END */}
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Contact;
