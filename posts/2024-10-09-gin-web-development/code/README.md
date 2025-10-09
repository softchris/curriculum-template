# Gin API Demo

A comprehensive example of building production-ready APIs with Go and the Gin framework.

## Features

- RESTful API design with proper HTTP methods and status codes
- Comprehensive middleware system (logging, authentication, rate limiting, error handling)
- Request binding and validation with custom validation rules
- Structured error handling with consistent response formats
- File upload handling with validation
- Production-ready configuration and security headers

## Project Structure

```
gin-api-demo/
├── main.go              # Application entry point
├── models/              # Data models and request/response types
├── handlers/            # HTTP handlers
├── middleware/          # Custom middleware
├── errors/              # Error definitions and handling
└── go.mod              # Module definition
```

## Getting Started

1. Install dependencies:
```bash
go mod tidy
```

2. Run the application:
```bash
go run main.go
```

3. The server will start on port 8080

## API Endpoints

### Public Endpoints

- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/health` - Health check
- `POST /api/v1/users/register` - User registration
- `GET /api/v1/users/search` - Search users
- `POST /api/v1/files/upload` - File upload

### Protected Endpoints (require authentication)

- `GET /api/v1/users` - Get all users (with pagination)
- `POST /api/v1/users` - Create a new user
- `GET /api/v1/users/:id` - Get user by ID
- `PUT /api/v1/users/:id` - Update user
- `DELETE /api/v1/users/:id` - Delete user

## Authentication

For protected endpoints, include the Authorization header:
```
Authorization: Bearer valid-demo-token
```

## Example Requests

### Create User
```bash
curl -X POST http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer valid-demo-token" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }'
```

### Search Users
```bash
curl "http://localhost:8080/api/v1/users/search?q=john&limit=10&sort=name&order=asc"
```

### Register User
```bash
curl -X POST http://localhost:8080/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "date_of_birth": "1990-01-01T00:00:00Z",
    "agree_to_terms": true
  }'
```

## Features Demonstrated

### Middleware
- Custom logging with request duration
- JWT-style authentication (simplified)
- Rate limiting with sliding window
- Error handling with structured responses
- Panic recovery with stack trace logging

### Request Handling
- JSON binding and validation
- Query parameter binding
- Form data binding for file uploads
- Custom validation rules
- Proper error responses

### Production Readiness
- Structured error handling
- Comprehensive logging
- Security headers
- Input validation
- Rate limiting
- Health checks

## Notes

This is a demonstration project. In production, you should:
- Use a real database instead of in-memory storage
- Implement proper JWT token validation
- Use secure password hashing (bcrypt)
- Add comprehensive tests
- Implement proper logging (structured logging)
- Add metrics and monitoring
- Use environment-based configuration