import React from "react";
import "./AuthButton.css"; // Import the CSS file

function AuthButton({ text, onClick }) {
  return (
    <button className="auth-button" onClick={onClick}>
      {text}
    </button>
  );
}

export default AuthButton;
