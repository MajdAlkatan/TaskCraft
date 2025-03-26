import React, { useState } from 'react';

function ChangePassword() {
  const [newPassword, setNewPassword] = useState('');

  const handleChangePassword = (e) => {
    e.preventDefault();
    console.log('Password changed:', newPassword);
  };

  return (
    <div className="change-password-section">
      <h3>Change Password</h3>
      <form onSubmit={handleChangePassword}>
        <div>
          <label>New Password:</label>
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Change Password</button>
      </form>
    </div>
  );
}

export default ChangePassword;
