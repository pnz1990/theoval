import React, { useState, useEffect } from 'react';
import { Container, Box, List, ListItem, ListItemText, Typography, Paper, Button } from '@mui/material';
import { useHistory } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * # ProfileList
 *
 * Fetches and displays all profiles associated with the current user.
 *
 * @component
 * @param {Object} props - Component props.
 * @param {Object} props.userData - Contains user data utilized for authentication and fetching profiles.
 * @returns {JSX.Element} A React component that displays a list of profiles or a prompt to create a new one.
 */
function ProfileList({ userData }) { 
  const [profiles, setProfiles] = useState([]);
  const history = useHistory();

  useEffect(() => {
    if (userData) { 
      fetch(`${API_URL}/profiles`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => response.json())
      .then(data => setProfiles(data));
    }
  }, [userData]);

  /**
   * Handles profile selection and navigates to the respective chats page.
   *
   * @function handleProfileClick
   * @param {Object} profile - The selected profile object.
   * @returns {void}
   */
  const handleProfileClick = (profile) => {
    history.push(`/groups/${profile.group_id}/chats?profile_id=${profile.id}`);
  };

  if (!profiles.length) {
    return (
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
          <Box sx={{ textAlign: 'center', mb: 2 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              No profiles yet.
            </Typography>
            <Button variant="contained" color="primary" onClick={() => history.push('/profileform')}>
              Create Profile
            </Button>
          </Box>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Your Profiles
          </Typography>
        </Box>
        <List>
          {profiles.map(profile => (
            <ListItem button key={profile.id} onClick={() => handleProfileClick(profile)}>
              <ListItemText primary={profile.name} secondary={profile.bio} />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
}

export default ProfileList;
