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

// TaskStore manages tasks in memory
type TaskStore struct {
	mu     sync.RWMutex
	tasks  map[int]*types.Task
	nextID int
}

// NewTaskStore creates a new in-memory task store
func NewTaskStore() *TaskStore {
	return &TaskStore{
		tasks:  make(map[int]*types.Task),
		nextID: 1,
	}
}

// TaskHandler handles all task-related HTTP requests
type TaskHandler struct {
	store *TaskStore
}

// NewTaskHandler creates a new task handler
func NewTaskHandler() *TaskHandler {
	return &TaskHandler{
		store: NewTaskStore(),
	}
}

// ServeHTTP implements the http.Handler interface for routing
func (h *TaskHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Parse the URL path to determine the action
	path := strings.TrimPrefix(r.URL.Path, "/tasks")

	switch {
	case path == "" || path == "/":
		h.handleTasks(w, r)
	case strings.HasPrefix(path, "/"):
		// Extract task ID from path like "/123"
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

// handleTasks handles requests to /tasks (without ID)
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

// handleTaskByID handles requests to /tasks/{id}
func (h *TaskHandler) handleTaskByID(w http.ResponseWriter, r *http.Request, id int) {
	switch r.Method {
	case http.MethodGet:
		h.getTaskByID(w, r, id)
	case http.MethodPut:
		h.updateTask(w, r, id)
	case http.MethodDelete:
		h.deleteTask(w, r, id)
	default:
		h.sendError(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

// getAllTasks returns all tasks, optionally filtered by completion status
func (h *TaskHandler) getAllTasks(w http.ResponseWriter, r *http.Request) {
	h.store.mu.RLock()
	defer h.store.mu.RUnlock()

	// Check for query parameters
	completed := r.URL.Query().Get("completed")

	var tasks []*types.Task
	for _, task := range h.store.tasks {
		// Filter by completion status if specified
		if completed != "" {
			isCompleted, err := strconv.ParseBool(completed)
			if err != nil {
				h.sendError(w, "Invalid completed parameter", http.StatusBadRequest)
				return
			}
			if task.Completed != isCompleted {
				continue
			}
		}
		tasks = append(tasks, task)
	}

	h.sendSuccess(w, "Tasks retrieved successfully", tasks, http.StatusOK)
}

// getTaskByID returns a specific task by ID
func (h *TaskHandler) getTaskByID(w http.ResponseWriter, r *http.Request, id int) {
	h.store.mu.RLock()
	defer h.store.mu.RUnlock()

	task, exists := h.store.tasks[id]
	if !exists {
		h.sendError(w, "Task not found", http.StatusNotFound)
		return
	}

	h.sendSuccess(w, "Task retrieved successfully", task, http.StatusOK)
}

// createTask creates a new task
func (h *TaskHandler) createTask(w http.ResponseWriter, r *http.Request) {
	var req types.CreateTaskRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		h.sendError(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	// Validate required fields
	if req.Title == "" {
		h.sendError(w, "Title is required", http.StatusBadRequest)
		return
	}

	h.store.mu.Lock()
	defer h.store.mu.Unlock()

	// Create new task
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

// updateTask updates an existing task
func (h *TaskHandler) updateTask(w http.ResponseWriter, r *http.Request, id int) {
	var req types.UpdateTaskRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		h.sendError(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	h.store.mu.Lock()
	defer h.store.mu.Unlock()

	task, exists := h.store.tasks[id]
	if !exists {
		h.sendError(w, "Task not found", http.StatusNotFound)
		return
	}

	// Update fields if provided
	if req.Title != nil {
		task.Title = *req.Title
	}
	if req.Description != nil {
		task.Description = *req.Description
	}
	if req.Completed != nil {
		task.Completed = *req.Completed
	}

	task.UpdatedAt = time.Now()

	h.sendSuccess(w, "Task updated successfully", task, http.StatusOK)
}

// deleteTask deletes a task
func (h *TaskHandler) deleteTask(w http.ResponseWriter, r *http.Request, id int) {
	h.store.mu.Lock()
	defer h.store.mu.Unlock()

	_, exists := h.store.tasks[id]
	if !exists {
		h.sendError(w, "Task not found", http.StatusNotFound)
		return
	}

	delete(h.store.tasks, id)

	h.sendSuccess(w, fmt.Sprintf("Task %d deleted successfully", id), nil, http.StatusOK)
}

// sendError sends a JSON error response
func (h *TaskHandler) sendError(w http.ResponseWriter, message string, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	response := types.ErrorResponse{
		Error:   http.StatusText(status),
		Message: message,
		Status:  status,
	}

	json.NewEncoder(w).Encode(response)
}

// sendSuccess sends a JSON success response
func (h *TaskHandler) sendSuccess(w http.ResponseWriter, message string, data interface{}, status int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	response := types.SuccessResponse{
		Message: message,
		Data:    data,
		Status:  status,
	}

	json.NewEncoder(w).Encode(response)
}
