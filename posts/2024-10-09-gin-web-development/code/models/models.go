package models

import "time"

type User struct {
	ID        int       `json:"id"`
	Name      string    `json:"name" binding:"required"`
	Email     string    `json:"email" binding:"required,email"`
	Age       int       `json:"age" binding:"min=1,max=120"`
	CreatedAt time.Time `json:"created_at"`
}

type CreateUserRequest struct {
	Name  string `json:"name" binding:"required"`
	Email string `json:"email" binding:"required,email"`
	Age   int    `json:"age" binding:"min=1,max=120"`
}

type RegisterUserRequest struct {
	Username     string    `json:"username" binding:"required,min=3,max=50"`
	Email        string    `json:"email" binding:"required,email"`
	Password     string    `json:"password" binding:"required,min=8,password"`
	FullName     string    `json:"full_name" binding:"required,max=100"`
	DateOfBirth  time.Time `json:"date_of_birth" binding:"required"`
	AgreeToTerms bool      `json:"agree_to_terms" binding:"required"`
}

type UserPreferences struct {
	Theme         string   `json:"theme" binding:"oneof=light dark"`
	Language      string   `json:"language" binding:"required,len=2"`
	Notifications bool     `json:"notifications"`
	Categories    []string `json:"categories" binding:"dive,oneof=tech business sports"`
}

type UpdateUserRequest struct {
	FullName    *string          `json:"full_name,omitempty" binding:"omitempty,max=100"`
	Email       *string          `json:"email,omitempty" binding:"omitempty,email"`
	Preferences *UserPreferences `json:"preferences,omitempty"`
}

type SearchUsersQuery struct {
	Query    string `form:"q" binding:"required,min=1"`
	Category string `form:"category" binding:"omitempty,oneof=active inactive all"`
	Limit    int    `form:"limit" binding:"omitempty,min=1,max=100"`
	Offset   int    `form:"offset" binding:"omitempty,min=0"`
	SortBy   string `form:"sort" binding:"omitempty,oneof=name email created_at"`
	Order    string `form:"order" binding:"omitempty,oneof=asc desc"`
}

type UploadFileRequest struct {
	Title       string `form:"title" binding:"required,max=200"`
	Description string `form:"description" binding:"max=1000"`
	Category    string `form:"category" binding:"required,oneof=document image video"`
	Public      bool   `form:"public"`
}

type LoginRequest struct {
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required"`
}
