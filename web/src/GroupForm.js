import React, { useState, useEffect } from 'react';
import { Container, TextField, Button, Box, Typography, Paper, Breadcrumbs, Link } from '@mui/material';
import { useHistory, useParams } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function GroupForm() { // Removed userData as a prop
  const [name, setName] = useState('');
  const [picture, setPicture] = useState('');
  const [maxProfiles, setMaxProfiles] = useState('');
  const [error, setError] = useState('');
  const [groupId, setGroupId] = useState('');
  const [pictureError, setPictureError] = useState('');
  const history = useHistory();
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      fetch(`${API_URL}/groups/${id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => response.json())
      .then(data => {
        setName(data.name);
        setPicture(data.picture);
        setMaxProfiles(data.max_profiles);
        setGroupId(data.id);
      });
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (picture && !isValidUrl(picture)) {
      setPictureError('Invalid URL');
      return;
    }
    const maxProfilesInt = parseInt(maxProfiles, 10);
    if (isNaN(maxProfilesInt) || maxProfilesInt <= 0) {
      setError('Max Profiles must be a positive integer');
      return;
    }
    setPictureError('');
    setError('');
    const method = id ? 'PUT' : 'POST';
    const endpoint = id ? `${API_URL}/groups/${id}` : `${API_URL}/groups`;
    const response = await fetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ name, picture, max_profiles: maxProfilesInt }),
    });
    if (response.ok) {
      history.push('/groups');
    } else {
      const data = await response.json();
      setError(data.message);
    }
  };

  const isValidUrl = (url) => {
    try {
      new URL(url);
      return true;
    } catch (_) {
      return false;
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
        <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2, p: 1 }}>
          <Link color="inherit" onClick={() => history.push('/admin')} sx={{ cursor: 'pointer' }}>
            Admin
          </Link>
          <Link color="inherit" onClick={() => history.push('/groups')} sx={{ cursor: 'pointer' }}>
            Groups
          </Link>
          <Typography color="textPrimary">{id ? 'Edit Group' : 'Create Group'}</Typography>
        </Breadcrumbs>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {id ? 'Edit Group' : 'Create Group'}
          </Typography>
          {error && <Typography color="error">{error}</Typography>}
        </Box>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Group ID"
            fullWidth
            margin="normal"
            value={groupId}
            InputProps={{
              readOnly: true,
            }}
          />
          <TextField
            label="Name"
            fullWidth
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <TextField
            label="Picture URL"
            fullWidth
            margin="normal"
            value={picture}
            onChange={(e) => setPicture(e.target.value)}
            error={!!pictureError}
            helperText={pictureError}
          />
          <TextField
            label="Max Profiles"
            type="number"
            fullWidth
            margin="normal"
            value={maxProfiles}
            onChange={(e) => setMaxProfiles(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
            {id ? 'Update' : 'Create'}
          </Button>
        </form>
      </Paper>
    </Container>
  );
}

export default GroupForm;
