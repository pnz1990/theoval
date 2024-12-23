import React, { useState } from 'react';
import { Container, TextField, Button, Box, Typography, Paper } from '@mui/material';
import { useHistory } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * # ProfileForm
 *
 * Creates a new user profile within a specified group.
 *
 * @component
 * @param {Object} props - Component props.
 * @param {Object} props.userData - Contains user data to help verify authentication.
 * @returns {JSX.Element} A form to gather and submit profile details.
 */
function ProfileForm({ userData }) { // Added userData as a prop
  const [name, setName] = useState('');
  const [picture, setPicture] = useState('');
  const [bio, setBio] = useState('');
  const [error, setError] = useState('');
  const [pictureError, setPictureError] = useState('');
  const [group_id, setGroupId] = useState('');
  const [groupError, setGroupError] = useState('');
  const [groupProfilesLeft, setGroupProfilesLeft] = useState(null);
  const [step, setStep] = useState(1);
  const history = useHistory();

  /**
   * Validates the entered `group_id` and proceeds to the next step if valid.
   *
   * @function handleGroupSubmit
   * @param {Event} e - The event object.
   * @returns {Promise<void>}
   */
  const handleGroupSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch(`${API_URL}/groups/${group_id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (response.ok) {
      const group = await response.json();
      const profilesResponse = await fetch(`${API_URL}/profiles?group_id=${group_id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const profiles = await profilesResponse.json();
      setGroupProfilesLeft(group.max_profiles - profiles.length);
      setStep(2);
    } else {
      setGroupError('Invalid Group ID');
    }
  };

  /**
   * Submits the profile data to the server if all validations pass.
   *
   * @function handleSubmit
   * @param {Event} e - The event object.
   * @returns {Promise<void>}
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (picture && !isValidUrl(picture)) {
      setPictureError('Invalid URL');
      return;
    }
    setPictureError('');
    
    // Check if user already has a profile in the group
    const checkResponse = await fetch(`${API_URL}/profiles/check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ group_id }),
    });
    const checkData = await checkResponse.json();
    if (!checkResponse.ok) {
      setError(checkData.message);
      return;
    }

    const response = await fetch(`${API_URL}/profiles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ name, picture, bio, group_id }),
    });
    if (response.ok) {
      const profile = await response.json();
      history.push(`/groups/${profile.group_id}/chats?profile_id=${profile.id}`);
    } else {
      const data = await response.json();
      setError(data.message);
    }
  };

  /**
   * Checks if a given string is a valid URL.
   *
   * @function isValidUrl
   * @param {string} url - The URL string to validate.
   * @returns {boolean} Returns `true` if valid, otherwise `false`.
   */
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
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Create Profile
          </Typography>
          {error && <Typography color="error">{error}</Typography>}
        </Box>
        {step === 1 ? (
          <form onSubmit={handleGroupSubmit}>
            <TextField
              label="Group ID"
              fullWidth
              margin="normal"
              value={group_id}
              onChange={(e) => setGroupId(e.target.value)}
              required
            />
            {groupError && <Typography color="error">{groupError}</Typography>}
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
              Next
            </Button>
          </form>
        ) : (
          <form onSubmit={handleSubmit}>
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
              label="Bio"
              fullWidth
              margin="normal"
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              required
              multiline
              rows={4}
            />
            <TextField
              label="Group ID"
              fullWidth
              margin="normal"
              value={group_id}
              onChange={(e) => setGroupId(e.target.value)}
              required
              disabled
            />
            {groupProfilesLeft !== null && (
              <Typography sx={{ mt: 2 }}>
                {groupProfilesLeft} participants left to be created in this group.
              </Typography>
            )}
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
              Create
            </Button>
          </form>
        )}
      </Paper>
    </Container>
  );
}

export default ProfileForm;
