# Event Tracking API

This is a FastAPI-based event tracking system with PostgreSQL. 
It provides RESTful endpoints to create, retrieve, update, and delete events. The application supports filtering, pagination, and is fully containerized with Docker Compose.

## Getting Started

### Prerequisites
- **Docker & Docker Compose:** Required for running the application in containers.
- **Python 3.10+:** (Optional) If you prefer to run the app locally without Docker.

### Clone the Repository
Clone this repository to your local machine:
```sh
git clone https://github.com/your-repo.git
cd your-repo
```

##  Setup & Run with Docker
Build and Start the Containers:
From the project root (where docker-compose.yml is located), run:
```sh
docker-compose up --build
```
This command builds the Docker images and starts the containers for both the FastAPI app and the PostgreSQL database.

Wait for Services to be Ready:
The FastAPI container uses netcat (nc) to wait until the PostgreSQL service is ready. 
Look for the "Waiting for db" message in the logs before the app starts.


## Access the API
Open your browser and navigate to http://localhost:8000 to see the welcome message:
"Welcome to my Tracking System Event"
Visit http://localhost:8000/docs to access the interactive Swagger UI for testing the API endpoints.

## Running the Tests
The project includes tests to verify API functionality.
Inside the Docker Container:
Execute the following command to run pytest:
```sh
docker exec -it fastapi_container pytest /app/tests
```
Or locally:
```sh
pytest
```

## Additional Details
Pagination - The GET /events endpoint supports pagination with the following query parameters:
skip: Number of records to skip (default is 0, must be non-negative).
limit: Maximum number of records to return (default is 100, allowed range 1–1000).
Example usage:
```sh
/events?skip=10&limit=5
```
This will skip the first 10 events and return the next 5 events.

Example Event Payload
When creating an event (via POST /events), you can use a payload similar to:

```sh
{
  "type": "user_signup",
  "timestamp": "2025-02-23T14:30:00Z",
  "payload": {
    "username": "omer",
    "email": "omer@example.com",
    "referral": "friend_invite"}
}
```

## Logging & Error Handling
The API logs errors (e.g., during event creation or retrieval) and returns appropriate HTTP status codes for issues such as internal server errors or resource not found.

