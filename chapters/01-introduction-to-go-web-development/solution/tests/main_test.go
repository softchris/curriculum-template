package main

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestHomeHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(homeHandler)

    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v",
            status, http.StatusOK)
    }

    expected := "Welcome to My Portfolio"
    if !contains(rr.Body.String(), expected) {
        t.Errorf("handler returned unexpected body: got %v want %v",
            rr.Body.String(), expected)
    }
}

func TestAboutHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/about", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(aboutHandler)

    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v",
            status, http.StatusOK)
    }

    expected := "About Me"
    if !contains(rr.Body.String(), expected) {
        t.Errorf("handler returned unexpected body: got %v want %v",
            rr.Body.String(), expected)
    }
}

func TestProjectsHandler(t *testing.T) {
    req, err := http.NewRequest("GET", "/projects", nil)
    if err != nil {
        t.Fatal(err)
    }

    rr := httptest.NewRecorder()
    handler := http.HandlerFunc(projectsHandler)

    handler.ServeHTTP(rr, req)

    if status := rr.Code; status != http.StatusOK {
        t.Errorf("handler returned wrong status code: got %v want %v",
            status, http.StatusOK)
    }

    expected := "My Projects"
    if !contains(rr.Body.String(), expected) {
        t.Errorf("handler returned unexpected body: got %v want %v",
            rr.Body.String(), expected)
    }
}

// Helper function to check if a string contains a substring
func contains(s, substr string) bool {
    return len(s) >= len(substr) && s[len(s)-len(substr):] == substr || 
           (len(s) > len(substr) && containsAt(s, substr, 0))
}

func containsAt(s, substr string, start int) bool {
    if start+len(substr) > len(s) {
        return false
    }
    for i := 0; i < len(substr); i++ {
        if s[start+i] != substr[i] {
            if start+1 < len(s) {
                return containsAt(s, substr, start+1)
            }
            return false
        }
    }
    return true
}