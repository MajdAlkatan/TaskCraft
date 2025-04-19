// src/store/store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './reducers/authReducer';
import usersReducer from './reducers/usersSlice'
import profileReducer from './reducers/profileSlice'
import workspaceReducer from "./reducers/workspaceSlice"
import workspaceListReducer from "./reducers/workspaceListSlice"
import changePasswordReducer from "./reducers/changepasswordSlice"
const store = configureStore({
  reducer: {
    auth: authReducer,
    users: usersReducer,
    profile: profileReducer,
    workspace: workspaceReducer, 
    workspaceList: workspaceListReducer,
    changePassword: changePasswordReducer,



  },

});

export default store;
