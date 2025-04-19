import React, { useState, useEffect } from 'react';
import './Profile.css';
import DefulteInput from '../../Components/Input/DefulteInput/DefulteInput';
import { FaPen, FaSave } from 'react-icons/fa';
import { useDispatch, useSelector } from 'react-redux';
import { updateProfile, uploadProfileImage } from '../../store/reducers/profileSlice';
import { fetchUserData } from '../../store/reducers/usersSlice';

function Profile() {
  const dispatch = useDispatch();
  const { profile, loading } = useSelector((state) => state.users);

  const [isEditing, setIsEditing] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [formData, setFormData] = useState({
    fullname: '',
    email: '',
  });

  useEffect(() => {
    if (profile) {
      setFormData({
        fullname: profile.fullname || '',
        email: profile.email || '',
      });
      setImagePreview(profile.image || '');
    }
  }, [profile]);

  const handleEditToggle = () => setIsEditing(true);

  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData((prev) => ({ ...prev, [id]: value }));
  };

  const handleSave = async () => {
  try {
    // 1. Update profile
    await dispatch(updateProfile({ 
      id: profile.id, 
      fullname: formData.fullname,
      email: formData.email // أضف هذا إذا كان ال API يسمح بتحديث الإيميل
    })).unwrap();

    // 2. Upload image if exists
    if (imageFile) {
      await dispatch(uploadProfileImage(imageFile)).unwrap();
    }

    // 3. Refresh data
    await dispatch(fetchUserData());

    // 4. Exit edit mode
    setIsEditing(false);
  } catch (error) {
    console.error('Update failed:', error);
  }
};

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <section className="profile-section">
      <div className="profile-header-section">
        <img
          src={imagePreview || profile.image}  // Use the preview or the existing profile image
          alt="Profile"
          className="profil-img"
          onClick={() => document.getElementById('profile-image-input').click()}
        />
        <div className="profil-title">
          <h3>{formData.fullname}</h3>
          <p>{formData.email}</p>
        </div>
        <input
          type="file"
          id="profile-image-input"
          style={{ display: 'none' }}
          accept="image/*"
          onChange={handleImageChange}
        />
      </div>

      <div className="profile-detailes-secction">
        {isEditing ? (
          <>
            <DefulteInput
              label="Username"
              id="fullname"
              type="text"
              value={formData.fullname}
              onChange={handleChange}
            />
            {/* <DefulteInput
              label="Email"
              id="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
            /> */}
          </>
        ) : (
          <>
            <h3>{formData.fullname}</h3>
            <p>{formData.email}</p>
          </>
        )}
      </div>

      <div className="edit-save-icons">
        {isEditing ? (
          <div className="fasave" onClick={handleSave}>
            <p>{loading ? 'Saving...' : 'Save'}</p>
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
