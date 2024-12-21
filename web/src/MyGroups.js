import React from 'react';
import { Container, Typography, Box, List, ListItem, ListItemText, Paper, Breadcrumbs, Link } from '@mui/material';
import { useHistory } from 'react-router-dom';

function MyGroups({ userData }) { // Added userData as a prop
  const history = useHistory();

  console.log('MyGroups: Received userData:', userData); // Debugging log
  console.log('MyGroups: userData.groups:', userData?.groups); // Debugging log

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
            console.log('Rendering group:', group, 'with profile_id:', profile_id); // Debugging log
            return (
              <ListItem 
                button 
                key={group.id} 
                onClick={() => history.push(`/groups/${group.id}/chats?profile_id=${profile_id}`)} // Updated redirect
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