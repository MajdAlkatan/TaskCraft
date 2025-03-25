import React from "react";
import "./AuthInput.css"; // Import the CSS file

function AuthInput({ inputtype, placeholder, Icon }) {
  return (
    <div className="auth-input-container">
      <span className="auth-input-icon">{Icon && <Icon className="icon" />}</span>
      <input
        type={inputtype}
        placeholder={placeholder}
        className="auth-input"
      />
    </div>
  );
}

export default AuthInput;
