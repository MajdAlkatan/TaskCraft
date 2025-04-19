import React, { useState } from 'react';
import { FaChevronDown } from 'react-icons/fa';
import './WorkspaceDropdown.css';

const WorkspaceItem = ({ name, active, index }) => {
  const firstLetter = name.trim().charAt(0).toUpperCase();
  const colorVar = `var(--workspace-color-${(index % 10) + 1})`;

  return (
    <div className={`workspace-item ${active ? 'active' : ''}`}>
      <div className="workspace-icon" style={{ backgroundColor: colorVar }}>
        {firstLetter}
      </div>
      <span>{name}</span>
    </div>
  );
};

const WorkspaceDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const currentWorkspace = 'Tech Craft';
  const workspaces = ['TechLeads', 'Tech Craft', 'Majd WorkSpace ','Ali Workspace'];

  return (
    <div className="dropdown-wrapper">
      <button className="dropdown-toggle" onClick={() => setIsOpen(!isOpen)}>
        Workspaces <FaChevronDown />
      </button>

      {isOpen && (
        <div className="dropdown-content">
          <p className="section-title">Current Workspace</p>
          <WorkspaceItem name={currentWorkspace} active index={0} />

          <hr className="divider" />

          <p className="section-title">Your Workspaces</p>
          {workspaces.map((name, index) => (
            <WorkspaceItem
              key={name}
              name={name}
              index={index}
              active={name === currentWorkspace}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default WorkspaceDropdown;
