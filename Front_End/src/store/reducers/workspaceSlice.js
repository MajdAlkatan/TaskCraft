// src/store/reducers/workspaceSlice.js
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import axios from '../../Utils/axiosInstance'; // This uses the configured instance with interceptors

export const createWorkspace = createAsyncThunk(
  'workspace/create',
  async ({ name, image }, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('name', name);
      if (image) {
        formData.append('image', image);
      }

      const response = await axios.post('/workspaces/', formData);
      return response.data;
    } catch (error) {
      return rejectWithValue(
        error.response?.data || { detail: 'Something went wrong' }
      );
    }
  }
);

const workspaceSlice = createSlice({
  name: 'workspace',
  initialState: {
    isLoading: false,
    error: null,
    createdWorkspace: null,
  },
  reducers: {
    clearWorkspaceState: (state) => {
      state.isLoading = false;
      state.error = null;
      state.createdWorkspace = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(createWorkspace.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createWorkspace.fulfilled, (state, action) => {
        state.isLoading = false;
        state.createdWorkspace = action.payload;
      })
      .addCase(createWorkspace.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const { clearWorkspaceState } = workspaceSlice.actions;
export default workspaceSlice.reducer;
