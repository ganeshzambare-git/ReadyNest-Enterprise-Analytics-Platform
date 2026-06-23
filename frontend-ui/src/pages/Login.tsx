import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import apiClient from '../api/client';
import './Pages.css';

const Login = () => {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/auth/login', { username, password });
      login(response.data.token, response.data.user);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="login-page">
      <div className="login-card glow-cyan-box">
        <div className="text-center mb-8">
          <span className="text-4xl text-cyan glow-cyan-text mb-4 inline-block">⬡</span>
          <h2 className="font-orbitron text-2xl font-bold">ReadyNest Auth</h2>
          <p className="text-gray-400 text-sm mt-2">Enter your credentials to access the data platform.</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              className="dark-input"
            />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              className="dark-input"
            />
          </div>
          <button type="submit" className="btn-primary bg-green glow-green-box w-full mt-4">
            Authenticate
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
