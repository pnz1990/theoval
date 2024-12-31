/**
 * @file ChatPage.js
 * @description Manages chat sessions within a group, including real-time messages and profile viewing.
 */
import React, { useState, useEffect, useRef } from 'react';
import { Container, Box, List, ListItem, ListItemText, TextField, Button, Typography, Paper, Avatar, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';
import { useParams } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

/**
 * @component ChatPage
 * @description Renders chats and messages for a specific group with profile previews.
 * @param {object} props - React props.
 * @param {object} props.userData - Contains profiles and other user information.
 * @param {function} props.fetchUserData - Function to fetch user data.
 * @returns {JSX.Element}
 */
function ChatPage({ userData, fetchUserData }) {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedChat, setSelectedChat] = useState(null);
  const { groupId } = useParams();
  
  // Retrieve the current user's profile for the selected group from userData
  const currentProfile = userData 
    ? userData.profiles.find(p => p.group_id === groupId) 
    : null;
  const profileId = currentProfile ? currentProfile.id : null;
  const [open, setOpen] = useState(false);
  const [newChatName, setNewChatName] = useState('');
  const [profilesModalOpen, setProfilesModalOpen] = useState(false);
  const [selectedProfileDetails, setSelectedProfileDetails] = useState(null);
  const [profiles, setProfiles] = useState([]);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handleViewProfiles = () => {
    setSelectedProfileDetails(null);
    setProfilesModalOpen(true);
  };
  const handleCloseProfilesModal = () => {
    setProfilesModalOpen(false);
  };
  const handleSelectProfile = (profile) => {
    setSelectedProfileDetails(profile);
  };

  const handleBackToProfileList = () => {
    setSelectedProfileDetails(null);
  };

  const fetchChats = async () => {
    const response = await fetch(`${API_URL}/groups/${groupId}/chats?profile_id=${profileId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    const data = await response.json();
    setChats(data);
  };

  const fetchProfiles = async () => {
    try {
      console.log('Fetching profiles for groupId:', groupId, 'profileId:', profileId);
      if (!groupId) {
        console.error('groupId is undefined.');
        return;
      }
      const response = await fetch(`${API_URL}/groups/${groupId}/profiles`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        console.log('Profiles data received:', data);
        setProfiles(data.profiles || data); // Adjust based on actual API response structure
      } else {
        console.error('Failed to fetch profiles:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching profiles:', error);
    }
  };

  /**
   * @function handleCreateChat
   * @description Creates a new chat thread in the current group.
   */
  const handleCreateChat = async () => {
    if (newChatName.trim() === '') return;

    try {
      const response = await fetch(`${API_URL}/groups/${groupId}/chats`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ name: newChatName })
      });

      if (response.ok) {
        const chat = await response.json();
        setChats([...chats, chat]);
        setSelectedChat(chat);
        setNewChatName('');
        handleClose();
        await fetchChats();
      } else {
        console.error('Failed to create chat:', response.statusText);
      }
    } catch (error) {
      console.error('Error creating chat:', error);
    }
  };

  // Fetch user data once when the component mounts
  useEffect(() => {
    fetchUserData();
    fetchProfiles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Removed dependency on fetchUserData

  // Fetch chats and profiles when userData or groupId changes
  useEffect(() => {
    if (userData) {
      fetchChats();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [groupId, userData]); // Removed profileId to prevent unnecessary re-fetches

  useEffect(() => {
    if (selectedChat) {
      const fetchMessages = () => {
        fetch(`${API_URL}/chats/${selectedChat.id}/messages`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        .then(response => response.json())
        .then(data => setMessages(data));
      };

      fetchMessages();
      const interval = setInterval(fetchMessages, 1000);
      return () => clearInterval(interval);
    }
  }, [selectedChat]);

  /**
   * @function handleSendMessage
   * @description Sends a new message in the selected chat thread.
   */
  const handleSendMessage = async () => {
    if (newMessage.trim() === '') return;

    const response = await fetch(`${API_URL}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({ content: newMessage, chat_id: selectedChat.id, profile_id: profileId })
    });

    if (response.ok) {
      const message = await response.json();
      setMessages([...messages, message]);
      setNewMessage('');
      fetch(`${API_URL}/chats/${selectedChat.id}/messages`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => response.json())
      .then(data => setMessages(data));
    }
  };

  const getProfile = (profileId) => {
    return profiles.find(p => p.id === profileId) || { name: 'Unknown', picture: '' };
  };

  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <Container sx={{ width: '100%', height: '80vh' }}>
      <Box sx={{ display: 'flex', width: '100%', height: '100%', mt: 4 }}>
        <Paper sx={{ width: '25%', overflow: 'hidden', bgcolor: 'background.paper', borderRadius: 2, boxShadow: 3 }}>
          <Button variant="contained" color="primary" onClick={handleViewProfiles} sx={{ m: 2 }}>
            Profiles
          </Button>
          <Button variant="contained" color="primary" onClick={handleOpen} sx={{ m: 2 }}>
            Add Chat
          </Button>
          <List>
            {chats.map(chat => (
              <ListItem 
                button 
                key={chat.id} 
                onClick={() => setSelectedChat(chat)} 
                sx={{ '&:hover': { bgcolor: 'primary.light' }, borderRadius: 1, m: 1 }}
              >
                <ListItemText primary={chat.name} />
              </ListItem>
            ))}
          </List>
        </Paper>
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', ml: 2 }}>
          <Paper sx={{ flexGrow: 1, overflow: 'auto', p: 2, bgcolor: 'background.paper', borderRadius: 2, boxShadow: 3 }}>
            {selectedChat ? (
              <>
                <Typography variant="h5" gutterBottom>{selectedChat.name}</Typography>
                <Box sx={{ mb: 2, maxHeight: '70vh', overflowY: 'auto' }}>
                  {messages.map(message => {
                    const profile = getProfile(message.profile_id);
                    const isOwnMessage = message.profile_id === profileId;
                    return (
                      <Box key={message.id} sx={{ mb: 1, p: 1, borderRadius: 1, bgcolor: isOwnMessage ? 'green.100' : 'grey.100', display: 'flex', alignItems: 'center' }}>
                        <Avatar src={profile.picture} alt={profile.name} sx={{ mr: 2 }} />
                        <Box>
                          <Typography variant="body2" color="textSecondary">
                            <strong>{profile.name}</strong> ({new Date(message.created_at).toLocaleString()}):
                          </Typography>
                          <Typography variant="body1">{message.content}</Typography>
                        </Box>
                      </Box>
                    );
                  })}
                  <div ref={messagesEndRef} />
                </Box>
              </>
            ) : (
              <Typography variant="h6" gutterBottom>Select a chat to view messages</Typography>
            )}
          </Paper>
          {selectedChat && (
            <Box sx={{ display: 'flex', mt: 2 }}>
              <TextField
                fullWidth
                variant="outlined"
                placeholder="Type a message"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                sx={{ bgcolor: 'background.paper', borderRadius: 1 }}
              />
              <Button variant="contained" color="primary" onClick={handleSendMessage} sx={{ ml: 2, borderRadius: 1 }}>
                Send
              </Button>
            </Box>
          )}
        </Box>
      </Box>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Create New Chat</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Chat Name"
            type="text"
            fullWidth
            value={newChatName}
            onChange={(e) => setNewChatName(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleCreateChat} color="primary">
            Create
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={profilesModalOpen} onClose={handleCloseProfilesModal}>
        <DialogTitle>View Profiles</DialogTitle>
        <DialogContent>
          {!selectedProfileDetails ? (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: 2 }}>
              {profiles.map((p) => (
                <Box key={p.id} onClick={() => handleSelectProfile(p)} sx={{ cursor: 'pointer', textAlign: 'center' }}>
                  <Avatar src={p.picture} alt={p.name} sx={{ width: 56, height: 56, mx: 'auto' }} />
                  <Typography variant="body2">{p.name}</Typography>
                </Box>
              ))}
            </Box>
          ) : (
            <Box sx={{ textAlign: 'center' }}>
              <Button onClick={handleBackToProfileList} color="primary">
                Back to Profiles
              </Button>
              <Avatar src={selectedProfileDetails.picture} alt={selectedProfileDetails.name} sx={{ width: 100, height: 100, mx: 'auto' }} />
              <Typography variant="h6">{selectedProfileDetails.name}</Typography>
              <Typography variant="body1">{selectedProfileDetails.bio}</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseProfilesModal} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default ChatPage;
