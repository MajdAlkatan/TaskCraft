import React, { useState } from "react";
import "./Help.css"
import DefulteInput from "../../Components/Input/DefulteInput/DefulteInput";
const HelpSection = () => {
    const [activeSection, setActiveSection] = useState("faq");

    // Sample FAQs
    const faqs = [
        { question: "How do I create a new workspace?", answer: "Click on the 'Create Workspace' button in the dashboard and follow the prompts." },
        { question: "How do I add a new task?", answer: "Navigate to a workspace, click on 'Add Task,' and fill in the task details." },
        { question: "Can I change the permissions of a member?", answer: "Yes, go to the 'Members' tab, click on the member, and toggle their role between Viewer and Editor." },
    ];

    // Sample User Guide
    const userGuide = [
        "Step 1: Create a workspace to start managing tasks.",
        "Step 2: Add members to collaborate with.",
        "Step 3: Organize tasks into categories for better management.",
        "Step 4: Assign roles and permissions to your team members."
    ];

    // Sample Contact Form (for contacting support)
    const contactForm = (
        <form>
            <div>
                <label htmlFor="name">Your Name</label>
                <DefulteInput type="text" id="name" name="name" required />
            </div>
            <div>
                <label htmlFor="email">Your Email</label>
                <DefulteInput type="email" id="email" name="email" required />
            </div>
            <div className="message-textarea">
                <label htmlFor="message">Your Message</label>
                <textarea id="message" name="message" rows="4" required></textarea>
            </div>
            <button type="submit">Submit</button>
        </form>
    );

    return (
        <div className="help-section">
            <h1>Help Section</h1>

            {/* Navigation Links to Sections */}
            <div className="help-nav">
                <button onClick={() => setActiveSection("faq")}>FAQs</button>
                <button onClick={() => setActiveSection("guide")}>User Guide</button>
                <button onClick={() => setActiveSection("contact")}>Contact Support</button>
            </div>

            {/* Display Active Section */}
            {activeSection === "faq" && (
                <div className="faq-section">
                    <h2>Frequently Asked Questions</h2>
                    <ul>
                        {faqs.map((faq, index) => (
                            <li key={index}>
                                <strong>{faq.question}</strong>
                                <p>{faq.answer}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {activeSection === "guide" && (
                <div className="guide-section">
                    <h2>User Guide</h2>
                    <ol>
                        {userGuide.map((step, index) => (
                            <li key={index}>{step}</li>
                        ))}
                    </ol>
                </div>
            )}

            {activeSection === "contact" && (
                <div className="contact-section">
                    <h2>Contact Support</h2>
                    {contactForm}
                </div>
            )}
        </div>
    );
};

export default HelpSection;
