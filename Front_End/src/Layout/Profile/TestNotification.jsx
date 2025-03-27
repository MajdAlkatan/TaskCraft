import React from 'react';
import "./Profile.css"

function TestNotification() {
  const sendNotification = () => {
    if ("Notification" in window) {
      Notification.requestPermission().then(permission => {
        
        if (permission === 1) {
          new Notification("Test Notification", {
            body: "This is a test notification from your ToDo app!",
            icon: "/icon.png", // You can replace this with your app's icon
          });
        } else {
          alert("Notification permission denied!");
        }
      });
    } else {
      alert("Your browser does not support notifications.");
    }
  };

  return (
    <div className="notification-section">
      <h3>Test Notifications</h3>
      <p>Click the button below to send a test notification.</p>
      <button onClick={sendNotification}>Send Test Notification</button>
    </div>
  );
}

export default TestNotification;
