package main

import (
    "net/http"
    "strconv"
    "github.com/gin-gonic/gin"
)

type User struct {
    ID   int    `json:"id"`
    Name string `json:"name"`
}

func getUserHandler(c *gin.Context) {
    idStr := c.Param("id")
    
    id, err := strconv.Atoi(idStr)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
        return
    }
    
    user := User{ID: id, Name: "John Doe"}
    c.JSON(http.StatusOK, user)
}

func setupRouter() *gin.Engine {
    r := gin.New()
    
    // Add custom middleware
    r.Use(gin.Logger())
    r.Use(gin.Recovery())
    
    // Add API routes
    v1 := r.Group("/api/v1")
    {
        v1.GET("/users/:id", getUserHandler)
    }
    
    return r
}

func main() {
    r := setupRouter()
    r.Run(":8080")
}