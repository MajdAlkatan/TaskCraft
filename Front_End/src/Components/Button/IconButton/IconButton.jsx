import React from "react";
import PropTypes from "prop-types";
import "./IconButton.css"; // Optional: Add styles if needed

function IconButton({ icon: Icon, onClick }) {
  return (
    <button className="icon-button" onClick={onClick}>
      {Icon ? <Icon className="icon" /> : null} 
    </button>
  );
}

// Prop validation
IconButton.propTypes = {
  icon: PropTypes.elementType.isRequired, // Ensure the icon is a valid React component
  onClick: PropTypes.func,
};

export default IconButton;
