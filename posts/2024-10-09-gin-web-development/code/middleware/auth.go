package middleware

import (
    "net/http"
    "strings"
    "github.com/gin-gonic/gin"
)

func RequireAuth() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Extract token from Authorization header
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header required"})
            c.Abort()
            return
        }
        
        // Check for Bearer token format
        tokenParts := strings.Split(authHeader, " ")
        if len(tokenParts) != 2 || tokenParts[0] != "Bearer" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid authorization format"})
            c.Abort()
            return
        }
        
        token := tokenParts[1]
        
        // Validate token (simplified for demo)
        if !isValidToken(token) {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid or expired token"})
            c.Abort()
            return
        }
        
        // Extract user info from token and add to context
        userID := extractUserIDFromToken(token)
        c.Set("userID", userID)
        
        // Continue to next middleware/handler
        c.Next()
    }
}

func isValidToken(token string) bool {
    // In production, implement proper JWT validation
    return token == "valid-demo-token"
}

func extractUserIDFromToken(token string) int {
    // In production, extract from JWT claims
    return 1
}