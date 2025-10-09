package middleware

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
)

type RateLimiter struct {
	clients map[string]*ClientInfo
	mutex   sync.RWMutex
	limit   int
	window  time.Duration
}

type ClientInfo struct {
	requests []time.Time
}

func NewRateLimiter(limit int, window time.Duration) *RateLimiter {
	return &RateLimiter{
		clients: make(map[string]*ClientInfo),
		limit:   limit,
		window:  window,
	}
}

func (rl *RateLimiter) Middleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		clientIP := c.ClientIP()

		rl.mutex.Lock()
		client, exists := rl.clients[clientIP]
		if !exists {
			client = &ClientInfo{requests: []time.Time{}}
			rl.clients[clientIP] = client
		}

		// Clean old requests outside the window
		now := time.Now()
		validRequests := []time.Time{}
		for _, reqTime := range client.requests {
			if now.Sub(reqTime) < rl.window {
				validRequests = append(validRequests, reqTime)
			}
		}
		client.requests = validRequests

		// Check rate limit
		if len(client.requests) >= rl.limit {
			rl.mutex.Unlock()
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error":  "Rate limit exceeded",
				"limit":  rl.limit,
				"window": rl.window.String(),
			})
			c.Abort()
			return
		}

		// Record this request
		client.requests = append(client.requests, now)
		rl.mutex.Unlock()

		c.Next()
	}
}
