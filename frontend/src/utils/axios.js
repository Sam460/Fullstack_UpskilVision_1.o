// src/utils/axios.js (or wherever your axios.js is located)

import axios from 'axios';

// Use environment variable for API base URL
const instance = axios.create({
  // --- CORRECTED BASE URL ---
  // If VITE_API_BASE_URL is not set, it will default to 'http://localhost:5000'.
  // This removes the problematic '+ /api' which was creating the wrong path for /auth routes.
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000', 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
});

// Add request interceptor for auth token
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 404) {
      console.error('API endpoint not found:', error.config?.url);
    }

    if (error.response?.status === 500) {
      console.error('Server error:', error.response?.data);
      error.message = error.response?.data?.message || 'An unexpected server error occurred';
    }
    
    // For 401 Unauthorized, you might want to redirect to login
    if (error.response?.status === 401) {
        localStorage.removeItem('token');
        // window.location.href = '/login'; // Uncomment if you want automatic redirect
    }

    return Promise.reject(error);
  }
);

export default instance;