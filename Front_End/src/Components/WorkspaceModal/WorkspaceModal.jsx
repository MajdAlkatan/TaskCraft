import React, { useState } from "react";
import "./WorkspaceModal.css";
import { useDispatch, useSelector } from "react-redux";
import DefulteInput from "../Input/DefulteInput/DefulteInput";
import FormButton from "../Button/FormButton/FormButton";
import { createWorkspace } from "../../store/reducers/workspaceSlice";
import { fetchWorkspaces } from "../../store/reducers/workspaceListSlice"; // 👈

function WorkspaceModal({ onClose }) {
  const dispatch = useDispatch();
  const [workspaceName, setWorkspaceName] = useState("");
  const [workspaceImage, setWorkspaceImage] = useState(null);
  const { isLoading, error } = useSelector((state) => state.workspace);

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(createWorkspace({ name: workspaceName, image: workspaceImage }))
      .unwrap()
      .then(() => {
        dispatch(fetchWorkspaces()); // 👈 Refresh list right after creation
        onClose(); // Close modal on success
      })
      .catch((err) => {
        console.error("Failed to create workspace:", err);
      });
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Create New Workspace</h2>
        <form onSubmit={handleSubmit}>
          <DefulteInput
          className="modal-input"
            placeholder="TechCraft WorkSpace"
            label="Workspace Name"
            id="workspaceName"
            value={workspaceName}
            onChange={(e) => setWorkspaceName(e.target.value)}
            required
          />
          <DefulteInput
          className="modal-input"
            label="Workspace Image (optional)"
            id="workspaceImage"
            onChange={(e) => setWorkspaceImage(e.target.files[0])}
            isFileInput={true}
          />
          <FormButton type="submit" label={isLoading ? "Creating..." : "Create Workspace"} />
          <FormButton type="button" label="Cancel" onClick={onClose} />
          {error && <p className="error-message">{error.detail || "Something went wrong."}</p>}
        </form>
      </div>
    </div>
  );
}

export default WorkspaceModal;
