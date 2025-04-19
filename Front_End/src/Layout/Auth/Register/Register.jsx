import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { registerUser } from '../../../store/reducers/authReducer';
import AuthInput from '../../../Components/Input/AuthInput/AuthInput';
import AuthButton from '../../../Components/Button/AuthButton/AuthButton';
import { FaUser, FaLock, FaMailBulk } from "react-icons/fa";
import './Register.css';
import img from "../../../assets/R2.svg";

function Register() {
    const dispatch = useDispatch();
    const [formData, setFormData] = useState({
        email: '',
        fullname: '',
        password: '',
    });

    const { loading, error } = useSelector((state) => state.auth);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.email || !formData.fullname || !formData.password) {
            return alert("All fields are required");
        }
        dispatch(registerUser(formData));
    };

    return (
        <div className='signup-section'>
            <img src={img} alt="Signup" className='signupimg' />
            <div className='right-side-signup'>
                <h1>Sign Up</h1>
                <form onSubmit={handleSubmit}>
                    <AuthInput
                        placeholder='Enter Full Name'
                        name='fullname'
                        inputtype='text'
                        Icon={FaUser}
                        onChange={handleChange}
                        value={formData.fullname}
                    />
                    <AuthInput
                        placeholder='Enter Email'
                        name='email'
                        inputtype='email'
                        Icon={FaMailBulk}
                        onChange={handleChange}
                        value={formData.email}
                    />
                    <AuthInput
                        placeholder='Enter Password'
                        name='password'
                        inputtype='password'
                        Icon={FaLock}
                        onChange={handleChange}
                        value={formData.password}
                    />
                    <AuthButton type='submit' disabled={loading} text={'register'}>
                        {loading ? 'Registering...' : 'Register'}
                    </AuthButton>
                    {error && (
                        <div className='error-message'>
                            <strong>Error:</strong> {error}
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}

export default Register;
