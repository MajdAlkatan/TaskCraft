import React from "react";
import { useNavigate } from "react-router-dom";
import "./Sidebar.css";
import { FaTachometerAlt, FaTasks, FaList, FaCog, FaQuestionCircle, FaSignOutAlt } from "react-icons/fa";

function Sidebar() {
  const navigate = useNavigate(); // Initialize navigation function

  return (
    <aside className="sidebar">
      <div className="profile">
        <img src="https://via.placeholder.com/40" alt="Profile" className="profile-img" />
        <h3>Sundar Gurung</h3>
        <p>sundargurung360@gmail.com</p>
      </div>

      <nav className="menu">
        <a href="#" onClick={() => navigate("/")}><FaTachometerAlt className="icon" /> Dashboard</a>
        <a href="#" onClick={() => navigate("/mytask")}><FaList className="icon" /> My Task</a>
        <a href="#"><FaCog className="icon" /> Settings</a>
        <a href="#"><FaQuestionCircle className="icon" /> Help</a>
      </nav>

      <div className="logout">
        <a href="#"><FaSignOutAlt className="icon" /> Logout</a>
      </div>
    </aside>
  );
}

export default Sidebar;
