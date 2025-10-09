package handlers

import (
	"gin-api-demo/errors"
	"gin-api-demo/models"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

// In-memory storage for demo purposes
var users = []models.User{
	{ID: 1, Name: "John Doe", Email: "john@example.com", Age: 30, CreatedAt: time.Now()},
	{ID: 2, Name: "Jane Smith", Email: "jane@example.com", Age: 25, CreatedAt: time.Now()},
}
var nextID = 3

func GetAllUsers(c *gin.Context) {
	// Query parameter parsing
	limit := c.DefaultQuery("limit", "10")
	offset := c.DefaultQuery("offset", "0")

	// Convert parameters with error handling
	limitInt, err := strconv.Atoi(limit)
	if err != nil || limitInt < 1 {
		c.Error(errors.NewValidationError("Invalid limit parameter"))
		return
	}

	offsetInt, err := strconv.Atoi(offset)
	if err != nil || offsetInt < 0 {
		c.Error(errors.NewValidationError("Invalid offset parameter"))
		return
	}

	// Apply pagination
	end := offsetInt + limitInt
	if end > len(users) {
		end = len(users)
	}

	if offsetInt >= len(users) {
		c.JSON(http.StatusOK, gin.H{
			"users": []models.User{},
			"total": len(users),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"users": users[offsetInt:end],
		"total": len(users),
	})
}

func CreateUser(c *gin.Context) {
	var req models.CreateUserRequest

	// Bind and validate JSON request
	if err := c.ShouldBindJSON(&req); err != nil {
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Check if email already exists
	for _, user := range users {
		if user.Email == req.Email {
			c.Error(errors.ErrEmailAlreadyExists)
			return
		}
	}

	// Create new user
	user := models.User{
		ID:        nextID,
		Name:      req.Name,
		Email:     req.Email,
		Age:       req.Age,
		CreatedAt: time.Now(),
	}
	nextID++

	users = append(users, user)

	// Return created user with 201 status
	c.JSON(http.StatusCreated, user)
}

func GetUserByID(c *gin.Context) {
	// Extract path parameter
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.Error(errors.NewValidationError("User ID must be a valid integer"))
		return
	}

	// Find user
	for _, user := range users {
		if user.ID == id {
			c.JSON(http.StatusOK, user)
			return
		}
	}

	c.Error(errors.NewNotFoundError("User", id))
}

func UpdateUser(c *gin.Context) {
	// Extract path parameter
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.Error(errors.NewValidationError("User ID must be a valid integer"))
		return
	}

	var req models.UpdateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Find and update user
	for i, user := range users {
		if user.ID == id {
			if req.FullName != nil {
				users[i].Name = *req.FullName
			}
			if req.Email != nil {
				// Check if email already exists
				for j, existingUser := range users {
					if j != i && existingUser.Email == *req.Email {
						c.Error(errors.ErrEmailAlreadyExists)
						return
					}
				}
				users[i].Email = *req.Email
			}

			c.JSON(http.StatusOK, users[i])
			return
		}
	}

	c.Error(errors.NewNotFoundError("User", id))
}

func DeleteUser(c *gin.Context) {
	// Extract path parameter
	idStr := c.Param("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		c.Error(errors.NewValidationError("User ID must be a valid integer"))
		return
	}

	// Find and delete user
	for i, user := range users {
		if user.ID == id {
			users = append(users[:i], users[i+1:]...)
			c.JSON(http.StatusOK, gin.H{"message": "User deleted successfully"})
			return
		}
	}

	c.Error(errors.NewNotFoundError("User", id))
}

func SearchUsers(c *gin.Context) {
	var query models.SearchUsersQuery

	// Bind query parameters
	if err := c.ShouldBindQuery(&query); err != nil {
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Set defaults for optional parameters
	if query.Limit == 0 {
		query.Limit = 20
	}
	if query.Category == "" {
		query.Category = "all"
	}
	if query.SortBy == "" {
		query.SortBy = "created_at"
	}
	if query.Order == "" {
		query.Order = "desc"
	}

	// Perform search (simplified)
	results := searchUsers(query)

	c.JSON(http.StatusOK, gin.H{
		"results": results,
		"query":   query.Query,
		"total":   len(results),
	})
}

func searchUsers(query models.SearchUsersQuery) []models.User {
	// Simplified search implementation
	var results []models.User
	for _, user := range users {
		// Simple name or email search
		if len(user.Name) > 0 && user.Name == query.Query {
			results = append(results, user)
		} else if len(user.Email) > 0 && user.Email == query.Query {
			results = append(results, user)
		}
	}

	// Apply limit
	if len(results) > query.Limit {
		results = results[:query.Limit]
	}

	return results
}

func Health(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":    "healthy",
		"service":   "gin-api-demo",
		"timestamp": time.Now().Unix(),
	})
}

func Login(c *gin.Context) {
	var req models.LoginRequest

	if err := c.ShouldBindJSON(&req); err != nil {
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Simplified authentication (in production, check against database and hash passwords)
	if req.Email == "admin@example.com" && req.Password == "password123" {
		c.JSON(http.StatusOK, gin.H{
			"token":      "valid-demo-token",
			"expires_in": 3600,
		})
		return
	}

	c.Error(errors.ErrUnauthorized)
}
