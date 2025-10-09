package main

import "github.com/gin-gonic/gin"

func main() {
	// Create a Gin router with default middleware
	r := gin.Default()

	// Define a simple route
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	// Start server on port 8080
	r.Run(":8080")
}
