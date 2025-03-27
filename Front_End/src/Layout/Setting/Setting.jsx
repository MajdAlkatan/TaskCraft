import React from 'react';
import { Link } from 'react-router-dom';
import "./Setting.css";

function Setting() {
  return (
    <div className="settings-container">
      <h2>Settings</h2>

      <table>
        <thead>
          <tr>
            <th>Section</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Profile</td>
            <td><Link to="/profile">View</Link></td>
          </tr>
          <tr>
            <td>Change Password</td>
            <td><Link to="/change-password">Change</Link></td>
          </tr>
          <tr>
            <td>Test Notification</td>
            <td><Link to="/test-notification">Send</Link></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Setting;
