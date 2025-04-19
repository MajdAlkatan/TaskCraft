import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logoutUser } from "../../../../store/reducers/authReducer";
import { fetchUserData } from "../../../../store/reducers/usersSlice";
import "./Sidebar.css";
import {
  FaTachometerAlt,
  FaList,
  FaCog,
  FaQuestionCircle,
  FaSignOutAlt,
  FaPlus,
} from "react-icons/fa";
import WorkspaceModal from "../../../../Components/WorkspaceModal/WorkspaceModal"; // Import the modal component

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const [activeMenu, setActiveMenu] = useState(location.pathname);
  const { profile } = useSelector((state) => state.users);
  const [isModalOpen, setIsModalOpen] = useState(false); // State for modal visibility

  useEffect(() => {
    dispatch(fetchUserData());
  }, [dispatch]);

  const handleNavigation = (path) => {
    setActiveMenu(path);
    navigate(path);
  };

  const handleLogout = () => {
    dispatch(logoutUser());
    navigate("/login");
  };

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  return (
    <aside className="sidebar">
      <div className="profile">
        <img
          src={profile.image}
          alt="Profile"
          className="profile-img"
        />
        <h3>{profile.fullname || "Loading..."}</h3>
        <p>{profile.email || ""}</p>
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
      <hr />
      <div className="new-workspaces">
        <button onClick={toggleModal} className="new-workspaces-button">
          <FaPlus className="sidebar-icon" /> New Workspace
        </button>
      </div>

      <div className="logout">
        <a onClick={handleLogout}>
          <FaSignOutAlt className="sidebar-icon" /> Logout
        </a>
      </div>

      {/* Modal for creating a new workspace */}
      {isModalOpen && <WorkspaceModal onClose={toggleModal} />}
    </aside>
  );
}

export default Sidebar;