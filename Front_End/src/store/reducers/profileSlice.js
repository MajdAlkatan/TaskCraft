import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../../Utils/axiosInstance';

// Async thunk for updating profile
export const updateProfile = createAsyncThunk(
  'profile/updateProfile',
  async (profileData, thunkAPI) => {
    try {
      const state = thunkAPI.getState();
      const userId = state.users.user?.id; // <- dynamically get user ID
      const response = await axiosInstance.put(`/users/${userId}/`, profileData);
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || 'Failed to update profile');
    }
  }
);

// Async thunk for uploading profile image
export const uploadProfileImage = createAsyncThunk(
  'profile/uploadProfileImage',
  async (imageFile, thunkAPI) => {
    try {
      const state = thunkAPI.getState();
      const token = state.auth.token;  // Assuming the token is stored in auth slice

      const formData = new FormData();
      formData.append('image', imageFile);

      // Add the Authorization header with the token
      const response = await axiosInstance.patch(`/users/change_image/`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,  // Include the token
        },
      });

      // The API should return the updated image URL in the response.
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || 'Failed to upload image');
    }
  }
);

const profileSlice = createSlice({
  name: 'profile',
  initialState: {
    user: {
      username: 'Sundar Gurung',
      email: 'sundargurung360@gmail.com',
      phone: '1234567890',
      image: 'https://via.placeholder.com/40'
    },
    loading: false,
    error: null
  },
  reducers: {
    setUsername: (state, action) => {
      state.user.username = action.payload;
    },
    setEmail: (state, action) => {
      state.user.email = action.payload;
    },
    setPhone: (state, action) => {
      state.user.phone = action.payload;
    },
    setImage: (state, action) => {
      state.user.image = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(updateProfile.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.user.username = action.payload.fullname;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(uploadProfileImage.fulfilled, (state, action) => {
        // The API response contains the new image URL.
        state.user.image = action.payload.image || state.user.image;

      })
      .addCase(uploadProfileImage.rejected, (state, action) => {
        state.error = action.payload;
      });
  }
});

export const { setUsername, setEmail, setPhone, setImage } = profileSlice.actions;

export default profileSlice.reducer;
