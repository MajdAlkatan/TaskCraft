import React from 'react';
import "./Profile.css"
import DefulteInput from '../../Components/Input/DefulteInput/DefulteInput'; // Adjust the import path as necessary

function Profile() {
  return (
    <section className='profile-section'>
      <div className="profile-header-section">
        <img src="https://via.placeholder.com/40" alt="Profile" className='profil-img' />
        <div className="profil-title">
          <h3>Sundar Gurung</h3>
          <p>sundargurung360@gmail.com</p>
        </div>
      </div>
      <div className='profile-detailes-secction'>
        <DefulteInput label='Username'
          id={'username'}
          type='text'
          value={''}
          onChange={''}

        />
        <DefulteInput label='Email'
          id={'Email'}
          type='email'
          value={''}
          onChange={''}

        />
        <DefulteInput label='Contact Number'
          id={'phonrnumber'}
          type='number'
          value={''}
          onChange={''}

        />
      </div>

    </section>
  );
}

export default Profile;
