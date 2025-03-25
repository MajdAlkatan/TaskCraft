import React from "react";
import "./Header.css";
import { FaSearch, FaBell, FaCalendarAlt } from "react-icons/fa";

function Header() {
  return (
    <header className="header">
      <div className="search-bar">
        <FaSearch className="icon" />
        <input type="text" placeholder="Search your task here..." />
      </div>

      <div className="header-right">
        <FaBell className="icon" />
        <FaCalendarAlt className="icon" />
        <span className="date">Tuesday <br /> <span className="date-number">20/06/2023</span></span>
      </div>
    </header>
  );
}

export default Header;
