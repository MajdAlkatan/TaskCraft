// src/Layout/Home/Home.jsx
import './Home.css';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Welcome to Jaz Task Manager</h1>
      <p>Select your workspace or create a new one:</p>

      {/* Example Buttons to navigate to dashboards */}
      <div className="workspace-buttons">
        <button onClick={() => navigate('/dashboard')}>Main Workspace</button>
        <button onClick={() => navigate('/mytask')}>My Tasks</button>
      </div>
    </div>
  );
};

export default Home;
