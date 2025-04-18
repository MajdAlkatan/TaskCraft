import React from "react";
import "./AuthButton.css"; // Import the CSS file

function AuthButton({ text, onClick, type = "button", disabled }) {
  return (
    <button className="auth-button" onClick={onClick} type={type} disabled={disabled}>
      {text}
    </button>
  );
}

export default AuthButton;
