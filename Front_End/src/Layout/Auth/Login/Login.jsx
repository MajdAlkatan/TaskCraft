import React , { useEffect, useState } from "react";
import "./Login.css";
import UserInput from "../../../Components/Input/AuthInput/AuthInput";
import { FaUser, FaLock } from "react-icons/fa";
import { FaFacebook, FaGoogle, FaXTwitter } from "react-icons/fa6";
import LoginButton from "../../../Components/Button/AuthButton/AuthButton";
import img from "../../../assets/ach31.svg";
import { useDispatch, useSelector } from 'react-redux';
import { loginUser } from '../../../store/reducers/authReducer';
import { useNavigate } from "react-router-dom"; // ✅ Add this

function Login() {
    const dispatch = useDispatch();
    const navigate = useNavigate(); // ✅ Initialize navigate

    const [credentials, setCredentials] = useState({
        email: '',
        password: '',
    });

    const { user, error } = useSelector((state) => state.auth); // ✅ Get user from auth slice

    useEffect(() => {
        if (user) {
            navigate('/dashboard'); // ✅ Navigate when user is logged in
        }
    }, [user, navigate]);

    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        dispatch(loginUser(credentials));
    };

    return (
        <div className="login-section">
            <div className="login-left-side">
                <h1>Sign In</h1>
                <form onSubmit={handleSubmit}>
                    <UserInput inputtype="text" name="email" placeholder="Enter You Email" Icon={FaUser} onChange={handleChange} value={credentials.email} />
                    <UserInput inputtype="password" name="password" placeholder="Enter Password" Icon={FaLock} onChange={handleChange} value={credentials.password} />
                    <div className="remember-me">
                        <input type="checkbox" id="remember" />
                        <label htmlFor="remember">Remember Me</label>
                    </div>
                    <LoginButton type="submit" text="Login" />
                    {error && <p className="error-message">{error}</p>}
                </form>
                <div className="social-login">
                    <p>Or, Login with</p>
                    <div className="social-icons">
                        <FaFacebook className="social-icon facebook" />
                        <FaGoogle className="social-icon google" />
                        <FaXTwitter className="social-icon twitter" />
                    </div>
                </div>
                <div className="create-account">
                    <p>Don't have an account? <a href="#">Create One</a></p>
                </div>
            </div>
            <img src={img} alt="Login Illustration" className="lognimg" />
        </div>
    );
}

export default Login;
