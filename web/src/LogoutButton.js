import React from 'react';
import { Button, Box } from '@mui/material';
import { useHistory } from 'react-router-dom';

function LogoutButton({ setIsLoggedIn }) {
  const history = useHistory();

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    history.push('/login');
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
      <Button variant="contained" color="primary" onClick={handleLogout}>
        Logout
      </Button>
    </Box>
  );
}

export default LogoutButton;
