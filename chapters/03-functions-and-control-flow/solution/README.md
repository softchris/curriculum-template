# Restaurant Menu System - Solution

This directory contains the complete solution for Chapter 3's assignment: a restaurant menu system that demonstrates functions, control flow, and user interaction in Rust.

## Setup Instructions

1. Navigate to this directory:
   ```bash
   cd chapters/03-functions-and-control-flow/solution
   ```

2. Run the program:
   ```bash
   cargo run
   ```

3. Run the tests:
   ```bash
   cargo test
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

The program presents a main menu with these options:
1. **View Menu** - Display all available items organized by category
2. **Add Item to Order** - Select items and quantities to add to your order
3. **View Current Order** - See your current order with pricing breakdown
4. **Apply Discount Code** - Enter discount codes for special offers
5. **Checkout** - Complete your order and see the final receipt
6. **Exit** - Close the application

### Available Discount Codes
- `WELCOME10` - 10% welcome discount
- `STUDENT15` - 15% student discount  
- `FAMILY20` - 20% family discount

## Learning Points

This solution demonstrates:

### **Function Organization**
- **Separation of concerns**: Each function has a single, clear responsibility
- **Method organization**: Related functions grouped in `impl` blocks
- **Parameter design**: Proper use of `&self` vs `&mut self` for ownership

### **Control Flow Patterns**
- **Main menu loop**: Continues until user chooses to exit
- **Input validation loops**: Retry until valid input is received
- **Conditional logic**: Complex pricing calculations with discounts and tax
- **Pattern matching**: Robust handling of user input and menu selections

### **Data Structure Design**
```rust
#[derive(Debug, Clone)]
struct MenuItem {
    id: u8,
    name: String,
    price: f64,
    category: String,
}

struct Restaurant {
    menu: Vec<MenuItem>,
    order: Vec<OrderItem>,
    tax_rate: f64,
    discount_rate: f64,
}
```

### **Expression vs Statement Usage**
```rust
// Expression for conditional assignment
let discounted_subtotal = if self.discount_rate > 0.0 {
    subtotal * (1.0 - self.discount_rate)
} else {
    subtotal
};

// Match expression for discount codes
match code.to_uppercase().as_str() {
    "WELCOME10" => self.discount_rate = 0.10,
    "STUDENT15" => self.discount_rate = 0.15,
    // ...
}
```

### **Error Handling and Validation**
- Input validation with helpful error messages
- Graceful handling of invalid menu selections
- Prevention of empty orders at checkout
- Robust parsing with fallback behavior

## Expected Output

```
=== Welcome to Rusty's Restaurant ===

Main Menu:
1. View Menu
2. Add Item to Order
3. View Current Order
4. Apply Discount Code
5. Checkout
6. Exit

Please select an option (1-6): 1

=== MENU ===
Appetizers:
  1. Caesar Salad - $8.50
  2. Chicken Wings - $12.00
  3. Garlic Bread - $6.00

Main Courses:
  4. Grilled Salmon - $24.00
  5. Beef Burger - $16.50
  6. Pasta Primavera - $18.00

Desserts:
  7. Chocolate Cake - $7.50
  8. Ice Cream - $5.00
```

## Key Concepts Demonstrated

### **Function Parameters and Ownership**
```rust
fn display_menu(&self)              // Immutable borrow for reading
fn add_item_to_order(&mut self)     // Mutable borrow for modification
fn get_user_input(prompt: &str)     // String slice parameter
```

### **Control Flow Mastery**
- **Loop types**: `loop` for input validation, `for` for iteration
- **Conditional logic**: `if/else` expressions and `match` statements
- **Early returns**: Handling edge cases like empty orders

### **Expression-Based Programming**
- Using `if` expressions for conditional assignment
- Match expressions for complex decision logic
- Block expressions for scoped calculations

### **Iterator Usage**
```rust
let subtotal = self.order.iter()
    .map(|item| item.menu_item.price * item.quantity as f64)
    .sum();
```

## Testing

The solution includes comprehensive tests covering:
- Restaurant initialization
- Menu item verification
- Total calculations with and without discounts
- Edge cases like empty orders
- Multiple item scenarios

Run tests with:
```bash
cargo test
```

This demonstrates proper unit testing practices for Rust functions and validates the business logic of the restaurant system.