import React from 'react'
import "./Register.css"
import img from "../../../assets/R2.svg"
import AuthInput from '../../../Components/Input/AuthInput/AuthInput'
import AuthButton from '../../../Components/Button/AuthButton/AuthButton'
import { FaUser, FaLock, FaMailBulk } from "react-icons/fa"
function Register() {
    return (
        <div className='signup-section'>
            <img src={img} alt="" className='signupimg' />
            <div className='right-side-signup' >
                <h1>Sign Up</h1>
                <AuthInput placeholder='Enter Full Name' inputtype={'text'} Icon={FaUser} />
                <AuthInput placeholder='Enter Email' inputtype={'Email'} Icon={FaMailBulk} />
                <AuthInput placeholder='Enter Password' inputtype='password' Icon={FaLock} />
                <AuthInput placeholder='Confirm Password' inputtype='password' Icon={FaLock} />
                <div className="i-agree">
                    <input type="checkbox" id="agree" />
                    <label htmlFor="agree">I agree all terms</label>
                </div>
                <div className='authbuttonsignup'>
                    <AuthButton text='SignUp' />
                </div>
                <div className="create-account">
                    <p>Allready have an account? <a href="#">Sgin in</a></p>
                </div>
            </div>

        </div>
    )
}

export default Register