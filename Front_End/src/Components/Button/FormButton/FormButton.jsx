import React from "react";
import "./FormButton.css"
const FormButton = ({ label = "Click Me", onClick, className = "" ,type}) => {
  return (
    <button 
    type={type}
      onClick={onClick} 
      className={`btn ${className}`}
    >
      {label}
    </button>
  );
};

export default FormButton;
