import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DashBoard from './Layout/DashBoard/DashBoard';
import MyTask from './Layout/MyTask/MyTask';
import Header from './Layout/DashBoard/Section/Header/Header';
import Sidebar from './Layout/DashBoard/Section/SideBar/SideBar';
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
                </Routes>
            </div>
        </Router>
    );
}

export default App;
