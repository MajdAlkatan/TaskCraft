import Login from './Layout/Auth/Login/Login'
import Register from './Layout/Auth/Register/Register'
import DashBoard from './Layout/DashBoard/DashBoard'
import Header from './Layout/DashBoard/Section/Header/Header'
import Sidebar from './Layout/DashBoard/Section/SideBar/SideBar'
import './App.css'

function App() {
    return (
        <>
            <Header />
            <div className="main-content">
            <Sidebar />
            <DashBoard />

            </div>
            {/* <Login/> */}
            {/* <Register/> */}
        </>
    )
}

export default App
