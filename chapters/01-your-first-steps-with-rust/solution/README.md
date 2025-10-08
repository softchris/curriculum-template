# Personal Information Display Program - Solution

This directory contains the complete solution for Chapter 1's assignment.

## Setup Instructions

1. Navigate to this directory:
   ```bash
   cd chapters/01-your-first-steps-with-rust/solution
   ```

2. Run the program:
   ```bash
   cargo run
   ```

## Project Structure

```
solution/
├── Cargo.toml          # Project configuration
├── src/
│   └── main.rs         # Complete solution implementation
└── README.md           # This file
```

## How to Use

The program will prompt you for:
1. Your name
2. Your age (must be a valid number)
3. Your favorite color

It will then display your information in a formatted greeting.

## Learning Points

This solution demonstrates:
- User input handling with error validation
- Function organization and code structure
- String manipulation and type conversion
- Professional error handling patterns
- Clear user interface design

## Expected Output

```
Welcome to the Personal Information Display Program!

Please enter your name: Alice Johnson
Please enter your age: 28
Please enter your favorite color: blue

=== Your Information ===
Name: Alice Johnson
Age: 28 years old
Favorite Color: blue

Thank you for using our program, Alice!
```