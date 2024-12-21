import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useHistory, Route, Switch } from 'react-router-dom';
import './App.css';
import LogoutButton from './LogoutButton';
import Admin from './Admin'; // Import the Admin component
import GroupList from './GroupList'; // Import GroupList component
import GroupForm from './GroupForm'; // Import GroupForm component
import ProfileForm from './ProfileForm'; // Import ProfileForm component
import ChatPage from './ChatPage'; // Import ChatPage component

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [message, setMessage] = useState('');
  const history = useHistory();
  const isLoggedIn = !!localStorage.getItem('token');

  useEffect(() => {
    fetch(`${API_URL}/protected`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Unauthorized');
      }
      return response.json();
    })
    .then(data => {
      if (data.message) {
        setMessage(data.message);
      } else {
        history.push('/login');
      }
    })
    .catch(() => {
      history.push('/login');
    });
  }, [history]);

  return (
    <Switch>
      <Route path="/admin">
        <Admin />
      </Route>
      <Route path="/groups/new">
        <GroupForm />
      </Route>
      <Route path="/groups/:id/edit">
        <GroupForm />
      </Route>
      <Route path="/groups/:groupId/chats">
        <ChatPage />
      </Route>
      <Route path="/groups">
        <GroupList />
      </Route>
      <Route path="/profiles/new">
        <ProfileForm />
      </Route>
      <Route path="/profiles/:id/edit">
        <ProfileForm />
      </Route>
      <Route path="/">
        <Container maxWidth="sm">
          {isLoggedIn && <LogoutButton />}
          <Box sx={{ textAlign: 'center', mt: 8 }}>
            <Typography variant="h2" component="h1" gutterBottom>
              Welcome to The Oval
            </Typography>
            <Typography variant="h5" component="p" gutterBottom>
              {message || 'Your beautiful landing page built with React and Material-UI'}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              {isLoggedIn && (
                <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/admin')}>
                  Admin Area
                </Button>
              )}
              <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/profiles/new')}>
                Get Started
              </Button>
              <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/profiles')}>
                View Profiles
              </Button>
              {!isLoggedIn && (
                <Button variant="outlined" color="primary" onClick={() => history.push('/login')}>
                  Login
                </Button>
              )}
            </Box>
          </Box>
        </Container>
      </Route>
    </Switch>
  );
}

export default App;