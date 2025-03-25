import React from "react";
import "./Login.css";
import UserInput from "../../../Components/Input/AuthInput/AuthInput";
import { FaUser, FaLock } from "react-icons/fa";
import { FaFacebook, FaGoogle, FaXTwitter } from "react-icons/fa6"; // Social icons
import LoginButton from "../../../Components/Button/AuthButton/AuthButton";
import img from "../../../assets/ach31.svg";
// import facebook from "../../../assets/facebook.png";
// import google from "../../../assets/google.png";
// import twitter from "../../../assets/twitter.png";

function Login() {
    return (
        <div className="login-section">
            {/* Left Side - Login Form */}
            <div className="login-left-side">
                <h1>Sign In</h1>
                <UserInput inputtype={"text"} placeholder={"Enter Username"} Icon={FaUser} />
                <UserInput inputtype={"password"} placeholder={"Enter Password"} Icon={FaLock} />

                {/* Remember Me Checkbox */}
                <div className="remember-me">
                    <input type="checkbox" id="remember" />
                    <label htmlFor="remember">Remember Me</label>
                </div>

                {/* Login Button */}
                <LoginButton text={"Login"} onClick={() => alert("Login button clicked")} />

                {/* Social Login */}
                <div className="social-login">
                    <p>Or, Login with</p>
                    <div className="social-icons">
                        <FaFacebook className="social-icon facebook" />
                        <FaGoogle className="social-icon google" />
                        <FaXTwitter className="social-icon twitter" />
                    </div>
                </div>
                {/* Sign Up Link */}
                <div className="create-account">
                    <p>Don't have an account? <a href="#">Create One</a></p>
                </div>
            </div>

            {/* Right Side - Image */}
            <img src={img} alt="Login Illustration" className="lognimg" />
        </div>
    );
}

export default Login;
