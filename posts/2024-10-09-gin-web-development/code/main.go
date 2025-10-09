package main

import (
    "log"
    "github.com/gin-gonic/gin"
    "gin-api-demo/handlers"
    "gin-api-demo/middleware"
    "time"
)

func main() {
    // Set Gin mode based on environment
    gin.SetMode(gin.ReleaseMode)
    
    // Create router with custom configuration
    r := setupRouter()
    
    // Start server with error handling
    log.Println("Starting server on :8080")
    if err := r.Run(":8080"); err != nil {
        log.Fatal("Server startup failed:", err)
    }
}

func setupRouter() *gin.Engine {
    r := gin.New()
    
    // Global middleware (applies to all routes)
    r.Use(middleware.CustomLogger())
    r.Use(middleware.CustomRecovery())
    r.Use(middleware.ErrorHandler())
    
    // Rate limiting for all API endpoints
    rateLimiter := middleware.NewRateLimiter(100, time.Minute)
    
    api := r.Group("/api/v1")
    api.Use(rateLimiter.Middleware())
    {
        // Public endpoints
        api.POST("/auth/login", handlers.Login)
        api.GET("/health", handlers.Health)
        api.POST("/users/register", handlers.RegisterUser)
        
        // Public user endpoints
        api.GET("/users/search", handlers.SearchUsers)
        api.POST("/files/upload", handlers.UploadFile)
        
        // Protected endpoints
        protected := api.Group("")
        protected.Use(middleware.RequireAuth())
        {
            protected.GET("/users", handlers.GetAllUsers)
            protected.POST("/users", handlers.CreateUser)
            protected.GET("/users/:id", handlers.GetUserByID)
            protected.PUT("/users/:id", handlers.UpdateUser)
            protected.DELETE("/users/:id", handlers.DeleteUser)
        }
    }
    
    return r
}