import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { useEffect } from 'react';
import DashBoard from './Layout/DashBoard/DashBoard';
import MyTask from './Layout/MyTask/MyTask';
import Header from './Layout/DashBoard/Section/Header/Header';
import Sidebar from './Layout/DashBoard/Section/SideBar/SideBar';
import Setting from './Layout/Setting/Setting';
import Profile from './Layout/Profile/Profile';
import ChangePassword from './Layout/ChangePassword/ChangePassword';
import TestNotification from './Layout/Profile/TestNotification';
import Login from './Layout/Auth/Login/Login';
import Register from './Layout/Auth/Register/Register';
import HelpSection from './Layout/Help/Help';
import TaskCategories from './Layout/TaskCategories/TaskCategories';
import Home from './Layout/Home/Home'; // ✅ Your landing screen

import './App.css';

// A wrapper to apply layout only for internal app pages
const LayoutWrapper = ({ children }) => {
  const location = useLocation();
  const path = location.pathname;

  const hideHeaderAndSidebar =
    path === '/login' || path === '/register' || path === '/home';

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
  const { user } = useSelector((state) => state.auth);

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch(refreshToken());
    }, 100 * 1000);

    return () => clearInterval(interval);
  }, [dispatch]);

  return (
    <Router>
      <LayoutWrapper>
        <Routes>
          {/* Auth Routes */}
          <Route
            path="/login"
            element={user ? <Navigate to="/home" /> : <Login />}
          />
          <Route path="/register" element={<Register />} />

          {/* Root: Redirect to login or home */}
          <Route
            path="/"
            element={user ? <Navigate to="/home" /> : <Navigate to="/login" />}
          />

          {/* ✅ Landing/Home page (first after login) */}
          <Route
            path="/home"
            element={user ? <Home /> : <Navigate to="/login" />}
          />

          {/* Protected internal pages */}
          <Route
            path="/dashboard"
            element={user ? <DashBoard /> : <Navigate to="/login" />}
          />
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
