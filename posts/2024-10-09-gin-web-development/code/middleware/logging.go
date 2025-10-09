package middleware

import (
    "log"
    "time"
    "github.com/gin-gonic/gin"
)

func CustomLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Start timer
        start := time.Now()
        
        // Process request
        c.Next()
        
        // Calculate request duration
        duration := time.Since(start)
        
        // Log request details
        log.Printf(
            "%s %s %d %v %s",
            c.Request.Method,
            c.Request.RequestURI,
            c.Writer.Status(),
            duration,
            c.ClientIP(),
        )
    }
}