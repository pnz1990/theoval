/**
 * @file App.js
 * @description Root component handling global routes, authentication, and main layout.
 */
import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useHistory, Route, Switch } from 'react-router-dom';
import './App.css';
import LogoutButton from './LogoutButton';
import Admin from './Admin';
import GroupList from './GroupList';
import GroupForm from './GroupForm';
import ProfileForm from './ProfileForm';
import ChatPage from './ChatPage';
import MyGroups from './MyGroups';
import Login from './Login';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * @component App
 * @description Manages global state such as user login and routing to different pages.
 * @returns {JSX.Element}
 */
function App() {
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [userData, setUserData] = useState(null);
  const history = useHistory();

  const fetchUserData = async () => {
    try {
      const response = await fetch(`${API_URL}/users/me`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setUserData(data);
      } else {
        history.push('/login');
      }
    } catch (error) {
      history.push('/login');
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchUserData();
    } else {
      setUserData(null);
    }
  }, [isLoggedIn]);

  useEffect(() => {
    if (isLoggedIn) {
      const unlisten = history.listen(() => {
        fetchUserData();
      });
      return () => {
        unlisten();
      };
    }
  }, [history, isLoggedIn]);

  useEffect(() => {
    if (isLoggedIn) {
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
    }
  }, [history, isLoggedIn]);

  return (
    <Switch>
      <Route path="/admin">
        <Admin userData={userData} />
      </Route>
      <Route path="/groups/new">
        <GroupForm userData={userData} />
      </Route>
      <Route path="/groups/:id/edit">
        <GroupForm userData={userData} />
      </Route>
      <Route path="/groups/:groupId/chats">
        <ChatPage userData={userData} />
      </Route>
      <Route path="/groups">
        <GroupList userData={userData} />
      </Route>
      <Route path="/profiles/new">
        <ProfileForm userData={userData} />
      </Route>
      <Route path="/mygroups">
        <MyGroups userData={userData} />
      </Route>
      <Route path="/profiles/:id/edit">
        <ProfileForm userData={userData} />
      </Route>
      <Route path="/login">
        <Login setIsLoggedIn={setIsLoggedIn} />
      </Route>
      <Route path="/">
        <Container maxWidth="sm">
          {isLoggedIn && <LogoutButton setIsLoggedIn={setIsLoggedIn} />}
          <Box sx={{ textAlign: 'center', mt: 8 }}>
            <Typography variant="h2" component="h1" gutterBottom>
              Welcome to The Oval
            </Typography>
            <Typography variant="h5" component="p" gutterBottom>
              {message || 'Your beautiful landing page built with React and Material-UI'}
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              {isLoggedIn && (
                <>
                  <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/admin')}>
                    Admin Area
                  </Button>
                  <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/mygroups')}>
                    My Groups
                  </Button>
                </>
              )}
              {!isLoggedIn && (
                <Button variant="outlined" color="primary" onClick={() => history.push('/login')}>
                  Login
                </Button>
              )}
              {isLoggedIn && (
                <Button variant="contained" color="primary" sx={{ mr: 2 }} onClick={() => history.push('/profiles/new')}>
                  Get Started
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