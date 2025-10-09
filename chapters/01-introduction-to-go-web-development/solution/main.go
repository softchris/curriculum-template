package main

import (
    "log"
    "net/http"
    "os"
    "path/filepath"
    "time"
)

func homeHandler(w http.ResponseWriter, r *http.Request) {
    // Add security headers
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    
    // Log the request
    log.Printf("Home page request from %s", r.RemoteAddr)
    
    // Generate dynamic content
    html := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Name - Portfolio</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/projects">Projects</a>
    </nav>
    
    <main>
        <h1>Welcome to My Portfolio</h1>
        <p>Hello! I'm a Go developer passionate about building efficient web applications.</p>
        <p>Current time: ` + time.Now().Format("January 2, 2006 at 3:04 PM") + `</p>
        <p>This server is built with Go's standard library and demonstrates:</p>
        <ul>
            <li>Custom HTTP handlers</li>
            <li>Static file serving</li>
            <li>Proper error handling</li>
            <li>Security best practices</li>
        </ul>
    </main>
</body>
</html>`
    
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.Write([]byte(html))
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
    // Add security headers
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    
    // Log the request
    log.Printf("About page request from %s", r.RemoteAddr)
    
    html := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About - Portfolio</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/projects">Projects</a>
    </nav>
    
    <main>
        <h1>About Me</h1>
        <p>I'm a passionate developer with experience in Go web development.</p>
        <p>This page demonstrates server-side content generation with Go.</p>
        <p>Request method: ` + r.Method + `</p>
        <p>User agent: ` + r.Header.Get("User-Agent") + `</p>
    </main>
</body>
</html>`
    
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.Write([]byte(html))
}

func projectsHandler(w http.ResponseWriter, r *http.Request) {
    // Add security headers
    w.Header().Set("X-Content-Type-Options", "nosniff")
    w.Header().Set("X-Frame-Options", "DENY")
    
    // Log the request
    log.Printf("Projects page request from %s", r.RemoteAddr)
    
    html := `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projects - Portfolio</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/about">About</a>
        <a href="/projects">Projects</a>
    </nav>
    
    <main>
        <h1>My Projects</h1>
        <div class="project">
            <h2>Portfolio Website Server</h2>
            <p>A Go web server built with the standard library demonstrating:</p>
            <ul>
                <li>HTTP routing and handlers</li>
                <li>Static file serving</li>
                <li>Security best practices</li>
                <li>Error handling and logging</li>
            </ul>
        </div>
        
        <div class="project">
            <h2>Future Go Projects</h2>
            <p>Coming soon: REST APIs, database integration, and more!</p>
        </div>
    </main>
</body>
</html>`
    
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.Write([]byte(html))
}

func staticFileHandler(w http.ResponseWriter, r *http.Request) {
    // Remove the "/static/" prefix from the URL path
    filePath := r.URL.Path[8:]
    
    // Security check: prevent directory traversal
    if filepath.HasPrefix(filePath, "..") || filepath.Contains(filePath, "../") {
        log.Printf("Security warning: directory traversal attempt from %s for path %s", 
                  r.RemoteAddr, r.URL.Path)
        http.Error(w, "Invalid path", http.StatusBadRequest)
        return
    }
    
    // Construct full file path
    fullPath := filepath.Join("static", filePath)
    
    // Check if file exists
    if _, err := os.Stat(fullPath); os.IsNotExist(err) {
        log.Printf("File not found: %s requested by %s", fullPath, r.RemoteAddr)
        http.NotFound(w, r)
        return
    }
    
    // Add caching headers for static files
    w.Header().Set("Cache-Control", "public, max-age=3600")
    
    // Serve the file
    http.ServeFile(w, r, fullPath)
    log.Printf("Served static file: %s to %s", fullPath, r.RemoteAddr)
}

func main() {
    // Set up custom logging
    log.SetFlags(log.LstdFlags | log.Lshortfile)
    
    // Register route handlers
    http.HandleFunc("/", homeHandler)
    http.HandleFunc("/about", aboutHandler)
    http.HandleFunc("/projects", projectsHandler)
    http.HandleFunc("/static/", staticFileHandler)
    
    // Start server with timeout configuration
    server := &http.Server{
        Addr:         ":8080",
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    
    log.Println("Portfolio server starting on http://localhost:8080")
    log.Fatal(server.ListenAndServe())
}
