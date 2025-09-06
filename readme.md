# Microservices Authorization Project

This project demonstrates a **microservices-based architecture** for handling user authorization.
It consists of two main services that communicate with each other via **RabbitMQ**. Also media service for storing media files.

## Services

### User Service
- Manages user data (registration, profile, etc.).
- Publishes events (e.g., `user.created`) when a new user is created.

### Auth Service
- Handles authentication and authorization logic.
- Listens to user-related events from the **User Service**.
- Stores and validates credentials, manages login and access control.

### Media Service
- Handles media files (e.g., images, videos, etc.)
- Stores media files in a cloud storage (e.g., Amazon S3).

## Communication Flow

1. A new user registers in the **User Service**.
2. The service publishes a `user.created` event to RabbitMQ.
3. The **Auth Service** consumes this event and creates corresponding authentication data.

## Tech Stack

- **FastAPI** – web framework for building services
- **RabbitMQ** – message broker for asynchronous communication
- **PostgreSQL** – persistence layer
- **Docker Compose** – container orchestration
- **Pytest** – testing framework
- **S3** – cloud object storage for media files
## Project Structure

├── auth-service/ # Authentication service
├── user-service/ # User service
├── media-service/ # Media service
├── docker-compose.yml # RabbitMQ + databases


## Running the Project

Clone the repository:

```bash
git clone https://github.com/aibert-enni/fastapi-monorepo.git
```

Start infrastructure (RabbitMQ, databases):

```bash
docker compose up -d
```

Start services:

Start user service:
```bash
cd user_service
docker compose up -d
```

Start auth service:
```bash
cd auth_service
docker compose up -d
```

Start media service:
```bash
cd media_service
docker compose up -d
```

## Testing
### User test
Up docker:
```bash
cd user_service/tests
docker compose up
```
Run tests:
```bash
cd user_service/tests
python -m pytest
```
### Auth test
Up docker:
```bash
cd auth_service/tests
docker compose up
```
Run tests:
```bash
cd auth_service/tests
python -m pytest
```
## Documentation

User API doc: http://localhost:8000/docs
Auth API doc: http://localhost:8001/docs
Media API doc: http://localhost:8002/docs

RabbitMQ management UI: http://localhost:15672
