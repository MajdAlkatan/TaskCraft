import React from "react";
import "./Sidebar.css";
import { FaTachometerAlt, FaTasks, FaList, FaCog, FaQuestionCircle, FaSignOutAlt } from "react-icons/fa";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="profile">
        <img src="https://via.placeholder.com/0" alt="Profile" className="profile-img" />
        <h3>Sundar Gurung</h3>
        <p>sundargurung360@gmail.com</p>
      </div>

      <nav className="menu">
        <a href="#" className="active"><FaTachometerAlt className="icon" /> Dashboard</a>
        <a href="#"><FaTasks className="icon" /> Vital Task</a>
        <a href="#"><FaList className="icon" /> My Task</a>
        <a href="#"><FaList className="icon" /> Task Categories</a>
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
