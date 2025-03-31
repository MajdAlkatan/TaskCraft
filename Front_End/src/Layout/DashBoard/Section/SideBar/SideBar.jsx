import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Sidebar.css";
import { FaTachometerAlt, FaList, FaCog, FaQuestionCircle, FaSignOutAlt } from "react-icons/fa";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation(); // Get current route
  const [activeMenu, setActiveMenu] = useState(location.pathname); // Track active menu

  const handleNavigation = (path) => {
    setActiveMenu(path); // Update active state
    navigate(path); // Navigate to the selected path
  };

  return (
    <aside className="sidebar">
      <div className="profile">
        <img src="https://via.placeholder.com/40" alt="Profile" className="profile-img" />
        <h3>Sundar Gurung</h3>
        <p>sundargurung360@gmail.com</p>
      </div>

      <nav className="menu">
        <a 
          onClick={() => handleNavigation("/")} 
          className={activeMenu === "/" ? "active" : ""}
        >
          <FaTachometerAlt className="sidebar-icon" /> Dashboard
        </a>
        <a 
          onClick={() => handleNavigation("/mytask")} 
          className={activeMenu === "/mytask" ? "active" : ""}
        >
          <FaList className="sidebar-icon" /> My Task
        </a>
        <a 
          onClick={() => handleNavigation("/TaskCategories")} 
          className={activeMenu === "/TaskCategories" ? "active" : ""}
        >
          <FaQuestionCircle className="sidebar-icon" /> Task Categories
        </a>
        <a 
          onClick={() => handleNavigation("/settings")} 
          className={activeMenu === "/settings" ? "active" : ""}
        >
          <FaCog className="sidebar-icon" /> Settings
        </a>
        <a 
          onClick={() => handleNavigation("/help")} 
          className={activeMenu === "/help" ? "active" : ""}
        >
          <FaQuestionCircle className="sidebar-icon" /> Help
        </a>
      </nav>

      <div className="logout">
        <a href="#"><FaSignOutAlt className="sidebar-icon" /> Logout</a>
      </div>
    </aside>
  );
}

export default Sidebar;
