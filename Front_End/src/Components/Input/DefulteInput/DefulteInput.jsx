import React from "react";
import "./DefulteInput.css";

const DefulteInput = ({
  label,
  id,
  type = "text",
  value,
  onChange,
  placeholder = "",
  className = "",
  isFileInput = false, // New prop to handle file input
}) => {
  return (
    <div className="input-container">
      {label && <label htmlFor={id} className="input-label">{label}</label>}
      <input
        id={id}
        type={isFileInput ? "file" : type} // Use file input if isFileInput is true
        value={isFileInput ? undefined : value} // Prevent value for file input
        onChange={onChange}
        placeholder={placeholder}
        className={`input-field ${className}`}
      />
    </div>
  );
};

export default DefulteInput;