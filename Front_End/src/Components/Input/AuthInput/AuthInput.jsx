import React from "react";
import "./AuthInput.css"; // Import the CSS file

// src/Components/Input/AuthInput/AuthInput.js
function AuthInput({ inputtype, placeholder, Icon, onChange, name, value }) {
  return (
    <div className="auth-input-container">
      <span className="auth-input-icon">{Icon && <Icon className="auth-icon" />}</span>
      <input
        type={inputtype}
        placeholder={placeholder}
        name={name}
        className="auth-input"
        onChange={onChange}  // ✅ Corrected to uppercase "C"
        value={value}
      />
    </div>
  );
}


export default AuthInput;
