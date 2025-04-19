import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { FaChevronDown } from 'react-icons/fa';
import { fetchWorkspaces } from '../../store/reducers/workspaceListSlice'; // 👈
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
  const dispatch = useDispatch();
  const [isOpen, setIsOpen] = useState(false);

  const { workspaces, isLoading, error } = useSelector((state) => state.workspaceList);

  // Just an example — replace this with selected workspace from Redux or context later
  const currentWorkspace = workspaces?.[0]?.name || '...';

  useEffect(() => {
    dispatch(fetchWorkspaces());
  }, [dispatch]);

  return (
    <div className="dropdown-wrapper">
      <button className="dropdown-toggle" onClick={() => setIsOpen(!isOpen)}>
        Workspaces <FaChevronDown />
      </button>

      {isOpen && (
        <div className="dropdown-content">
          {isLoading && <p>Loading workspaces...</p>}
          {error && <p className="error-message">{error.detail}</p>}

          {!isLoading && !error && (
            <>
              <p className="section-title">Current Workspace</p>
              <WorkspaceItem name={currentWorkspace} active index={0} />

              <hr className="divider" />

              <p className="section-title">Your Workspaces</p>
              {workspaces.map((ws, index) => (
                <WorkspaceItem
                  key={ws.id}
                  name={ws.name}
                  index={index}
                  active={ws.name === currentWorkspace}
                />
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default WorkspaceDropdown;
