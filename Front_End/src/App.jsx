import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';

import DashBoard from './Layout/DashBoard/DashBoard';
import MyTask from './Layout/MyTask/MyTask';
import Header from './Layout/DashBoard/Section/Header/Header';
import Sidebar from './Layout/DashBoard/Section/SideBar/SideBar';
import Setting from './Layout/Setting/Setting';
import Profile from './Layout/Profile/Profile';
import ChangePassword from './Layout/ChangePassword/ChangePassword';
import TestNotification from './Layout/Profile/TestNotification';
import Login from "./Layout/Auth/Login/Login";
import Register from "./Layout/Auth/Register/Register";
import HelpSection from './Layout/Help/Help';
import TaskCategories from './Layout/TaskCategories/TaskCategories';

import './App.css';
import { useEffect } from 'react';

// A wrapper to access the location inside a component
const LayoutWrapper = ({ children }) => {
  const location = useLocation();
  const hideHeaderAndSidebar = location.pathname === "/login" || location.pathname === "/register";

  return (
    <>
      {!hideHeaderAndSidebar && <Header />}
      <div className="main-content">
        {!hideHeaderAndSidebar && <Sidebar />}
        {children}
      </div>
    </>
  );
};

function App() {
  
  const dispatch = useDispatch();

  useEffect(() => {
    const interval = setInterval(() => {
      // Try refreshing the token every 100 seconds (before 2 min expiry)
      dispatch(refreshToken());
    }, 100 * 1000); // 100 seconds

    return () => clearInterval(interval); // Clean up
  }, [dispatch]);
  const { user } = useSelector((state) => state.auth);

  return (
    <Router>
      <LayoutWrapper>
        <Routes>
          {/* Auth Routes */}
          <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login />} />
          <Route path="/register" element={<Register />} />

          {/* Redirect root to login or dashboard */}
          <Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />

          {/* Protected Routes */}
          <Route path="/dashboard" element={user ? <DashBoard /> : <Navigate to="/login" />} />
          <Route path="/mytask" element={<MyTask />} />
          <Route path="/settings" element={<Setting />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/change-password" element={<ChangePassword />} />
          <Route path="/test-notification" element={<TestNotification />} />
          <Route path="/TaskCategories" element={<TaskCategories />} />
          <Route path="/help" element={<HelpSection />} />
        </Routes>
      </LayoutWrapper>
    </Router>
  );
}

export default App;
