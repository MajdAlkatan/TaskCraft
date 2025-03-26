import React from 'react';
import "./Profile.css"
function Profile() {
  return (
    <div className="profile-section">
      <h3>Profile Info</h3>
      <div>
        <label>Username:</label>
        <p>John Doe</p>
      </div>
      <div>
        <label>Email:</label>
        <p>johndoe@example.com</p>
      </div>
    </div>
  );
}

export default Profile;
