// src/store/store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './reducers/authReducer';
import usersReducer from './reducers/usersSlice'
import profileReducer from './reducers/profileSlice'
const store = configureStore({
  reducer: {
    auth: authReducer,
    users: usersReducer,
    profile: profileReducer,


  },

});

export default store;
