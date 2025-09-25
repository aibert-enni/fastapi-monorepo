# Microservices Authorization Project

This project demonstrates a **microservices-based architecture** for handling user authorization.  
The services communicate with each other via **RabbitMQ**, while the **API Gateway** interacts with the services using **gRPC**.

## Services

### API Gateway
- Gateway between frontend and backend
- The communication between services is done via gRPC
- Admin endpoints

### User Service
- Manages user data (registration, profile, etc.).
- Publishes events (e.g., `user.created`) when a new user is created.
- There is outbox pattern for broker fallback messages, message sending implemented via celery schedule tasks for every 5 minutes

### Auth Service
- Handles authentication and authorization logic.
- Listens to user-related events from the **User Service**.
- Stores and validates credentials, manages login and access control.

### Media Service
- Handles media files (for now only images)
- Stores media files in a cloud storage (e.g., Amazon S3, Yandex storage).
- Allows users to upload avatars and get their URLs or delete.

## Communication Flow

1. A new user registers in the **User Service**.
2. The service publishes a `user.created` event to RabbitMQ.
3. The **Auth Service** consumes this event and creates corresponding authentication data.

## Tech Stack

- **FastAPI** – web framework for building services
- **gRPC** – inter-service communication
- **RabbitMQ** – message broker for asynchronous communication
- **PostgreSQL** – persistence layer
- **Celery** - task queue with scheduling
- **Docker Compose** – container orchestration
- **Pytest** – testing framework
- **Minio** – aws object storage for media files

## Demo / Test Server

A ready-to-use test server is available for quick evaluation of the project.(Only works api gateway and auth service because I'm not trump to maintain server for $$$)  
You can access the API Gateway documentation at:

https://enni-aibert.duckdns.org/docs

Admin account:
- username: admin
- password: admin1234

> ⚠️ Note: This server is for demonstration purposes only and should not be used in production. 

### API
<img width="1918" height="991" alt="Screenshot 2025-09-20 231516" src="https://github.com/user-attachments/assets/56d23a64-2a2b-4380-b3b5-37c1920d515b" />


## Running the Project

Clone the repository:

```bash
git clone https://github.com/aibert-enni/fastapi-monorepo.git
```

Create internal network for docker containers:
```bash
docker network create internal_network
```

Start services via Docker:

Start infrastructure (RabbitMQ):

```bash
docker compose up -d
```


Start auth service:
```bash
cd auth_service
docker compose up -d
```

Start user service:
```bash
cd user_service
docker compose up -d
```

Start media service:
```bash
cd media_service
docker compose up -d
```

Start api gateway:
```bash
cd api-gateway
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

### Media test
Up docker:
```bash
cd media_service/tests
docker compose up
```
Run tests:
```bash
cd media_service/tests
python -m pytest
```

## Documentation
API Gateway doc: http://localhost:8000/docs

RabbitMQ management UI: http://localhost:15672

Minio management UI: http://localhost:9001/login 
