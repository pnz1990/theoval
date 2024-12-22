import React, { useState } from 'react';
import { Container, TextField, Button, Box, Typography } from '@mui/material';
import { useHistory, Link } from 'react-router-dom';
import './Login.css';
import LogoutButton from './LogoutButton';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function Login({ setIsLoggedIn }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const history = useHistory();
  const isLoggedIn = !!localStorage.getItem('token');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('token', data.token);
      setIsLoggedIn(true);
      history.push('/');
    } else {
      setError(data.message);
    }
  };

  return (
    <Container maxWidth="sm">
      {isLoggedIn && <LogoutButton />}
      <Box sx={{ textAlign: 'center', mt: 8 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Login
        </Typography>
        {error && <Typography color="error">{error}</Typography>}
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            type="email"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            label="Password"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Login
          </Button>
          <Typography variant="body2" sx={{ mt: 2 }}>
            Don't have an account? <Link to="/register">Register</Link>
          </Typography>
        </form>
      </Box>
    </Container>
  );
}

export default Login;
