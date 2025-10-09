# My First API with Gin

A beginner-friendly book API built with Go and the Gin framework.

## What This Demonstrates

This simple API shows the fundamental concepts of web development with Gin:

- Creating HTTP routes (GET, POST)
- Handling JSON requests and responses
- URL parameters for dynamic routes
- Basic error handling
- RESTful API design

## Getting Started

1. Make sure you have Go installed
2. Create a new directory and navigate to it:
```bash
mkdir my-first-api
cd my-first-api
```

3. Initialize a Go module:
```bash
go mod init my-first-api
```

4. Install Gin:
```bash
go get github.com/gin-gonic/gin
```

5. Copy the code from `main.go` and run:
```bash
go run main.go
```

6. Your API will be available at `http://localhost:8080`

## API Endpoints

### Get All Books
```bash
curl http://localhost:8080/books
```

### Get a Specific Book
```bash
curl http://localhost:8080/books/1
```

### Add a New Book
```bash
curl -X POST http://localhost:8080/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Building Web Apps with Go",
    "author": "Jeremy Saenz"
  }'
```

## Example Responses

### GET /books
```json
[
  {
    "id": 1,
    "title": "The Go Programming Language",
    "author": "Alan Donovan"
  },
  {
    "id": 2,
    "title": "Learning Go",
    "author": "Jon Bodner"
  }
]
```

### GET /books/1
```json
{
  "id": 1,
  "title": "The Go Programming Language",
  "author": "Alan Donovan"
}
```

### POST /books (Success)
```json
{
  "id": 3,
  "title": "Building Web Apps with Go",
  "author": "Jeremy Saenz"
}
```

### Error Response (Book Not Found)
```json
{
  "error": "Book not found"
}
```

## What You've Learned

By building this simple API, you've learned:

1. **Basic Gin Setup**: How to create a Gin router and start a server
2. **Routing**: How to define routes for different HTTP methods and URLs
3. **JSON Handling**: How Gin automatically converts Go structs to JSON
4. **URL Parameters**: How to capture dynamic values from URLs
5. **Error Handling**: How to return appropriate error responses
6. **Request Binding**: How to parse JSON from request bodies

## Next Steps

Now that you understand the basics, try:

1. Adding more fields to the Book struct
2. Implementing UPDATE (PUT) and DELETE endpoints
3. Adding input validation
4. Using a real database instead of in-memory data
5. Adding middleware for logging or authentication

## Files

- `hello-world.go` - The simplest possible Gin server
- `main.go` - Complete book API with all endpoints
- `go.mod` - Go module definition with dependencies

This is your foundation for building larger, more complex APIs with Go and Gin!