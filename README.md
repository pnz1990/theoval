# The Oval

A personal project inspired by the TV reality show "The Circle." In "The Oval," users create anonymous profiles, engage in real-time chats, build alliances, and cast votes to determine the most influential player. The platform emphasizes privacy, strategic interactions, and dynamic gameplay, offering features such as private messaging and a robust voting system to enhance user engagement.

## Features

- **User Registration and Authentication**: Secure user registration and login using JWT authentication.
- **Group Management**: Create, update, delete, and retrieve groups where users can interact.
- **Profile Management**: Within each group, users can create, update, delete, and retrieve profiles to represent themselves anonymously.
- **Real-Time Chat**: Engage in real-time conversations within specific chats or private messages.
- **Voting System**: Cast votes to eliminate players, influencing the outcome of the game.
- **Alliance Building**: Form alliances with other users to strategize and collaborate.
- **Responsive Design**: Accessible and user-friendly interface across various devices.

## API Endpoints

Detailed documentation of all API endpoints, including expected parameters and responses.

### Authentication

- **Register a New User**
  
  `POST /register`
  
  - **Parameters (JSON Body)**:
    - `email` (string, required): User's email address.
    - `password` (string, required): User's password (must be strong).
  
  - **Responses**:
    - `201 Created`: User registered successfully.
    - `400 Bad Request`: User already exists or weak password.

- **User Login**
  
  `POST /login`
  
  - **Parameters (JSON Body)**:
    - `email` (string, required): User's email address.
    - `password` (string, required): User's password.
  
  - **Responses**:
    - `200 OK`: Returns JWT token.
    - `401 Unauthorized`: Invalid credentials.

### Groups

- **Create a New Group**
  
  `POST /groups` *(Requires JWT)*
  
  - **Parameters (JSON Body)**:
    - `name` (string, required): Name of the group.
    - `picture` (string, optional): URL to the group's picture.
    - `max_profiles` (integer, required): Maximum number of profiles allowed in the group.
  
  - **Responses**:
    - `201 Created`: Returns the ID of the created group.
    - `400 Bad Request`: Invalid group data.

- **Retrieve All Groups**
  
  `GET /groups` *(Requires JWT)*
  
  - **Responses**:
    - `200 OK`: Returns a list of all groups.

- **Retrieve a Specific Group**
  
  `GET /groups/<group_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `group_id` (string, required): ID of the group.
  
  - **Responses**:
    - `200 OK`: Returns group details.
    - `404 Not Found`: Group does not exist.

- **Update a Group**
  
  `PUT /groups/<group_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `group_id` (string, required): ID of the group.
  
  - **Parameters (JSON Body)**:
    - `name` (string, optional): New name for the group.
    - `picture` (string, optional): New picture URL.
    - `max_profiles` (integer, optional): New maximum number of profiles.
  
  - **Responses**:
    - `200 OK`: Returns the ID of the updated group.
    - `400 Bad Request`: Invalid update data.
    - `404 Not Found`: Group does not exist.

- **Delete a Group**
  
  `DELETE /groups/<group_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `group_id` (string, required): ID of the group.
  
  - **Responses**:
    - `204 No Content`: Group deleted successfully.
    - `404 Not Found`: Group does not exist.

### Profiles

- **Create a New Profile**
  
  `POST /profiles` *(Requires JWT)*
  
  - **Parameters (JSON Body)**:
    - `name` (string, required): Name of the profile.
    - `picture` (string, optional): URL to the profile's picture.
    - `bio` (string, optional): Biography of the profile.
    - `group_id` (string, required): ID of the group the profile belongs to.
  
  - **Responses**:
    - `201 Created`: Returns the ID of the created profile.
    - `400 Bad Request`: Invalid profile data or duplicate profile name.

- **Retrieve All Profiles**
  
  `GET /profiles` *(Requires JWT)*
  
  - **Responses**:
    - `200 OK`: Returns a list of all profiles.

- **Retrieve a Specific Profile**
  
  `GET /profiles/<profile_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `profile_id` (string, required): ID of the profile.
  
  - **Responses**:
    - `200 OK`: Returns profile details.
    - `404 Not Found`: Profile does not exist.

- **Update a Profile**
  
  `PUT /profiles/<profile_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `profile_id` (string, required): ID of the profile.
  
  - **Parameters (JSON Body)**:
    - `name` (string, optional): New name for the profile.
    - `picture` (string, optional): New picture URL.
    - `bio` (string, optional): New biography.
    - `group_id` (string, optional): New group ID.
  
  - **Responses**:
    - `200 OK`: Returns the ID of the updated profile.
    - `400 Bad Request`: Invalid update data.
    - `404 Not Found`: Profile does not exist.

- **Delete a Profile**
  
  `DELETE /profiles/<profile_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `profile_id` (string, required): ID of the profile.
  
  - **Responses**:
    - `204 No Content`: Profile deleted successfully.
    - `404 Not Found`: Profile does not exist.

### Chats

- **Create a New Chat**
  
  `POST /groups/<group_id>/chats` *(Requires JWT)*
  
  - **Parameters**:
    - `group_id` (string, required): ID of the group.
  
  - **Parameters (JSON Body)**:
    - `name` (string, required): Name of the chat.
    - `participant_ids` (array of strings, optional): IDs of profiles to participate in the chat.
  
  - **Responses**:
    - `201 Created`: Returns the ID of the created chat.
    - `400 Bad Request`: Invalid chat data.
    - `404 Not Found`: Group does not exist.

- **Retrieve All Chats in a Group**
  
  `GET /groups/<group_id>/chats` *(Requires JWT)*
  
  - **Parameters**:
    - `group_id` (string, required): ID of the group.
  
  - **Query Parameters (Optional)**:
    - `profile_id` (string): Filter chats that a specific profile is part of.
  
  - **Responses**:
    - `200 OK`: Returns a list of chats.
    - `404 Not Found`: Group does not exist.

- **Retrieve a Specific Chat**
  
  `GET /chats/<chat_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `chat_id` (string, required): ID of the chat.
  
  - **Responses**:
    - `200 OK`: Returns chat details.
    - `404 Not Found`: Chat does not exist.

- **Update a Chat**
  
  `PUT /chats/<chat_id>` *(Requires JWT)*
  
  - **Parameters**:
    - `chat_id` (string, required): ID of the chat.
  
  - **Parameters (JSON Body)**:
    - `name` (string, optional): New name for the chat.
    - `participant_ids` (array of strings, optional): Updated list of participant IDs.
  
  - **Responses**:
    - `200 OK`: Returns the ID of the updated chat.
    - `400 Bad Request`: Invalid update data.
    - `404 Not Found`: Chat does not exist.

### Messages

- **Create a New Message**
  
  `POST /messages` *(Requires JWT)*
  
  - **Parameters (JSON Body)**:
    - `content` (string, required): Content of the message.
    - `chat_id` (string, required): ID of the chat.
    - `profile_id` (string, required): ID of the profile sending the message.
  
  - **Responses**:
    - `201 Created`: Returns the ID of the created message.
    - `400 Bad Request`: Invalid message data.
    - `404 Not Found`: Chat or profile does not exist.

- **Retrieve All Messages in a Chat**
  
  `GET /chats/<chat_id>/messages` *(Requires JWT)*
  
  - **Parameters**:
    - `chat_id` (string, required): ID of the chat.
  
  - **Responses**:
    - `200 OK`: Returns a list of messages.
    - `404 Not Found`: Chat does not exist.

## Setup

### Prerequisites

- **Docker**: Ensure Docker is installed on your system. [Download Docker](https://www.docker.com/get-started)
- **Docker Compose**: Comes bundled with Docker Desktop. Verify installation with `docker-compose --version`.

### Running the Application

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/yourusername/theoval.git
    cd theoval
    ```

2. **Export Environment Variables**:

    Create a `.env` file or use the provided `set_env.sh` script to set necessary environment variables.

    ```sh
    source set_env.sh
    ```

3. **Build and Start Services Using Docker Compose**:

    ```sh
    docker-compose up --build
    ```

4. **Access the Application**:

    The application will be available at `http://localhost:5000`.

### Building the Application

To build the application manually without running the services:

1. **Navigate to the Project Directory**:

    ```sh
    cd theoval
    ```

2. **Build Docker Images**:

    ```sh
    docker-compose build
    ```

3. **Run Services**:

    ```sh
    docker-compose up
    ```

### Testing the Application

1. **Stop Running Services** (if any):

    ```sh
    docker-compose down
    ```

2. **Run Tests Using Docker Compose**:

    ```sh
    docker-compose run test
    ```

   This command executes the test suite defined in the project to ensure all functionalities work as expected.

## Running Tests

1. **Ensure Services Are Stopped**:

    ```sh
    docker-compose down
    ```

2. **Execute Test Suite**:

    ```sh
    docker-compose run test
    ```

   This will run all tests using the testing environment configured with in-memory SQLite.

## License

This project is licensed under the MIT License.