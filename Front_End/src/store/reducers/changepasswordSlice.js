// src/store/reducers/changePasswordSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axiosInstance from '../../Utils/axiosInstance';

export const updatePassword = createAsyncThunk(
  'changePassword/updatePassword',
  async (passData, thunkAPI) => {
    try {
      const response = await axiosInstance.patch(`/users/change_password/`, passData);
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || 'Failed to update password');
    }
  }
);

const changePasswordSlice = createSlice({
  name: 'changePassword',
  initialState: {
    loading: false,
    success: false,
    error: null,
  },
  reducers: {
    clearPasswordStatus: (state) => {
      state.success = false;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(updatePassword.pending, (state) => {
        state.loading = true;
        state.success = false;
        state.error = null;
      })
      .addCase(updatePassword.fulfilled, (state) => {
        state.loading = false;
        state.success = true;
      })
      .addCase(updatePassword.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export const { clearPasswordStatus } = changePasswordSlice.actions;
export default changePasswordSlice.reducer;
