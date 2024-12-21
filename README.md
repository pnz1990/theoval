# The Oval

The Oval is a comprehensive platform designed to facilitate group management, profile creation, and real-time chat functionalities. It serves as a centralized hub for users to create profiles, join groups, and engage in meaningful conversations within their communities.

## Features

- **User Authentication:** Secure registration and login with JWT-based authentication.
- **Group Management:** Create, update, and delete groups with customizable settings.
- **Profile Creation:** Users can create and manage multiple profiles within different groups.
- **Real-Time Chat:** Engage in real-time conversations within group-specific chats.
- **Admin Interface:** Dedicated admin pages for managing groups and profiles independently of user data.

## API Documentation

### Authentication

#### Register a New User

- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Registers a new user with an email and password.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123"
  }
  ```
- **Responses:**
  - `201 Created`: User registered successfully.
    ```json
    {
      "message": "User registered successfully"
    }
    ```
  - `400 Bad Request`: User already exists or password does not meet criteria.

#### Login

- **Endpoint:** `/login`
- **Method:** `POST`
- **Description:** Authenticates a user and returns a JWT token.
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123"
  }
  ```
- **Responses:**
  - `200 OK`: Returns JWT token.
    ```json
    {
      "token": "jwt.token.here"
    }
    ```
  - `401 Unauthorized`: Invalid credentials.

### User Information

#### Get Current User Info

- **Endpoint:** `/users/me`
- **Method:** `GET`
- **Description:** Retrieves information about the authenticated user, including profiles, groups, and chats.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns user information.
  - `400 Bad Request`: User not found.
  - `500 Internal Server Error`: Server error.

### Group Management

#### Create a New Group

- **Endpoint:** `/groups`
- **Method:** `POST`
- **Description:** Creates a new group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Group Name",
    "max_profiles": 10,
    "picture": "https://example.com/image.png"
  }
  ```
- **Responses:**
  - `201 Created`: Group created successfully.
    ```json
    {
      "id": "group-uuid"
    }
    ```
  - `400 Bad Request`: Invalid group data.

#### Get All Groups

- **Endpoint:** `/groups`
- **Method:** `GET`
- **Description:** Retrieves a list of all groups.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns a list of groups.

#### Get a Specific Group

- **Endpoint:** `/groups/<group_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns group details.
  - `404 Not Found`: Group does not exist.

#### Update a Group

- **Endpoint:** `/groups/<group_id>`
- **Method:** `PUT`
- **Description:** Updates information of a specific group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:** *(Same as Create Group)*
- **Responses:**
  - `200 OK`: Group updated successfully.
  - `400 Bad Request`: Invalid update data.
  - `404 Not Found`: Group does not exist.

#### Delete a Group

- **Endpoint:** `/groups/<group_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `204 No Content`: Group deleted successfully.
  - `404 Not Found`: Group does not exist.

### Profile Management

#### Check Existing Profile in Group

- **Endpoint:** `/profiles/check`
- **Method:** `POST`
- **Description:** Checks if the user already has a profile in a specific group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "group_id": "group-uuid"
  }
  ```
- **Responses:**
  - `200 OK`: No existing profile.
    ```json
    {
      "message": "No existing profile in this group"
    }
    ```
  - `400 Bad Request`: User already has a profile in the group.

#### Create a New Profile

- **Endpoint:** `/profiles`
- **Method:** `POST`
- **Description:** Creates a new profile within a group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Profile Name",
    "picture": "https://example.com/picture.png",
    "bio": "Short bio about the profile.",
    "group_id": "group-uuid"
  }
  ```
- **Responses:**
  - `201 Created`: Profile created successfully.
    ```json
    {
      "id": "profile-uuid",
      "name": "Profile Name",
      "picture": "https://example.com/picture.png",
      "bio": "Short bio about the profile.",
      "group_id": "group-uuid"
    }
    ```
  - `400 Bad Request`: Invalid profile data or user already has a profile in the group.

#### Get All Profiles

- **Endpoint:** `/profiles`
- **Method:** `GET`
- **Description:** Retrieves a list of all profiles.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns a list of profiles.

#### Get a Specific Profile

- **Endpoint:** `/profiles/<profile_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific profile.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns profile details.
  - `404 Not Found`: Profile does not exist.

### Chat Management

#### Create a New Chat

- **Endpoint:** `/groups/<group_id>/chats`
- **Method:** `POST`
- **Description:** Creates a new chat within a group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Chat Name",
    "participant_ids": ["profile-id-1", "profile-id-2"]
  }
  ```
- **Responses:**
  - `201 Created`: Chat created successfully.
    ```json
    {
      "id": "chat-uuid"
    }
    ```
  - `400 Bad Request`: Invalid chat data.

#### Get All Chats in a Group

- **Endpoint:** `/groups/<group_id>/chats`
- **Method:** `GET`
- **Description:** Retrieves all chats within a specific group.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Query Parameters:**
  - `profile_id` *(optional)*: Filter chats by profile participation.
- **Responses:**
  - `200 OK`: Returns a list of chats.

#### Get a Specific Chat

- **Endpoint:** `/chats/<chat_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific chat.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns chat details.
  - `404 Not Found`: Chat does not exist.

#### Update a Chat

- **Endpoint:** `/chats/<chat_id>`
- **Method:** `PUT`
- **Description:** Updates the name or participants of a specific chat.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "name": "Updated Chat Name",
    "participant_ids": ["profile-id-1", "profile-id-3"]
  }
  ```
- **Responses:**
  - `200 OK`: Chat updated successfully.
  - `400 Bad Request`: Invalid update data.
  - `404 Not Found`: Chat does not exist.

### Message Management

#### Create a New Message

- **Endpoint:** `/messages`
- **Method:** `POST`
- **Description:** Sends a new message in a chat.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Request Body:**
  ```json
  {
    "content": "Hello, world!",
    "chat_id": "chat-uuid",
    "profile_id": "profile-uuid"
  }
  ```
- **Responses:**
  - `201 Created`: Message sent successfully.
    ```json
    {
      "id": "message-uuid"
    }
    ```
  - `400 Bad Request`: Invalid message data.

#### Get All Messages in a Chat

- **Endpoint:** `/chats/<chat_id>/messages`
- **Method:** `GET`
- **Description:** Retrieves all messages within a specific chat.
- **Headers:**
  - `Authorization: Bearer <JWT_TOKEN>`
- **Responses:**
  - `200 OK`: Returns a list of messages.

## Installation

### Prerequisites

- **Backend:**
  - Python 3.8+
  - PostgreSQL
  - Virtual Environment Manager (e.g., `venv` or `conda`)

- **Frontend:**
  - Node.js 14+
  - npm or yarn

### Backend Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/theoval.git
   cd theoval/api
   ```

2. **Create and Activate Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Create a `.env` file in the `api` directory with the following:
     ```
     POSTGRES_USER=your_postgres_user
     POSTGRES_PASSWORD=your_postgres_password
     POSTGRES_DB=theoval_db
     JWT_SECRET_KEY=your_jwt_secret_key
     ```

5. **Initialize the Database:**
   ```bash
   python app.py
   ```

6. **Run the Backend Server:**
   ```bash
   python app.py
   ```

### Frontend Setup

1. **Navigate to Frontend Directory:**
   ```bash
   cd ../web
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure Environment Variables:**
   - Create a `.env` file in the `web` directory with the following:
     ```
     REACT_APP_API_URL=http://localhost:5001
     ```

4. **Run the Frontend Development Server:**
   ```bash
   npm start
   # or
   yarn start
   ```

## Usage

1. **Register a New User:**
   - Navigate to `/register` and create a new account.

2. **Login:**
   - Navigate to `/login` and authenticate using your credentials.

3. **Manage Groups:**
   - Access the Admin Area to create, update, or delete groups.

4. **Create Profiles:**
   - Create profiles within your groups to participate in chats.

5. **Join and Chat:**
   - Join groups and engage in real-time conversations within chat rooms.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature/YourFeature
   ```
3. **Commit Your Changes**
   ```bash
   git commit -m "Add Your Feature"
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/YourFeature
   ```
5. **Open a Pull Request**

Please ensure your code adheres to the project's coding standards and all tests pass.

## License

This project is licensed under the [MIT License](LICENSE).