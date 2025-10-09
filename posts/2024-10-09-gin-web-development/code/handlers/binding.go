package handlers

import (
	"gin-api-demo/errors"
	"gin-api-demo/models"
	"log"
	"net/http"
	"time"
	"unicode"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
)

func init() {
	// Register custom validation for password strength
	if v, ok := validator.New().(*validator.Validate); ok {
		v.RegisterValidation("password", validatePassword)
	}
}

func validatePassword(fl validator.FieldLevel) bool {
	password := fl.Field().String()

	// Check for at least one uppercase letter
	hasUpper := false
	hasLower := false
	hasDigit := false
	hasSpecial := false

	for _, char := range password {
		switch {
		case unicode.IsUpper(char):
			hasUpper = true
		case unicode.IsLower(char):
			hasLower = true
		case unicode.IsDigit(char):
			hasDigit = true
		case unicode.IsPunct(char) || unicode.IsSymbol(char):
			hasSpecial = true
		}
	}

	return hasUpper && hasLower && hasDigit && hasSpecial
}

func RegisterUser(c *gin.Context) {
	var req models.RegisterUserRequest

	// Bind and validate JSON request
	if err := c.ShouldBindJSON(&req); err != nil {
		// Return detailed validation errors
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Additional business logic validation
	if time.Since(req.DateOfBirth).Hours() < 18*365*24 {
		c.Error(errors.APIError{
			Code:       "AGE_REQUIREMENT",
			Message:    "User must be at least 18 years old",
			StatusCode: http.StatusBadRequest,
		})
		return
	}

	if !req.AgreeToTerms {
		c.Error(errors.APIError{
			Code:       "TERMS_REQUIRED",
			Message:    "Terms of service agreement required",
			StatusCode: http.StatusBadRequest,
		})
		return
	}

	// Check if username or email already exists
	for _, user := range users {
		if user.Email == req.Email {
			c.Error(errors.ErrEmailAlreadyExists)
			return
		}
	}

	// Process registration (simplified)
	user := models.User{
		ID:        nextID,
		Name:      req.FullName,
		Email:     req.Email,
		Age:       int(time.Since(req.DateOfBirth).Hours() / (365 * 24)),
		CreatedAt: time.Now(),
	}
	nextID++
	users = append(users, user)

	c.JSON(http.StatusCreated, gin.H{
		"message": "User registered successfully",
		"user_id": user.ID,
	})
}

func UploadFile(c *gin.Context) {
	var req models.UploadFileRequest

	// Bind form data
	if err := c.ShouldBind(&req); err != nil {
		c.Error(errors.NewValidationError(err.Error()))
		return
	}

	// Handle file upload
	file, header, err := c.Request.FormFile("file")
	if err != nil {
		c.Error(errors.APIError{
			Code:       "FILE_REQUIRED",
			Message:    "File upload required",
			StatusCode: http.StatusBadRequest,
		})
		return
	}
	defer file.Close()

	// Validate file size and type
	if header.Size > 10*1024*1024 { // 10MB limit
		c.Error(errors.APIError{
			Code:       "FILE_TOO_LARGE",
			Message:    "File size exceeds 10MB limit",
			StatusCode: http.StatusBadRequest,
		})
		return
	}

	// Process file upload (simplified - in production, save to storage)
	fileID := generateFileID()
	log.Printf("File uploaded: %s (size: %d bytes, type: %s)",
		header.Filename, header.Size, req.Category)

	c.JSON(http.StatusCreated, gin.H{
		"message":     "File uploaded successfully",
		"file_id":     fileID,
		"filename":    header.Filename,
		"size":        header.Size,
		"title":       req.Title,
		"description": req.Description,
		"category":    req.Category,
		"public":      req.Public,
	})
}

func generateFileID() string {
	// Simple file ID generation for demo
	return "file_" + time.Now().Format("20060102150405")
}
