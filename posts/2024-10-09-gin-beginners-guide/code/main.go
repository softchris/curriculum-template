package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

// Book represents a book in our collection
type Book struct {
	ID     int    `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
}

// Sample data - in a real app, this would be a database
var books = []Book{
	{ID: 1, Title: "The Go Programming Language", Author: "Alan Donovan"},
	{ID: 2, Title: "Learning Go", Author: "Jon Bodner"},
}

// Get all books
func getBooks(c *gin.Context) {
	c.JSON(http.StatusOK, books)
}

// Get a single book by ID
func getBook(c *gin.Context) {
	id := c.Param("id")

	// Convert string ID to integer
	var bookID int
	if _, err := fmt.Sscanf(id, "%d", &bookID); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid book ID format",
		})
		return
	}

	// Find the book
	for _, book := range books {
		if book.ID == bookID {
			c.JSON(http.StatusOK, book)
			return
		}
	}

	c.JSON(http.StatusNotFound, gin.H{
		"error": "Book not found",
	})
}

// Add a new book
func addBook(c *gin.Context) {
	var newBook Book

	// Bind the JSON request to our Book struct
	if err := c.ShouldBindJSON(&newBook); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Add the book to our collection
	newBook.ID = len(books) + 1
	books = append(books, newBook)

	c.JSON(http.StatusCreated, newBook)
}

func main() {
	r := gin.Default()

	// API routes
	r.GET("/books", getBooks)    // Get all books
	r.GET("/books/:id", getBook) // Get book by ID
	r.POST("/books", addBook)    // Add new book

	r.Run(":8080")
}
