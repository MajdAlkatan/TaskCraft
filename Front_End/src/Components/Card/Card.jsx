import React from "react";
import "./Card.css";
import { BsThreeDots } from "react-icons/bs"; // Settings icon

function Card({ title, description, priority, status, date, image, statusColor }) {
  const getStatusStyle = () => {
    switch (status.toLowerCase()) {
      case 'not started':
        return {
          color: 'red',
          borderColor: 'red',
        };
      case 'in progress':
        return { color: 'blue',
          borderColor: 'blue',
         };
      default:
        return { color: statusColor }; // Fallback to default color
    }
  };

  return (
    <div className="card-container" >
      <div className="card-left">
        <div className="card-circle" style={ getStatusStyle() }></div>
        <div className="card-content">
          <h2 className="card-title">{title}</h2>
          <p className="card-subtitle">{description}</p>
          <div className="card-meta">
            <span className="priority">Priority: {priority}</span>
            <span className="status" >Status: <h6 style={getStatusStyle()}>{status}</h6></span>
          </div>
          <p className="card-date"> {date}</p>
        </div>
      </div>

      <div className="card-right">
        <BsThreeDots className="settings-icon" />
        {image && <img src={image} alt="task" className="card-img" />}
      </div>
    </div>
  );
}

export default Card;