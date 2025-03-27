import React from "react";
import "./DefulteInput.css"
const DefulteInput = ({
  label,
  id,
  type = "text",
  value,
  onChange,
  placeholder = "",
  className = ""
}) => {
  return (
    <div className="input-container">
      {label && <label htmlFor={id} className="input-label">{label}</label>}
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className={`input-field ${className}`}
      />
    </div>
  );
};

export default DefulteInput;
