import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { BU } from '../../config';
import axios from '../../Utils/axiosInstance'; // ✅ instead of 'axios'

export const fetchUserData = createAsyncThunk(
  'users/fetchUserData',
  async (_, { getState }) => {
    const state = getState();
    const token = state.auth.accessToken; // Token retrieved from the auth state

    if (!token) {
      throw new Error('No access token found'); // Handle case where token is missing
    }

    const response = await axios.get(`${BU}/users/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    return response.data.results[0]; // Assuming `results[0]` contains the user data
  }
);

const initialState = {
  user: null,
  loading: false,
  error: null,
  profile: {
    fullname: '',
    email: '',
    image: null
  }
};

const usersSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    resetUserState: (state) => {
      state.user = null;
      state.profile = initialState.profile;
    },
    updateProfile: (state, action) => {
      state.profile = { ...state.profile, ...action.payload };
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUserData.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload;
        state.profile = {
          ...state.profile,
          fullname: action.payload.fullname,
          email: action.payload.email,
          image: action.payload.image
        };
      })
      .addCase(fetchUserData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
      
  }
});

// Export actions
export const { resetUserState, updateProfile } = usersSlice.actions;

// Export reducer 
export default usersSlice.reducer;
