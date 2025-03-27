import React from 'react';
import './WelcomeBack.css'; // Import CSS for styling

const WelcomeBack = () => {
  const users = [
    'user1.jpg', // Replace with actual avatar image paths
    'user2.jpg',
    'user3.jpg',
    'user4.jpg',
    'user5.jpg',
  ];

  return (
    <div className="welcome-back">
      <h2>
        Welcome back, Sundar <span role="img" aria-label="wave">👋</span>
      </h2>
      <div className="user-avatars">
        {users.map((user, index) => (
          <img key={index} src={user} alt={`User ${index + 1}`} className="avatar" />
        ))}
      </div>
      <button className="invite-button">Invite</button>
    </div>
  );
};

export default WelcomeBack;