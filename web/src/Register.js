import React, { useState } from 'react';
import { Container, TextField, Button, Box, Typography, LinearProgress } from '@mui/material';
import { useHistory, Link } from 'react-router-dom';
import './Register.css';
import LogoutButton from './LogoutButton';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [passwordStrength, setPasswordStrength] = useState(0);
  const history = useHistory();
  const isLoggedIn = !!localStorage.getItem('token');

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);
    calculatePasswordStrength(value);
  };

  const calculatePasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength += 25;
    if (/[A-Z]/.test(password)) strength += 25;
    if (/[a-z]/.test(password)) strength += 25;
    if (/[0-9]/.test(password)) strength += 25;
    setPasswordStrength(strength);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (passwordStrength < 75) {
      setError('Password must be at least 8 characters long and include an uppercase letter, a lowercase letter, and a number');
      return;
    }
    fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => { throw new Error(data.message); });
      }
      return response.json();
    })
    .then(data => {
      localStorage.removeItem('token');
      history.push('/login');
    })
    .catch(error => {
      setError(error.message || 'An error occurred. Please try again.');
    });
  };

  return (
    <Container maxWidth="sm">
      {isLoggedIn && <LogoutButton />}
      <Box sx={{ textAlign: 'center', mt: 8 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Register
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
            onChange={handlePasswordChange}
          />
          <LinearProgress variant="determinate" value={passwordStrength} />
          <TextField
            label="Confirm Password"
            type="password"
            fullWidth
            margin="normal"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Register
          </Button>
        </form>
      </Box>
    </Container>
  );
}

export default Register;
