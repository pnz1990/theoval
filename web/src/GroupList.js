import React, { useState, useEffect } from 'react';
import { Container, Typography, Box, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Paper, Divider, Breadcrumbs, Link } from '@mui/material';
import { useHistory } from 'react-router-dom';
import DeleteIcon from '@mui/icons-material/Delete';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function GroupList() { // Removed userData as a prop
  const [groups, setGroups] = useState([]);
  const history = useHistory();

  useEffect(() => { // Removed userData from dependency array
    console.log('GroupList: useEffect triggered');
    fetch(`${API_URL}/groups`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error fetching groups: ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('GroupList: Fetched groups:', data);
      setGroups(data);
    })
    .catch(error => {
      console.error('GroupList: Failed to fetch groups:', error);
    });
  }, []); // Dependency array is now empty

  const handleDelete = async (id) => {
    console.log(`GroupList: Deleting group with id ${id}`);
    try {
      const response = await fetch(`${API_URL}/groups/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        setGroups(groups.filter(group => group.id !== id));
        console.log(`GroupList: Deleted group with id ${id}`);
      } else {
        const errorData = await response.json();
        console.error(`GroupList: Failed to delete group: ${errorData.message}`);
      }
    } catch (error) {
      console.error('GroupList: Error deleting group:', error);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ p: 3, mt: 8 }}>
        <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2, p: 1 }}>
          <Link color="inherit" onClick={() => history.push('/admin')} sx={{ cursor: 'pointer' }}>
            Admin
          </Link>
          <Typography color="textPrimary">Groups</Typography>
        </Breadcrumbs>
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Groups
          </Typography>
          <Button variant="contained" color="primary" onClick={() => history.push('/groups/new')}>
            Create Group
          </Button>
        </Box>
        <Divider />
        <List>
          {groups.map(group => (
            <ListItem key={group.id} button onClick={() => history.push(`/groups/${group.id}/edit`)}>
              <ListItemText primary={`${group.name} (ID: ${group.id})`} secondary={`Max Profiles: ${group.max_profiles}`} />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(group.id)}>
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Paper>
    </Container>
  );
}

export default GroupList;
