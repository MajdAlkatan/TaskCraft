// src/store/reducers/workspaceListSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from '../../Utils/axiosInstance';

export const fetchWorkspaces = createAsyncThunk(
  'workspaceList/fetch',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get('/workspaces/owned/');
      return response.data.workspaces;
    } catch (error) {
      return rejectWithValue(error.response?.data || { detail: 'Failed to fetch workspaces' });
    }
  }
);

const workspaceListSlice = createSlice({
  name: 'workspaceList',
  initialState: {
    workspaces: [],
    isLoading: false,
    error: null,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchWorkspaces.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchWorkspaces.fulfilled, (state, action) => {
        state.isLoading = false;
        state.workspaces = action.payload;
      })
      .addCase(fetchWorkspaces.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export default workspaceListSlice.reducer;
