import React from 'react';
import { Container, Typography, Box, List, ListItem, ListItemText, Paper, Breadcrumbs, Link } from '@mui/material';
import { useHistory } from 'react-router-dom';

/**
 * @file MyGroups.js
 * @description Displays a list of groups the current user has joined.
 */

/**
 * @component MyGroups
 * @description Renders "My Groups" page. Shows a message if no groups found.
 * @param {object} props - React props.
 * @param {object} props.userData - Contains user details and their groups.
 * @returns {JSX.Element}
 */
function MyGroups({ userData }) {
  const history = useHistory();

  const handleProfileClick = (profile) => {
    history.push(`/groups/${profile.group_id}/chats?profile_id=${profile.id}`);
  };

  if (!userData || !userData.groups || userData.groups.length === 0) {
    return (
      <Container maxWidth="sm">
        <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
          <Box sx={{ textAlign: 'center', mb: 2 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              My Groups
            </Typography>
            <Typography variant="body1">
              You have not joined any groups yet.
            </Typography>
          </Box>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
        <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2, p: 1 }}>
          <Link color="inherit" onClick={() => history.push('/')} sx={{ cursor: 'pointer' }}>
            Home
          </Link>
          <Typography color="textPrimary">My Groups</Typography>
        </Breadcrumbs>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            My Groups
          </Typography>
        </Box>
        <List>
          {userData.groups.map(group => {
            const userProfile = userData.profiles.find(p => p.group_id === group.id);
            const profile_id = userProfile ? userProfile.id : null;
            return (
              <ListItem 
                button 
                key={group.id} 
                onClick={() => handleProfileClick(userProfile)}
              >
                <ListItemText primary={group.name} secondary={`Max Profiles: ${group.max_profiles}`} />
              </ListItem>
            );
          })}
        </List>
      </Paper>
    </Container>
  );
}

export default MyGroups;