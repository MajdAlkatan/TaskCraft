import React, { Fragment } from "react";
import "./Header.css";
import { FaSearch, FaBell, FaCalendarAlt } from "react-icons/fa";
import IconButton from "../../../../Components/Button/IconButton/IconButton";
function Header() {
  return (
    <header className="header">
      <div className="brandName">Task<p className="craft">Craft</p> </div>
      <div className="search-bar">
        <FaSearch className="icon" />
        <input type="text" placeholder="Search your task here..." />
      </div>

      <div className="header-right">
        <IconButton icon={FaBell} />
        <IconButton icon={FaCalendarAlt} />
        <span className="date">Tuesday <br /> <span className="date-number">20/06/2023</span></span>
      </div>
    </header>
  );
}

export default Header;
