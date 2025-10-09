package main

import (
	"log"
	"net/http"
	"time"

	"task-management-api/handlers"
	"task-management-api/middleware"
)

func main() {
	// Create handlers
	taskHandler := handlers.NewTaskHandler()

	// Create a new ServeMux
	mux := http.NewServeMux()

	// Register routes
	mux.Handle("/tasks", taskHandler)
	mux.Handle("/tasks/", taskHandler)

	// Add a health check endpoint
	mux.HandleFunc("/health", healthCheckHandler)

	// Create middleware chain
	var handler http.Handler = mux
	handler = middleware.Logger(handler)
	handler = middleware.CORS(handler)
	handler = middleware.SecurityHeaders(handler)

	// Configure server
	server := &http.Server{
		Addr:         ":8080",
		Handler:      handler,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Println("Task Management API starting on http://localhost:8080")
	log.Println("Available endpoints:")
	log.Println("  GET    /tasks          - Get all tasks")
	log.Println("  POST   /tasks          - Create a new task")
	log.Println("  GET    /tasks/{id}     - Get a specific task")
	log.Println("  PUT    /tasks/{id}     - Update a specific task")
	log.Println("  DELETE /tasks/{id}     - Delete a specific task")
	log.Println("  GET    /health         - Health check")

	if err := server.ListenAndServe(); err != nil {
		log.Fatal("Server failed to start:", err)
	}
}

// healthCheckHandler provides a simple health check endpoint
func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"healthy","timestamp":"` + time.Now().Format(time.RFC3339) + `"}`))
}
