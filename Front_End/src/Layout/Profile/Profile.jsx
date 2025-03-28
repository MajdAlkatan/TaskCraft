import React, { useState } from 'react';
import "./Profile.css"
import DefulteInput from '../../Components/Input/DefulteInput/DefulteInput'; // Adjust the import path as necessary
import { FaPen, FaSave } from "react-icons/fa";

function Profile() {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    username: "Sundar Gurung",
    email: "sundargurung360@gmail.com",
    phone: "1234567890",
  });
  const [profileImage, setProfileImage] = useState("https://via.placeholder.com/40");

  const handleEditToggle = () => {
    setIsEditing((prev) => !prev);
  };

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSave = () => {
    setIsEditing(false);
    // Logic to save data, e.g., API call
    console.log("Saved data", formData);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfileImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <section className='profile-section'>
      <div className="profile-header-section">
        <img
          src={profileImage}
          alt="Profile"
          className='profil-img'
          onClick={() => document.getElementById('profile-image-input').click()} // Trigger file input click
        />
        <div className="profil-title">
          <h3>{formData.username}</h3>
          <p>{formData.email}</p>
        </div>
        <input
          type="file"
          id="profile-image-input"
          style={{ display: 'none' }} // Hide the file input
          accept="image/*" // Accept only image files
          onChange={handleImageChange}
        />
      </div>
      <div className='profile-detailes-secction'>
        {isEditing ? (
          <DefulteInput
            label='Username'
            id='username'
            type='text'
            value={formData.username}
            onChange={handleChange}
          />
        ) : (
          <h3>{formData.username}</h3>
        )}
        {isEditing ? (
          <DefulteInput
            label='Email'
            id='email'
            type='email'
            value={formData.email}
            onChange={handleChange}
          />
        ) : (
          <p>{formData.email}</p>
        )}
        {isEditing ? (
          <DefulteInput
            label='Contact Number'
            id='phone'
            type='number'
            value={formData.phone}
            onChange={handleChange}
          />
        ) : (
          <p>Contact Number: {formData.phone}</p>
        )}
      </div>
      <div className="edit-save-icons">
        {isEditing ? (
          <div className="fasave" onClick={handleSave}>
            <p>Save</p>
            <FaSave className="save-icon" />
          </div>
        ) : (
          <div className="fapen" onClick={handleEditToggle}>
            <p>Edit</p>
            <FaPen className="edit-icon" />
          </div>
        )}
      </div>
    </section>
  );
}

export default Profile;