# Personal Budget Calculator - Solution

This directory contains the complete solution for Chapter 2's assignment: a personal budget calculator that demonstrates variable management, data type selection, and safe arithmetic operations.

## Setup Instructions

1. Navigate to this directory:
   ```bash
   cd chapters/02-variables-data-types-and-basic-operations/solution
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

The program will prompt you for:
1. Your monthly income (in dollars)
2. Multiple expense categories and amounts
3. Type 'done' when finished entering expenses

It will then display:
- A detailed budget summary
- Expense breakdown with percentages
- Budget status and personalized advice

## Learning Points

This solution demonstrates:
- **Variable mutability management**: Using `mut` only when necessary
- **Data type selection**: `f64` for monetary calculations, `String` for categories
- **Input validation**: Robust error handling for user input
- **Arithmetic operations**: Safe calculations with overflow consideration
- **Type conversion**: Safe parsing from strings to numbers
- **Professional formatting**: Currency display and user-friendly output

## Expected Output

```
=== Personal Budget Calculator ===

Enter your monthly income: $3500.50
Income recorded: $3,500.50

Enter expense categories and amounts (type 'done' when finished):

Expense category: Rent
Amount: $1200.00
Added: Rent - $1,200.00

Expense category: Groceries
Amount: $400.25
Added: Groceries - $400.25

Expense category: done

=== Budget Summary ===
Monthly Income:    $  3,500.50
Total Expenses:    $  1,600.25
Remaining Budget:  $  1,900.25

Expense Breakdown:
  Rent            $ 1200.00 ( 34.3%)
  Groceries       $  400.25 ( 11.4%)

Status: ✓ You're within budget! Well done.
```

## Key Concepts Demonstrated

### Variable Mutability
```rust
let income = get_monthly_income();      // Immutable - never changes
let mut expenses = Vec::new();          // Mutable - grows with input
```

### Data Type Selection
```rust
let income: f64                         // Decimal precision for money
let expenses: Vec<(String, f64)>        // Paired category and amount data
```

### Safe Type Conversion
```rust
match input.parse::<f64>() {
    Ok(amount) if amount >= 0.0 => return amount,
    Ok(_) => println!("Amount cannot be negative."),
    Err(_) => println!("Please enter a valid amount."),
}
```

### Error Handling
- Graceful handling of invalid numeric input
- Validation of negative amounts
- User-friendly error messages with examples