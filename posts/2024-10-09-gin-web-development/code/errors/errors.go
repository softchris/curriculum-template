package errors

import (
    "fmt"
    "net/http"
)

type APIError struct {
    Code       string `json:"code"`
    Message    string `json:"message"`
    Details    string `json:"details,omitempty"`
    StatusCode int    `json:"-"`
}

func (e APIError) Error() string {
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

// Predefined error types
var (
    ErrValidationFailed = APIError{
        Code:       "VALIDATION_FAILED",
        Message:    "Request validation failed",
        StatusCode: http.StatusBadRequest,
    }
    
    ErrUserNotFound = APIError{
        Code:       "USER_NOT_FOUND",
        Message:    "User not found",
        StatusCode: http.StatusNotFound,
    }
    
    ErrUnauthorized = APIError{
        Code:       "UNAUTHORIZED",
        Message:    "Authentication required",
        StatusCode: http.StatusUnauthorized,
    }
    
    ErrInternalServer = APIError{
        Code:       "INTERNAL_ERROR",
        Message:    "An internal server error occurred",
        StatusCode: http.StatusInternalServerError,
    }

    ErrEmailAlreadyExists = APIError{
        Code:       "EMAIL_ALREADY_EXISTS",
        Message:    "A user with this email address already exists",
        StatusCode: http.StatusConflict,
    }
)

func NewValidationError(details string) APIError {
    err := ErrValidationFailed
    err.Details = details
    return err
}

func NewNotFoundError(resource string, id interface{}) APIError {
    err := ErrUserNotFound
    err.Message = fmt.Sprintf("%s with ID %v not found", resource, id)
    return err
}