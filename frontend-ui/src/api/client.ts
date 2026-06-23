import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // FastAPI default port
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach mock auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
