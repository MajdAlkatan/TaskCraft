import React, { useState } from 'react';
import './ProjectLink.css';
import FormButton from '../../Components/Button/FormButton/FormButton';

const ProjectLink = () => {
    const [copied, setCopied] = useState(false);
    const link = 'https://sharealinkhereandthere.com/34565sy29';

    const copyToClipboard = () => {
        navigator.clipboard.writeText(link);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="project-link">
            <input className="project-link-input" value={link} readOnly />
            <FormButton label={copied ? "Copied!" : "Copy Link"} onClick={copyToClipboard} />
        </div>
    );
};

export default ProjectLink;
