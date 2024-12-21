# The Oval

The Oval is a web application that allows users to register, log in, create groups, and create profiles within those groups. It uses Flask for the backend and PostgreSQL as the database.

## Features

- User registration and login with JWT authentication
- Create, update, delete, and retrieve groups
- Create, update, delete, and retrieve profiles within groups

## Setup

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/theoval.git
    cd theoval
    ```

2. Export the environment variables:

    ```sh
    source set_env.sh
    ```

3. Build and start the services using Docker Compose:

    ```sh
    docker-compose up --build
    ```

4. The application will be available at `http://localhost:5000`.

### Running Tests

1. Ensure the services are stopped if they are running:

    ```sh
    docker-compose down
    ```

2. Run the tests using Docker Compose:

    ```sh
    docker-compose run test
    ```

## API Endpoints

### Authentication

- `POST /register`: Register a new user
- `POST /login`: Log in a user and receive a JWT token

### Groups

- `POST /groups`: Create a new group (requires JWT token)
- `GET /groups`: Retrieve all groups (requires JWT token)
- `GET /groups/<group_id>`: Retrieve a specific group by ID (requires JWT token)
- `PUT /groups/<group_id>`: Update a specific group by ID (requires JWT token)
- `DELETE /groups/<group_id>`: Delete a specific group by ID (requires JWT token)

### Profiles

- `POST /profiles`: Create a new profile within a group (requires JWT token)
- `GET /profiles`: Retrieve all profiles (requires JWT token)
- `GET /profiles/<profile_id>`: Retrieve a specific profile by ID (requires JWT token)
- `PUT /profiles/<profile_id>`: Update a specific profile by ID (requires JWT token)
- `DELETE /profiles/<profile_id>`: Delete a specific profile by ID (requires JWT token)

## License

This project is licensed under the MIT License.