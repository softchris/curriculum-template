package middleware

import (
	"gin-api-demo/errors"
	"log"
	"net/http"
	"runtime/debug"

	"github.com/gin-gonic/gin"
)

func ErrorHandler() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Execute request and capture any errors
		c.Next()

		// Check if any errors occurred
		if len(c.Errors) > 0 {
			// Get the last error (most recent)
			err := c.Errors.Last()

			// Handle different error types
			switch e := err.Err.(type) {
			case errors.APIError:
				// Log the error for debugging
				log.Printf("API Error: %s - %s [%s %s]",
					e.Code, e.Message, c.Request.Method, c.Request.URL.Path)

				// Return structured error response
				c.JSON(e.StatusCode, gin.H{
					"error": gin.H{
						"code":    e.Code,
						"message": e.Message,
						"details": e.Details,
					},
				})

			default:
				// Handle unexpected errors
				log.Printf("Unexpected error: %v [%s %s]",
					e, c.Request.Method, c.Request.URL.Path)

				// Return generic error response
				c.JSON(http.StatusInternalServerError, gin.H{
					"error": gin.H{
						"code":    "INTERNAL_ERROR",
						"message": "An unexpected error occurred",
					},
				})
			}

			// Abort further processing
			c.Abort()
		}
	}
}

func CustomRecovery() gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				// Log panic with stack trace
				log.Printf("Panic recovered: %v\nStack trace:\n%s",
					err, debug.Stack())

				// Return generic error response
				c.JSON(http.StatusInternalServerError, gin.H{
					"error": gin.H{
						"code":    "INTERNAL_ERROR",
						"message": "An unexpected error occurred",
					},
				})

				c.Abort()
			}
		}()

		c.Next()
	}
}
