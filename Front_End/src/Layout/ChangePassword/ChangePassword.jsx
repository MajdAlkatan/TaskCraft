import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updatePassword, clearPasswordStatus } from '../../store/reducers/changepasswordSlice';
import { logoutUser } from '../../store/reducers/authReducer';

import DefulteInput from '../../Components/Input/DefulteInput/DefulteInput';
import FormButton from "../../Components/Button/FormButton/FormButton";
import './ChangePassword.css';

function ChangePassword() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const dispatch = useDispatch();
  const { success, error } = useSelector(state => state.changePassword);

  useEffect(() => {
    if (success) {
      alert("Password changed successfully. You will be logged out in 5 minutes. Click OK to logout now.");
      const timeout = setTimeout(() => {
        dispatch(logoutUser());
        window.location.href = '/login'; // Or navigate with react-router
      }, 5 * 60 * 1000); // 5 minutes
      
      // Optional: logout immediately if user clicks confirm
      if (window.confirm("Logout now? Click 'OK' or wait 5 minutes.")) {
        clearTimeout(timeout);
        dispatch(logoutUser());
        window.location.href = '/login';
      }
    }
    return () => dispatch(clearPasswordStatus());
  }, [success, dispatch]);

  const handleChangePassword = (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      alert('New password and confirm password do not match.');
      return;
    }

    const passData = {
      old_password: currentPassword,
      new_password: newPassword,
    };

    dispatch(updatePassword(passData));
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
           placeholder='enter old password'
            label="Current Password"
            id="current-password"
            type="password"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            required
          />
          <DefulteInput
          placeholder='enter new password'
            label="New Password"
            id="new-password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <DefulteInput
          placeholder='enter confirm password'
            label="Confirm New Password"
            id="confirm-password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />

          {error && <p style={{ color: 'red', marginTop: 10 }}>{JSON.stringify(error)}</p>}

          <div className="btn-changepassword">
            <FormButton type="submit" label='Change password' />
            <FormButton type="button" label='Cancel' onClick={() => window.history.back()} />
          </div>
        </form>
      </div>
    </section>
  );
}

export default ChangePassword;
