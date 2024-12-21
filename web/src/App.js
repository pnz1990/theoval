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
import MyGroups from './MyGroups';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [message, setMessage] = useState('');
  const [userData, setUserData] = useState(null); // Added state for user data
  const history = useHistory();
  const isLoggedIn = !!localStorage.getItem('token');

  useEffect(() => {
    const fetchUserData = async () => { // Added function to fetch user data
      try {
        const response = await fetch(`${API_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          console.log('App: Fetched userData:', data);
          setUserData(data);
        } else {
          console.error('App: Failed to fetch userData:', response.statusText);
          history.push('/login');
        }
      } catch (error) {
        console.error('App: Error fetching user data:', error);
        history.push('/login');
      }
    };

    if (isLoggedIn) {
      fetchUserData(); // Fetch user data if logged in
    }
  }, [history, isLoggedIn]);

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
        <Admin userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/groups/new">
        <GroupForm userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/groups/:id/edit">
        <GroupForm userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/groups/:groupId/chats">
        <ChatPage userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/groups">
        <GroupList userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/profiles/new">
        <ProfileForm userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/mygroups">
        <MyGroups userData={userData} /> {/* Passed userData as prop */}
      </Route>
      <Route path="/profiles/:id/edit">
        <ProfileForm userData={userData} /> {/* Passed userData as prop */}
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
              <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/mygroups')}>
                My Groups
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