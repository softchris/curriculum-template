# Task Management API

A RESTful API for managing tasks built with Go's standard library. This project demonstrates HTTP fundamentals including proper status codes, request handling, JSON processing, and middleware implementation.

## Features

- CRUD operations for tasks
- JSON request/response handling
- Query parameter filtering
- Middleware for logging, CORS, and security
- Comprehensive error handling
- In-memory data storage
- Unit tests

## API Endpoints

### Tasks
- `GET /tasks` - Get all tasks (supports `?completed=true/false` filter)
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a specific task
- `DELETE /tasks/{id}` - Delete a specific task

### Health Check
- `GET /health` - Health check endpoint

## Running the Application

```bash
# Start the server
go run main.go

# Run tests
go test ./tests/...
```

The server will start on `http://localhost:8080`.

## Example Usage

### Create a task
```bash
curl -X POST http://localhost:8080/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Go","description":"Study HTTP fundamentals"}'
```

### Get all tasks
```bash
curl http://localhost:8080/tasks
```

### Update a task
```bash
curl -X PUT http://localhost:8080/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

### Delete a task
```bash
curl -X DELETE http://localhost:8080/tasks/1
```

## Project Structure

- `main.go` - Main application entry point
- `handlers/tasks.go` - Task HTTP handlers
- `middleware/middleware.go` - HTTP middleware functions
- `types/task.go` - Data structures and types
- `tests/main_test.go` - Unit tests