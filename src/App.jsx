import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashBoard from './Layout/DashBoard/DashBoard';
import MyTask from './Layout/MyTask/MyTask';
import Header from './Layout/DashBoard/Section/Header/Header';
import Sidebar from './Layout/DashBoard/Section/SideBar/SideBar';
import Setting from './Layout/Setting/Setting';
import Profile from './Layout/Profile/Profile';
import ChangePassword from './Layout/ChangePassword/ChangePassword';
import TestNotification from './Layout/Profile/TestNotification';
import './App.css';

function App() {
    return (
        <Router>
            <Header />
            <div className="main-content">
                <Sidebar />
                <Routes>
                    <Route path="/" element={<DashBoard />} />
                    <Route path="/mytask" element={<MyTask />} />
                    <Route path="/settings" element={<Setting />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/change-password" element={<ChangePassword />} />
                    <Route path="/test-notification" element={<TestNotification />} />

                </Routes>
            </div>
        </Router>
    );
}

export default App;
