# Mastering HTTP: The Foundation of Web Communication

Picture this scenario: you've built your first Go web server and it's handling basic requests perfectly. Everything seems straightforward until you start receiving different types of requests, need to parse JSON data, handle file uploads, or deal with complex query parameters. Suddenly, what seemed simple becomes a maze of HTTP status codes, headers, and request parsing challenges. You realize that while frameworks can hide these complexities, truly understanding HTTP fundamentals is what separates competent web developers from exceptional ones.

This knowledge gap is surprisingly common among developers who jump straight into web frameworks without mastering the underlying HTTP protocol. When production issues arise—like incorrect status codes confusing clients, malformed JSON responses breaking integrations, or security vulnerabilities from improper input handling—developers often struggle to debug effectively because they lack deep HTTP knowledge. The irony is that Go's standard library makes HTTP fundamentals accessible and elegant, but many developers rush past these concepts.

What makes this chapter particularly valuable is that you'll learn HTTP concepts through Go's lens, which emphasizes explicitness and clarity. By the end of this chapter, you'll handle complex HTTP scenarios with confidence, understand how requests flow through your application, and implement middleware patterns that make your applications more robust and maintainable. Most importantly, you'll gain the debugging skills that come from understanding HTTP at a fundamental level.

## Introduction

HTTP is the foundation of all web communication, and Go provides exceptional tools for working with it at a fundamental level. While many developers rely on frameworks to handle HTTP complexities, understanding these concepts directly through Go's standard library gives you superpowers when building, debugging, and optimizing web applications.

This chapter builds directly on your Chapter 1 foundation, taking you from basic web servers to sophisticated HTTP request handling. You'll master the request-response lifecycle, learn to parse different types of data, and implement middleware patterns that professional applications require.

Here's what you'll master in this chapter:

• **HTTP request and response fundamentals**: Understand the complete lifecycle of HTTP communication and how Go handles each phase.

• **Status codes and headers management**: Learn when and how to use different HTTP status codes and set proper headers for various response types.

• **Multi-method request handling**: Implement endpoints that properly handle GET, POST, PUT, DELETE, and other HTTP methods with appropriate validation.

• **Data parsing techniques**: Parse query parameters, form data, and JSON payloads while handling validation and error cases gracefully.

• **Middleware implementation**: Create reusable middleware for logging, security, CORS, and other cross-cutting concerns.

• **RESTful API development**: Build a complete REST API using only the standard library with proper resource design and error handling.

## Learning Objectives

By completing this chapter, you will achieve these specific, measurable outcomes:

• **HTTP lifecycle mastery**: Trace and explain the complete HTTP request-response cycle in Go applications, including how Go's server handles concurrent requests.

• **Status code proficiency**: Correctly implement and justify the use of appropriate HTTP status codes (200, 201, 400, 404, 500, etc.) for different scenarios.

• **Request parsing expertise**: Successfully parse and validate query parameters, form data, and JSON payloads with proper error handling and security considerations.

• **Middleware implementation skills**: Create and chain custom middleware functions for logging, authentication, CORS, and security headers.

• **RESTful API development**: Build a complete CRUD API following REST conventions with proper resource design, status codes, and error responses.

• **Production readiness**: Implement proper logging, error handling, and security measures that meet professional development standards.

## The HTTP Request-Response Lifecycle in Go

Understanding how HTTP requests flow through your Go application is crucial for building robust web services. Unlike some languages where this process is hidden behind framework abstractions, Go gives you direct access to every stage of the HTTP lifecycle, making it easier to understand and debug when issues arise.

When a client makes an HTTP request to your Go server, several important steps occur before your handler function even executes. Go's `net/http` package manages connection handling, request parsing, and response writing automatically, but understanding these details helps you write better handlers and troubleshoot problems effectively.

The journey begins when Go's HTTP server receives a TCP connection. The server automatically parses the raw HTTP request into a structured `*http.Request` object and creates an `http.ResponseWriter` interface for sending the response back. This parsing includes extracting the HTTP method, URL, headers, and body content into easily accessible Go data structures.

Let's examine how Go handles a typical HTTP request:

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "time"
)

func requestLifecycleHandler(w http.ResponseWriter, r *http.Request) {
    // Log request details to understand the lifecycle
    log.Printf("Request received: %s %s from %s", 
               r.Method, r.URL.Path, r.RemoteAddr)
    
    // Access various parts of the request
    fmt.Fprintf(w, "Method: %s\n", r.Method)
    fmt.Fprintf(w, "URL Path: %s\n", r.URL.Path)
    fmt.Fprintf(w, "Query String: %s\n", r.URL.RawQuery)
    fmt.Fprintf(w, "User Agent: %s\n", r.Header.Get("User-Agent"))
    fmt.Fprintf(w, "Content Length: %d\n", r.ContentLength)
}
```

This handler demonstrates key aspects of request processing:

• **Accesses** the HTTP method to understand what action the client wants to perform.

• **Extracts** URL path information for routing decisions and resource identification.

• **Reads** query string data for filtering and pagination parameters.

• **Inspects** headers to understand client capabilities and preferences.

• **Checks** content length to prepare for body parsing and validation.

Go's concurrent request handling is one of its most powerful features. Every incoming request automatically runs in its own goroutine, allowing your server to handle thousands of concurrent connections efficiently:

```go
func concurrentHandler(w http.ResponseWriter, r *http.Request) {
    // Each request runs in its own goroutine
    goroutineID := getCurrentGoroutineID() // Hypothetical function
    
    log.Printf("Handling request in goroutine %d", goroutineID)
    
    // Simulate some processing time
    time.Sleep(2 * time.Second)
    
    fmt.Fprintf(w, "Request processed by goroutine %d\n", goroutineID)
    log.Printf("Request completed in goroutine %d", goroutineID)
}
```

This concurrent model means your handlers must be designed for safe concurrent access:

• **Avoids** shared mutable state unless properly synchronized with mutexes.

• **Uses** goroutine-safe operations for logging and data access.

• **Handles** context cancellation when clients disconnect prematurely.

• **Implements** proper resource cleanup to prevent goroutine leaks.

Understanding this lifecycle helps you design handlers that work efficiently with Go's concurrency model and debug issues when they arise.

## HTTP Status Codes and Headers: Communicating Effectively

HTTP status codes are your application's primary way of communicating success, failure, and various conditions to clients. While it's tempting to just return 200 for success and 500 for errors, proper status code usage greatly improves API usability and helps clients handle different scenarios appropriately.

Go makes working with status codes straightforward, but knowing when to use each code requires understanding what they communicate to clients. The HTTP specification defines status codes in ranges: 2xx for success, 3xx for redirection, 4xx for client errors, and 5xx for server errors. Each range serves a specific purpose in the client-server communication protocol.

Let's explore proper status code usage with practical examples:

```go
func statusCodeHandler(w http.ResponseWriter, r *http.Request) {
    switch r.URL.Path {
    case "/success":
        // 200 OK - Standard successful response
        w.WriteHeader(http.StatusOK)
        fmt.Fprintf(w, "Operation completed successfully")
        
    case "/created":
        // 201 Created - Resource was successfully created
        w.WriteHeader(http.StatusCreated)
        fmt.Fprintf(w, "Resource created successfully")
        
    case "/no-content":
        // 204 No Content - Success but no response body
        w.WriteHeader(http.StatusNoContent)
        // No body content for 204 responses
        
    case "/bad-request":
        // 400 Bad Request - Client sent invalid data
        w.WriteHeader(http.StatusBadRequest)
        fmt.Fprintf(w, "Invalid request format")
        
    case "/not-found":
        // 404 Not Found - Requested resource doesn't exist
        w.WriteHeader(http.StatusNotFound)
        fmt.Fprintf(w, "Resource not found")
        
    default:
        // 500 Internal Server Error - Server-side problem
        w.WriteHeader(http.StatusInternalServerError)
        fmt.Fprintf(w, "Unexpected server error")
    }
}
```

Each status code choice communicates specific information:

• **200 OK** indicates successful request processing with response content.

• **201 Created** signals successful resource creation, often used with POST requests.

• **204 No Content** shows success but intentionally omits response body content.

• **400 Bad Request** tells clients their request format or data is invalid.

• **404 Not Found** clearly indicates the requested resource doesn't exist.

• **500 Internal Server Error** signals server-side problems beyond client control.

Headers provide additional metadata about requests and responses. Go's `http.Header` type makes header manipulation intuitive while following HTTP standards:

```go
func headerHandler(w http.ResponseWriter, r *http.Request) {
    // Read request headers
    contentType := r.Header.Get("Content-Type")
    userAgent := r.Header.Get("User-Agent")
    authorization := r.Header.Get("Authorization")
    
    log.Printf("Content-Type: %s", contentType)
    log.Printf("User-Agent: %s", userAgent)
    
    // Set response headers before writing status or body
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("X-API-Version", "1.0")
    
    // Add security headers
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"message": "Headers set successfully"}`)
}
```

Header management demonstrates important principles:

• **Reads** request headers to understand client capabilities and authentication.

• **Sets** response content type to help clients parse response data correctly.

• **Adds** caching directives to control how responses are cached.

• **Includes** security headers to prevent common web vulnerabilities.

• **Maintains** header order by setting them before writing status or body.

Proper status codes and headers make your APIs more professional and easier for clients to integrate with, while also improving debugging when issues occur.

## Handling Different HTTP Methods

Modern web applications need to handle various HTTP methods to implement full CRUD (Create, Read, Update, Delete) functionality. Each HTTP method has specific semantics that clients expect, and your handlers should respect these conventions to build predictable APIs.

Go doesn't automatically route different methods to different functions like some frameworks do, but this gives you complete control over how your application handles each method. You can implement method-specific logic within a single handler or create separate handlers for different methods based on your application's needs.

Here's how to properly handle different HTTP methods in a single handler:

```go
func methodHandler(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        handleGet(w, r)
    case http.MethodPost:
        handlePost(w, r)
    case http.MethodPut:
        handlePut(w, r)
    case http.MethodDelete:
        handleDelete(w, r)
    case http.MethodOptions:
        handleOptions(w, r)
    default:
        // 405 Method Not Allowed for unsupported methods
        w.Header().Set("Allow", "GET, POST, PUT, DELETE, OPTIONS")
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}
```

This structure provides clear method routing and proper error handling:

• **Uses** constants from the http package for method comparison.

• **Delegates** to specific handler functions for clean code organization.

• **Returns** 405 Method Not Allowed for unsupported methods.

• **Sets** the Allow header to inform clients about supported methods.

• **Handles** OPTIONS requests for CORS preflight support.

Let's implement each method handler with proper semantics:

```go
func handleGet(w http.ResponseWriter, r *http.Request) {
    // GET should be safe and idempotent - no side effects
    log.Printf("GET request for resource: %s", r.URL.Path)
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    
    // Return existing resource data
    response := `{"id": 1, "name": "Sample Resource", "status": "active"}`
    w.Write([]byte(response))
}

func handlePost(w http.ResponseWriter, r *http.Request) {
    // POST creates new resources - not idempotent
    log.Printf("POST request to create resource")
    
    // Read and validate request body
    if r.Header.Get("Content-Type") != "application/json" {
        http.Error(w, "Content-Type must be application/json", 
                   http.StatusBadRequest)
        return
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated) // 201 for resource creation
    
    response := `{"id": 2, "message": "Resource created successfully"}`
    w.Write([]byte(response))
}

func handlePut(w http.ResponseWriter, r *http.Request) {
    // PUT updates entire resources - should be idempotent
    log.Printf("PUT request to update resource: %s", r.URL.Path)
    
    if r.Header.Get("Content-Type") != "application/json" {
        http.Error(w, "Content-Type must be application/json", 
                   http.StatusBadRequest)
        return
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    
    response := `{"id": 1, "message": "Resource updated successfully"}`
    w.Write([]byte(response))
}

func handleDelete(w http.ResponseWriter, r *http.Request) {
    // DELETE removes resources - should be idempotent
    log.Printf("DELETE request for resource: %s", r.URL.Path)
    
    w.WriteHeader(http.StatusNoContent) // 204 for successful deletion
    // No response body for DELETE operations
}
```

Each method implementation follows HTTP semantics:

• **GET** retrieves data without side effects and always returns the same result.

• **POST** creates new resources and typically returns 201 Created status.

• **PUT** updates entire resources and should produce the same result when repeated.

• **DELETE** removes resources and returns 204 No Content on success.

• **All methods** validate content type for operations that expect request bodies.

This method-based routing approach gives you full control over your API's behavior while maintaining HTTP standard compliance.

## Parsing Query Parameters, Form Data, and JSON

Real-world web applications need to handle various types of input data: URL query parameters for filtering and pagination, form data from HTML forms, and JSON payloads from API clients. Go's standard library provides excellent tools for parsing each type, but proper validation and error handling are crucial for building secure applications.

Query parameters are the simplest form of input data, passed in the URL after the question mark. They're commonly used for filtering, sorting, pagination, and optional parameters that modify how resources are retrieved or processed.

Here's how to properly parse and validate query parameters:

```go
func queryParamHandler(w http.ResponseWriter, r *http.Request) {
    // Get query parameters using URL.Query()
    queryParams := r.URL.Query()
    
    // Get single parameter with default value
    page := queryParams.Get("page")
    if page == "" {
        page = "1" // Default value
    }
    
    // Convert string to integer with validation
    pageNum, err := strconv.Atoi(page)
    if err != nil || pageNum < 1 {
        http.Error(w, "Invalid page number", http.StatusBadRequest)
        return
    }
    
    // Get parameter with multiple values
    tags := queryParams["tag"] // Returns []string
    
    // Get optional boolean parameter
    includeInactive := queryParams.Get("include_inactive") == "true"
    
    // Validate page size with limits
    limitStr := queryParams.Get("limit")
    limit := 10 // Default limit
    if limitStr != "" {
        if parsedLimit, err := strconv.Atoi(limitStr); err == nil {
            if parsedLimit > 0 && parsedLimit <= 100 {
                limit = parsedLimit
            } else {
                http.Error(w, "Limit must be between 1 and 100", 
                          http.StatusBadRequest)
                return
            }
        }
    }
    
    w.Header().Set("Content-Type", "application/json")
    response := fmt.Sprintf(`{
        "page": %d,
        "limit": %d,
        "tags": %v,
        "include_inactive": %t
    }`, pageNum, limit, tags, includeInactive)
    
    w.Write([]byte(response))
}
```

This implementation demonstrates robust query parameter handling:

• **Provides** default values for optional parameters to ensure consistent behavior.

• **Validates** numeric conversions and range limits to prevent invalid data processing.

• **Handles** multiple values for parameters that can appear multiple times.

• **Implements** proper error responses with specific error messages for debugging.

• **Sets** reasonable limits on parameter values to prevent abuse.

Form data handling is essential for processing HTML form submissions and file uploads. Go's `ParseForm()` method makes this straightforward while handling URL encoding automatically:

```go
func formDataHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Only POST method allowed", http.StatusMethodNotAllowed)
        return
    }
    
    // Parse form data (handles both URL-encoded and multipart forms)
    if err := r.ParseForm(); err != nil {
        http.Error(w, "Failed to parse form data", http.StatusBadRequest)
        return
    }
    
    // Get form values with validation
    username := r.FormValue("username")
    if username == "" {
        http.Error(w, "Username is required", http.StatusBadRequest)
        return
    }
    
    email := r.FormValue("email")
    if email == "" || !isValidEmail(email) {
        http.Error(w, "Valid email is required", http.StatusBadRequest)
        return
    }
    
    // Get optional fields
    newsletter := r.FormValue("newsletter") == "on"
    
    // Process the form data
    log.Printf("Form submission: username=%s, email=%s, newsletter=%t", 
               username, email, newsletter)
    
    w.Header().Set("Content-Type", "text/html")
    fmt.Fprintf(w, "<h1>Form submitted successfully!</h1>")
    fmt.Fprintf(w, "<p>Username: %s</p>", username)
    fmt.Fprintf(w, "<p>Email: %s</p>", email)
}

func isValidEmail(email string) bool {
    // Simple email validation (use more robust validation in production)
    return strings.Contains(email, "@") && strings.Contains(email, ".")
}
```

Form processing showcases important patterns:

• **Validates** HTTP method to ensure forms are submitted via POST.

• **Parses** form data before accessing individual fields.

• **Checks** required fields and provides specific error messages.

• **Implements** basic validation for email format and other constraints.

• **Handles** boolean checkbox values using standard HTML form conventions.

JSON processing is crucial for modern APIs that communicate with JavaScript clients, mobile apps, and other services. Go's `encoding/json` package provides powerful tools for parsing and generating JSON with proper error handling:

```go
type UserRequest struct {
    Name  string `json:"name"`
    Email string `json:"email"`
    Age   int    `json:"age"`
}

func jsonHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Only POST method allowed", http.StatusMethodNotAllowed)
        return
    }
    
    // Verify content type
    if r.Header.Get("Content-Type") != "application/json" {
        http.Error(w, "Content-Type must be application/json", 
                   http.StatusBadRequest)
        return
    }
    
    // Limit request body size to prevent memory exhaustion
    r.Body = http.MaxBytesReader(w, r.Body, 1048576) // 1MB limit
    
    // Parse JSON request body
    var userReq UserRequest
    decoder := json.NewDecoder(r.Body)
    decoder.DisallowUnknownFields() // Reject unknown fields
    
    if err := decoder.Decode(&userReq); err != nil {
        http.Error(w, "Invalid JSON format: "+err.Error(), 
                   http.StatusBadRequest)
        return
    }
    
    // Validate required fields
    if userReq.Name == "" {
        http.Error(w, "Name is required", http.StatusBadRequest)
        return
    }
    
    if userReq.Age < 0 || userReq.Age > 150 {
        http.Error(w, "Age must be between 0 and 150", http.StatusBadRequest)
        return
    }
    
    // Process the data
    log.Printf("JSON request: %+v", userReq)
    
    // Return JSON response
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    
    response := map[string]interface{}{
        "message": "User created successfully",
        "user":    userReq,
        "id":      123,
    }
    
    json.NewEncoder(w).Encode(response)
}
```

JSON handling demonstrates security and robustness principles:

• **Validates** content type to ensure proper request format.

• **Limits** request body size to prevent denial of service attacks.

• **Rejects** unknown fields to prevent data injection attempts.

• **Validates** business logic constraints on parsed data.

• **Returns** properly formatted JSON responses with appropriate status codes.

These parsing techniques form the foundation for building robust APIs that handle real-world data safely and efficiently.

## Implementing Middleware for Cross-Cutting Concerns

Middleware provides an elegant way to handle cross-cutting concerns like logging, authentication, CORS, and security headers without duplicating code across every handler. Go's `http.Handler` interface makes middleware implementation straightforward and composable, allowing you to chain multiple middleware functions together.

The middleware pattern in Go works by wrapping handler functions with additional functionality. Each middleware function receives an `http.Handler` and returns a new `http.Handler` that can perform actions before and after calling the wrapped handler. This creates a chain of responsibility where each middleware can process the request, call the next handler, and then process the response.

Let's start with a basic logging middleware that tracks request details and response times:

```go
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        
        // Create a wrapper to capture response status code
        wrappedWriter := &responseWriter{
            ResponseWriter: w,
            statusCode:     http.StatusOK,
        }
        
        // Call the next handler
        next.ServeHTTP(wrappedWriter, r)
        
        // Log request details after completion
        duration := time.Since(start)
        log.Printf(
            "%s %s %d %v %s",
            r.Method,
            r.RequestURI,
            wrappedWriter.statusCode,
            duration,
            r.RemoteAddr,
        )
    })
}

// responseWriter wraps http.ResponseWriter to capture status code
type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}
```

This logging middleware showcases key middleware patterns:

• **Wraps** the original ResponseWriter to capture status codes.

• **Measures** request duration from start to completion.

• **Calls** the next handler in the chain using ServeHTTP.

• **Logs** comprehensive request information for monitoring and debugging.

• **Maintains** the original handler interface for seamless integration.

Security headers middleware adds essential protection against common web vulnerabilities:

```go
func securityMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Add security headers before processing the request
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "1; mode=block")
        w.Header().Set("Strict-Transport-Security", 
                      "max-age=31536000; includeSubDomains")
        w.Header().Set("Content-Security-Policy", 
                      "default-src 'self'")
        
        next.ServeHTTP(w, r)
    })
}
```

CORS (Cross-Origin Resource Sharing) middleware enables your API to handle requests from web browsers running on different domains:

```go
func corsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Set CORS headers
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", 
                      "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", 
                      "Content-Type, Authorization")
        w.Header().Set("Access-Control-Max-Age", "86400")
        
        // Handle preflight OPTIONS requests
        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusOK)
            return
        }
        
        next.ServeHTTP(w, r)
    })
}
```

CORS middleware demonstrates important concepts:

• **Sets** appropriate headers for cross-origin requests.

• **Handles** OPTIONS preflight requests that browsers send automatically.

• **Configures** allowed methods, headers, and caching duration.

• **Returns** early for OPTIONS requests without calling subsequent handlers.

Middleware chaining allows you to combine multiple middleware functions into a processing pipeline:

```go
func chainMiddleware(handler http.Handler, middlewares ...func(http.Handler) http.Handler) http.Handler {
    // Apply middleware in reverse order so first middleware wraps innermost
    for i := len(middlewares) - 1; i >= 0; i-- {
        handler = middlewares[i](handler)
    }
    return handler
}

func main() {
    // Create your main handler
    mux := http.NewServeMux()
    mux.HandleFunc("/api/users", userHandler)
    
    // Chain multiple middleware
    handler := chainMiddleware(
        mux,
        loggingMiddleware,
        securityMiddleware,
        corsMiddleware,
    )
    
    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", handler))
}
```

The chaining function creates a middleware stack where:

• **Each** middleware wraps the next one in the chain.

• **Request** processing flows from first to last middleware.

• **Response** processing flows from last to first middleware.

• **Order** matters - logging should typically be outermost to capture all requests.

This middleware pattern makes your application modular and testable while keeping cross-cutting concerns separate from business logic.

## Building RESTful APIs with Standard Library

REST (Representational State Transfer) is an architectural style that uses HTTP methods and URLs to create predictable, scalable APIs. While many developers reach for frameworks to build REST APIs, Go's standard library provides everything needed to create professional-grade RESTful services that follow industry conventions and best practices.

A well-designed REST API treats URLs as resources and uses HTTP methods to represent actions on those resources. For example, `/users` represents a collection of users, while `/users/123` represents a specific user. The HTTP method determines the action: GET retrieves, POST creates, PUT updates, and DELETE removes resources.

Let's build a complete RESTful API for managing tasks, starting with the basic resource structure:

```go
type Task struct {
    ID          int       `json:"id"`
    Title       string    `json:"title"`
    Description string    `json:"description"`
    Completed   bool      `json:"completed"`
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
}

type TaskStore struct {
    mu     sync.RWMutex
    tasks  map[int]*Task
    nextID int
}

func NewTaskStore() *TaskStore {
    return &TaskStore{
        tasks:  make(map[int]*Task),
        nextID: 1,
    }
}
```

This foundation establishes our data model:

• **Defines** a Task struct with JSON tags for proper API responses.

• **Includes** metadata fields like timestamps for audit trails.

• **Uses** thread-safe storage with read-write mutex for concurrent access.

• **Provides** auto-incrementing ID generation for new resources.

Now let's implement the main REST handler that routes requests based on URL patterns:

```go
func (ts *TaskStore) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // Parse URL path to determine resource and ID
    path := strings.TrimPrefix(r.URL.Path, "/tasks")
    
    switch {
    case path == "" || path == "/":
        ts.handleTaskCollection(w, r)
    case strings.HasPrefix(path, "/"):
        // Extract task ID from path like "/123"
        idStr := strings.TrimPrefix(path, "/")
        if id, err := strconv.Atoi(idStr); err == nil {
            ts.handleTaskResource(w, r, id)
        } else {
            ts.sendError(w, "Invalid task ID", http.StatusBadRequest)
        }
    default:
        ts.sendError(w, "Not Found", http.StatusNotFound)
    }
}
```

This routing logic demonstrates REST URL patterns:

• **Distinguishes** between collection endpoints (/tasks) and resource endpoints (/tasks/123).

• **Extracts** resource IDs from URL paths using string manipulation.

• **Validates** ID format and returns appropriate errors for invalid IDs.

• **Delegates** to specific handlers based on the type of resource request.

The collection handler manages operations on the entire collection of tasks:

```go
func (ts *TaskStore) handleTaskCollection(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        ts.getAllTasks(w, r)
    case http.MethodPost:
        ts.createTask(w, r)
    default:
        w.Header().Set("Allow", "GET, POST")
        ts.sendError(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}

func (ts *TaskStore) getAllTasks(w http.ResponseWriter, r *http.Request) {
    ts.mu.RLock()
    defer ts.mu.RUnlock()
    
    // Support filtering by completion status
    completed := r.URL.Query().Get("completed")
    
    var tasks []*Task
    for _, task := range ts.tasks {
        if completed != "" {
            isCompleted, err := strconv.ParseBool(completed)
            if err != nil {
                ts.sendError(w, "Invalid completed parameter", http.StatusBadRequest)
                return
            }
            if task.Completed != isCompleted {
                continue
            }
        }
        tasks = append(tasks, task)
    }
    
    ts.sendJSON(w, tasks, http.StatusOK)
}
```

The GET collection endpoint demonstrates REST best practices:

• **Uses** appropriate HTTP method for retrieval operations.

• **Supports** query parameters for filtering results.

• **Validates** query parameter format with proper error handling.

• **Returns** JSON array of resources with appropriate status code.

• **Implements** proper locking for thread-safe access to shared data.

Resource creation follows REST conventions for POST requests:

```go
func (ts *TaskStore) createTask(w http.ResponseWriter, r *http.Request) {
    var task Task
    if err := json.NewDecoder(r.Body).Decode(&task); err != nil {
        ts.sendError(w, "Invalid JSON body", http.StatusBadRequest)
        return
    }
    
    // Validate required fields
    if task.Title == "" {
        ts.sendError(w, "Title is required", http.StatusBadRequest)
        return
    }
    
    ts.mu.Lock()
    defer ts.mu.Unlock()
    
    // Set server-controlled fields
    task.ID = ts.nextID
    task.CreatedAt = time.Now()
    task.UpdatedAt = time.Now()
    task.Completed = false // Default value
    
    ts.tasks[ts.nextID] = &task
    ts.nextID++
    
    ts.sendJSON(w, &task, http.StatusCreated)
}
```

Resource creation showcases important patterns:

• **Parses** JSON request body into Go struct with error handling.

• **Validates** business rules and required fields before processing.

• **Controls** server-managed fields like ID and timestamps.

• **Returns** 201 Created status with the newly created resource.

Individual resource handling supports GET, PUT, and DELETE operations:

```go
func (ts *TaskStore) handleTaskResource(w http.ResponseWriter, r *http.Request, id int) {
    switch r.Method {
    case http.MethodGet:
        ts.getTask(w, r, id)
    case http.MethodPut:
        ts.updateTask(w, r, id)
    case http.MethodDelete:
        ts.deleteTask(w, r, id)
    default:
        w.Header().Set("Allow", "GET, PUT, DELETE")
        ts.sendError(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}

func (ts *TaskStore) updateTask(w http.ResponseWriter, r *http.Request, id int) {
    ts.mu.Lock()
    defer ts.mu.Unlock()
    
    task, exists := ts.tasks[id]
    if !exists {
        ts.sendError(w, "Task not found", http.StatusNotFound)
        return
    }
    
    var updates Task
    if err := json.NewDecoder(r.Body).Decode(&updates); err != nil {
        ts.sendError(w, "Invalid JSON body", http.StatusBadRequest)
        return
    }
    
    // Update fields (preserve original ID and timestamps)
    if updates.Title != "" {
        task.Title = updates.Title
    }
    if updates.Description != "" {
        task.Description = updates.Description
    }
    task.Completed = updates.Completed
    task.UpdatedAt = time.Now()
    
    ts.sendJSON(w, task, http.StatusOK)
}
```

This RESTful implementation provides a complete, standards-compliant API using only Go's standard library while demonstrating professional patterns for resource management, error handling, and concurrent access.

## Assignment: RESTful Task Management API

Now it's time to demonstrate your mastery of HTTP fundamentals by building a comprehensive RESTful API for task management. This assignment integrates everything you've learned about HTTP methods, status codes, request parsing, and middleware into a single, production-ready application.

Your task is to create a complete task management system that handles CRUD operations, implements proper error handling, includes middleware for logging and security, and follows REST conventions. This API will serve as a foundation for the more advanced web development concepts we'll explore in future chapters.

**Core API Requirements:**
Build a RESTful API with these endpoints following proper HTTP semantics:
- `GET /tasks` - Retrieve all tasks with optional filtering by completion status
- `POST /tasks` - Create a new task with validation
- `GET /tasks/{id}` - Retrieve a specific task
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task
- `GET /health` - Health check endpoint for monitoring

**Data Model Requirements:**
Implement a Task structure with these fields:
- ID (auto-generated integer)
- Title (required string)
- Description (optional string)
- Completed (boolean, defaults to false)
- CreatedAt (timestamp)
- UpdatedAt (timestamp)

**HTTP Implementation Requirements:**
- Use appropriate HTTP status codes for all responses (200, 201, 400, 404, 405, 500)
- Implement proper Content-Type headers for JSON responses
- Handle different HTTP methods correctly with proper semantics
- Parse JSON request bodies with validation and error handling
- Support query parameters for filtering (e.g., ?completed=true)

**Middleware Requirements:**
Implement these middleware functions:
- Request logging with timestamp, method, URL, status code, and duration
- Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- CORS support for cross-origin requests
- Panic recovery for graceful error handling

**Error Handling Requirements:**
- Return consistent JSON error responses with appropriate status codes
- Validate all input data with meaningful error messages
- Handle malformed JSON requests gracefully
- Implement proper concurrent access protection for the data store

**Technical Constraints:**
- Use only Go's standard library (no external dependencies)
- Implement in-memory storage with proper concurrency controls
- Include comprehensive error handling and logging
- Follow Go idioms and best practices for code organization
- Structure your code with separate packages for handlers, middleware, and types

This assignment tests your understanding of HTTP fundamentals while requiring you to integrate multiple concepts into a cohesive, professional application.

## Solution: Complete RESTful Task Management API

Here's the complete solution that demonstrates all the HTTP fundamentals concepts covered in this chapter. The implementation showcases production-ready patterns while maintaining simplicity and clarity for educational purposes.

The solution is organized into multiple packages following Go conventions, with clear separation between data types, HTTP handlers, middleware, and the main application logic:

**Project Structure:**
```
task-management-api/
├── main.go                 # Application entry point
├── types/
│   └── task.go            # Data structures
├── handlers/
│   └── tasks.go           # HTTP handlers
├── middleware/
│   └── middleware.go      # HTTP middleware
└── tests/
    └── main_test.go       # Unit tests
```

Let's examine the complete implementation, starting with the data types that define our API structure:

```go
// types/task.go
package types

import "time"

type Task struct {
    ID          int       `json:"id"`
    Title       string    `json:"title"`
    Description string    `json:"description"`
    Completed   bool      `json:"completed"`
    CreatedAt   time.Time `json:"created_at"`
    UpdatedAt   time.Time `json:"updated_at"`
}

type CreateTaskRequest struct {
    Title       string `json:"title"`
    Description string `json:"description"`
}

type UpdateTaskRequest struct {
    Title       *string `json:"title,omitempty"`
    Description *string `json:"description,omitempty"`
    Completed   *bool   `json:"completed,omitempty"`
}

type ErrorResponse struct {
    Error   string `json:"error"`
    Message string `json:"message"`
    Status  int    `json:"status"`
}

type SuccessResponse struct {
    Message string      `json:"message"`
    Data    interface{} `json:"data,omitempty"`
    Status  int         `json:"status"`
}
```

The type definitions establish our API contract:

• **Task** struct includes all necessary fields with proper JSON tags for API responses.

• **CreateTaskRequest** separates input validation from the main Task struct.

• **UpdateTaskRequest** uses pointers to distinguish between zero values and omitted fields.

• **ErrorResponse** and **SuccessResponse** provide consistent response formats.

The middleware package implements cross-cutting concerns that apply to all requests:

```go
// middleware/middleware.go
package middleware

import (
    "log"
    "net/http"
    "time"
)

func Logger(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        
        wrappedWriter := &responseWriter{
            ResponseWriter: w,
            statusCode:     http.StatusOK,
        }
        
        next.ServeHTTP(wrappedWriter, r)
        
        duration := time.Since(start)
        log.Printf(
            "%s %s %d %v %s",
            r.Method,
            r.RequestURI,
            wrappedWriter.statusCode,
            duration,
            r.RemoteAddr,
        )
    })
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}

func CORS(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
        
        if r.Method == http.MethodOptions {
            w.WriteHeader(http.StatusOK)
            return
        }
        
        next.ServeHTTP(w, r)
    })
}

func SecurityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "1; mode=block")
        next.ServeHTTP(w, r)
    })
}
```

The middleware implementation demonstrates professional patterns:

• **Logger** captures comprehensive request information including response times.

• **CORS** enables cross-origin requests while handling preflight OPTIONS requests.

• **SecurityHeaders** adds protection against common web vulnerabilities.

• **responseWriter** wrapper captures status codes for logging purposes.

The handlers package contains the core business logic for task management:

```go
// handlers/tasks.go
package handlers

import (
    "encoding/json"
    "fmt"
    "net/http"
    "strconv"
    "strings"
    "sync"
    "time"
    
    "task-management-api/types"
)

type TaskStore struct {
    mu    sync.RWMutex
    tasks map[int]*types.Task
    nextID int
}

func NewTaskStore() *TaskStore {
    return &TaskStore{
        tasks:  make(map[int]*types.Task),
        nextID: 1,
    }
}

type TaskHandler struct {
    store *TaskStore
}

func NewTaskHandler() *TaskHandler {
    return &TaskHandler{
        store: NewTaskStore(),
    }
}
```

The handler structure provides thread-safe task storage:

• **TaskStore** manages tasks with proper synchronization using read-write mutexes.

• **TaskHandler** encapsulates the store and provides HTTP handler methods.

• **Constructor** functions follow Go idioms for object initialization.

The main handler implements REST routing logic:

```go
func (h *TaskHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    path := strings.TrimPrefix(r.URL.Path, "/tasks")
    
    switch {
    case path == "" || path == "/":
        h.handleTasks(w, r)
    case strings.HasPrefix(path, "/"):
        idStr := strings.TrimPrefix(path, "/")
        if id, err := strconv.Atoi(idStr); err == nil {
            h.handleTaskByID(w, r, id)
        } else {
            h.sendError(w, "Invalid task ID", http.StatusBadRequest)
        }
    default:
        h.sendError(w, "Not Found", http.StatusNotFound)
    }
}

func (h *TaskHandler) handleTasks(w http.ResponseWriter, r *http.Request) {
    switch r.Method {
    case http.MethodGet:
        h.getAllTasks(w, r)
    case http.MethodPost:
        h.createTask(w, r)
    default:
        h.sendError(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}
```

The routing logic demonstrates clean URL parsing:

• **Parses** URL paths to distinguish between collection and resource endpoints.

• **Extracts** resource IDs with proper validation and error handling.

• **Routes** requests to appropriate handlers based on HTTP method.

• **Returns** proper error responses for invalid routes or methods.

Here's the complete task creation handler:

```go
func (h *TaskHandler) createTask(w http.ResponseWriter, r *http.Request) {
    var req types.CreateTaskRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        h.sendError(w, "Invalid JSON body", http.StatusBadRequest)
        return
    }
    
    if req.Title == "" {
        h.sendError(w, "Title is required", http.StatusBadRequest)
        return
    }
    
    h.store.mu.Lock()
    defer h.store.mu.Unlock()
    
    task := &types.Task{
        ID:          h.store.nextID,
        Title:       req.Title,
        Description: req.Description,
        Completed:   false,
        CreatedAt:   time.Now(),
        UpdatedAt:   time.Now(),
    }
    
    h.store.tasks[h.store.nextID] = task
    h.store.nextID++
    
    h.sendSuccess(w, "Task created successfully", task, http.StatusCreated)
}
```

The creation handler showcases REST best practices:

• **Parses** JSON request body with proper error handling.

• **Validates** required fields before processing.

• **Controls** server-managed fields like ID and timestamps.

• **Uses** appropriate HTTP status code (201 Created) for resource creation.

• **Implements** proper locking for concurrent access safety.

The main application brings everything together with proper middleware chaining:

```go
// main.go
package main

import (
    "log"
    "net/http"
    "time"
    
    "task-management-api/handlers"
    "task-management-api/middleware"
)

func main() {
    taskHandler := handlers.NewTaskHandler()
    
    mux := http.NewServeMux()
    mux.Handle("/tasks", taskHandler)
    mux.Handle("/tasks/", taskHandler)
    mux.HandleFunc("/health", healthCheckHandler)
    
    var handler http.Handler = mux
    handler = middleware.Logger(handler)
    handler = middleware.CORS(handler)
    handler = middleware.SecurityHeaders(handler)
    
    server := &http.Server{
        Addr:         ":8080",
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    
    log.Println("Task Management API starting on http://localhost:8080")
    if err := server.ListenAndServe(); err != nil {
        log.Fatal("Server failed to start:", err)
    }
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    w.Write([]byte(`{"status":"healthy","timestamp":"` + time.Now().Format(time.RFC3339) + `"}`))
}
```

The main application demonstrates production-ready configuration:

• **Chains** multiple middleware functions in the correct order.

• **Configures** server timeouts to prevent resource exhaustion.

• **Includes** health check endpoint for monitoring systems.

• **Provides** clear startup logging for operational visibility.

This complete solution showcases all the HTTP fundamentals concepts while providing a solid foundation for building more complex web applications.

## Quiz: Testing Your HTTP Knowledge

Let's verify your understanding of HTTP fundamentals with questions that test the practical knowledge you'll use when building real web applications.

**Question 1:** Which Go standard library package provides the core HTTP functionality?

a) http/server

b) net/http ✓

c) web/http

**Explanation:** The `net/http` package is Go's standard library package for HTTP client and server implementations. It includes everything needed for building web servers, making HTTP requests, and handling HTTP protocols. The other options don't exist in Go's standard library.

**Question 2:** What is the correct way to handle a POST request that should return a 201 status code for successful resource creation?

a) `w.WriteHeader(http.StatusOK)` followed by `w.Write([]byte("Created"))`

b) `w.WriteHeader(http.StatusCreated)` followed by JSON response with created resource ✓

c) `w.Write([]byte("201 Created"))` without setting status code

**Explanation:** HTTP 201 Created is the proper status code for successful resource creation via POST requests. You should use `http.StatusCreated` constant and typically return the created resource in JSON format. Option A uses wrong status code (200 instead of 201), and option C doesn't properly set the HTTP status code header.

## Summary: Building on Your HTTP Foundation

Congratulations! You've mastered the essential HTTP fundamentals that power modern web applications. This chapter took you from basic request handling to building complete RESTful APIs, giving you the skills to create professional web services using Go's powerful standard library.

You've learned how HTTP requests flow through Go applications, from the initial TCP connection to your handler functions. Understanding this lifecycle helps you debug issues, optimize performance, and build more reliable web services. The concurrent request handling that Go provides automatically gives your applications excellent scalability characteristics right out of the box.

Your work with status codes, headers, and different HTTP methods established the foundation for building APIs that communicate clearly with clients. Proper status code usage makes your APIs more predictable and easier to integrate with, while correct header management ensures security and performance. These skills are essential for any web developer working in professional environments.

The data parsing techniques you practiced—handling query parameters, form data, and JSON payloads—prepare you for real-world applications that process complex user input. Combined with proper validation and error handling, these skills help you build secure applications that gracefully handle edge cases and malicious input.

**Key concepts you've mastered:**

• **HTTP lifecycle understanding** including request parsing, concurrent handling, and response generation

• **Status code proficiency** with proper usage of 2xx, 4xx, and 5xx codes for different scenarios

• **Request data parsing** for query parameters, form data, and JSON with comprehensive validation

• **Middleware implementation** for cross-cutting concerns like logging, security, and CORS

• **RESTful API development** following industry standards for resource design and HTTP method semantics

• **Production-ready patterns** including error handling, concurrent access control, and proper logging

**Next steps in your web development journey:**

In Chapter 3, you'll dive into advanced routing and URL pattern matching. You'll learn to build sophisticated routing systems that handle dynamic URL parameters, implement route groups for API organization, and create custom routers that go beyond Go's basic ServeMux capabilities. The HTTP fundamentals you've mastered in this chapter provide the perfect foundation for these more advanced routing concepts.

The RESTful API patterns you've learned will evolve as we explore more complex data relationships, authentication systems, and integration with databases. Your solid understanding of HTTP fundamentals will make these advanced topics much easier to grasp and implement effectively.

Keep practicing with the task management API you've built. Try adding new features like task categories, due dates, or user assignments. Experiment with different query parameters, implement additional validation rules, or add performance logging. The more you work with these HTTP fundamentals, the more intuitive web development with Go becomes.

Remember that these HTTP skills are transferable beyond Go—understanding request-response cycles, status codes, and REST principles will serve you well in any web development context. However, Go's explicit approach to HTTP handling gives you insights into web development that many framework-heavy languages obscure.

You're now ready to tackle the more sophisticated routing and URL handling patterns that modern web applications require. Your solid HTTP foundation ensures you'll understand not just how to implement these patterns, but why they work and how to debug them when issues arise.