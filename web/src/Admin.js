/**
 * @file Admin.js
 * @description Renders the admin dashboard, allowing navigation to group creation and management.
 */
import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, Breadcrumbs, Link } from '@mui/material';
import { useHistory, Route, Switch } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * @component Admin
 * @description Provides admin-level actions such as group creation and viewing protected routes.
 * @returns {JSX.Element}
 */
function Admin() {
  const [message, setMessage] = useState('');
  const history = useHistory();
  const isLoggedIn = !!localStorage.getItem('token');

  useEffect(() => {
    fetch(`${API_URL}/protected`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          setMessage(data.message);
        } else {
          history.push('/login');
        }
      });
  }, [history]);

  return (
    <Container maxWidth="sm">
      <Box sx={{ textAlign: 'center', mt: 8 }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Admin Area
        </Typography>
        <Typography variant="h5" component="p" gutterBottom>
          Welcome to the admin area.
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <Button variant="outlined" color="primary" onClick={() => history.push('/groups/new')}>
            Create Group
          </Button>
          <Button variant="outlined" color="primary" onClick={() => history.push('/groups')} sx={{ ml: 2 }}>
            View Groups
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Admin;
