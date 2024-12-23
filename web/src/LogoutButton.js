/**
 * @file LogoutButton.js
 * @description Provides a button to clear stored authentication tokens and log out the user.
 */
import React from 'react';
import { Button, Box } from '@mui/material';
import { useHistory } from 'react-router-dom';

/**
 * @component LogoutButton
 * @description Renders a logout button that resets login state and navigates to the login page.
 * @param {object} props - React props.
 * @param {function} props.setIsLoggedIn - Sets the current login state.
 * @returns {JSX.Element}
 */
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
