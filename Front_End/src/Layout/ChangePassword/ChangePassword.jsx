import React, { useState } from 'react';
import DefulteInput from '../../Components/Input/DefulteInput/DefulteInput'; // Adjust the import path as necessary
import './ChangePassword.css'; // Import the CSS file for styles
import FormButton from "../../Components/Button/FormButton/FormButton"
function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleChangePassword = (e) => {
    e.preventDefault();

    // Basic validation
    if (newPassword !== confirmPassword) {
      console.error('New password and confirm password do not match.');
      return;
    }

    console.log('Current Password:', currentPassword);
    console.log('New Password:', newPassword);
    // Here you would typically send the data to your backend for processing
  };

  return (
    <section className='changepassowrd'>
      <div className="profile-changepassword">
        <img src="https://via.placeholder.com/40" alt="Profile" className='changepassword-img' />
        <div className="pass-title">
          <h3>Sundar Gurung</h3>
          <p>sundargurung360@gmail.com</p>
        </div>
      </div>
      <div className="change-password-section">
        <form onSubmit={handleChangePassword}>
          <DefulteInput
            label="Current Password"
            id="current-password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
          />
          <DefulteInput
            label="New Password"
            id="new-password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <DefulteInput
            label="Confirm New Password"
            id="confirm-password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
          <div className="btn-changepassword">
            <FormButton type="submit" label='Change password' />
            <FormButton type="" label='cancle' />
          </div>
        </form>
      </div>
    </section>
  );
}

export default ChangePassword;