import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './index.css';
import App from './App';
import Login from './Login';
import Register from './Register';
import Admin from './Admin';
import GroupList from './GroupList'; // Import GroupList component
import GroupForm from './GroupForm'; // Import GroupForm component
import ProfileForm from './ProfileForm'; // Import ProfileForm component
import ChatPage from './ChatPage'; // Import ChatPage component
import ProfileList from './ProfileList'; // Import ProfileList component

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/admin" component={Admin} />
        <Route path="/groups/new" component={GroupForm} />
        <Route path="/groups/:id/edit" component={GroupForm} />
        <Route path="/groups/:groupId/chats" component={ChatPage} />
        <Route path="/groups" component={GroupList} />
        <Route path="/profiles/new" component={ProfileForm} />
        <Route path="/profiles" component={ProfileList} />
        <Route path="/" component={App} />
      </Switch>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);