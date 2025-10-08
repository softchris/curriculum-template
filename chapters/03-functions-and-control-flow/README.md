# Functions and Control Flow

Programs that can only execute instructions in a straight line, from top to bottom, are like recipes that never allow you to taste as you go, adjust seasonings, or repeat steps until something is just right. Real software needs the ability to make decisions, repeat actions, and organize logic into reusable components. Without these capabilities, even simple programs become unwieldy masses of duplicated code, and complex programs become impossible to understand or maintain.

Consider a typical web application that handles user authentication. It must check if a password meets security requirements, validate user input, retry network connections when they fail, and route users to different pages based on their access levels. Each of these tasks requires the program to make decisions, repeat actions conditionally, and organize related operations into logical units. Without proper control flow and function organization, such an application would collapse under its own complexity.

Rust's approach to functions and control flow emphasizes both performance and safety. Unlike languages where function calls might have hidden costs or where control flow can lead to undefined behavior, Rust makes the costs explicit and ensures that all code paths are safe. This chapter will show you how to leverage these features to write programs that are not only correct and efficient, but also clear and maintainable.

## Introduction

Functions and control flow are the building blocks that transform simple, linear programs into sophisticated applications capable of making decisions, repeating actions, and organizing complex logic. In Rust, these features are designed with the same principles that guide the entire language: safety, performance, and explicitness.

Unlike many other programming languages, Rust makes important distinctions that affect how you write and think about code. The difference between expressions and statements isn't just academic—it changes how you structure your programs. The way ownership works with function parameters isn't just a rule to memorize—it's a design tool that helps you write more reliable code.

**What you'll learn in this chapter:**
- How to define and call functions with proper parameter handling and return values
- How to use conditional logic with if/else statements and expressions
- How to implement different types of loops for various iteration patterns
- How to understand and leverage the distinction between expressions and statements
- How to handle early returns and control complex program flow
- How to organize code into logical, reusable functions that work with Rust's ownership system

## Learning Objectives

By the end of this chapter, you will be able to:

- **Define and call functions** with parameters and return values, understanding how ownership affects parameter passing
- **Use conditional statements effectively** with if/else constructs for making logical decisions in your programs
- **Implement appropriate loop types** (loop, while, for) for different iteration scenarios and requirements
- **Distinguish between expressions and statements** and leverage this distinction to write more concise and readable code
- **Handle early returns and complex control flow** patterns to manage program execution effectively
- **Organize code into logical, reusable functions** that promote code clarity and maintenance while working within Rust's ownership system

## Understanding Functions in Rust

Functions are the primary way to organize code in Rust, allowing you to break complex problems into smaller, manageable pieces. But Rust functions are more than just ways to avoid repeating code—they're designed to work seamlessly with the ownership system, making it impossible to accidentally create memory safety issues through function calls.

In many programming languages, functions can be a source of subtle bugs. Parameters might be modified unexpectedly, memory might be allocated without being freed, or functions might access data they shouldn't. Rust's function system eliminates these categories of errors by making ownership and borrowing explicit in function signatures.

Understanding how functions work in Rust isn't just about syntax—it's about learning to think in terms of data ownership and responsibility. When you see a function signature in Rust, you immediately know whether it takes ownership of its parameters, borrows them temporarily, or returns ownership to the caller.

### Function Syntax and Basic Usage

Rust function syntax is designed to be clear and explicit about what the function does with its parameters and what it returns. Every function signature tells a complete story about data flow and ownership.

```rust
fn greet(name: &str) {
    println!("Hello, {}!", name);
}

fn main() {
    let user_name = "Alice";
    greet(user_name);
    println!("Still can use: {}", user_name); // Works because greet borrows
}
```

This simple example demonstrates fundamental function concepts:
- **Defines** a function with `fn` keyword and descriptive name
- **Takes** a string slice parameter, borrowing rather than taking ownership
- **Allows** the caller to continue using the parameter after the call
- **Follows** Rust naming conventions with snake_case function names

Functions with return values use the `->` syntax to specify the return type:

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b  // No semicolon - this is an expression
}

fn main() {
    let result = add(5, 3);
    println!("Result: {}", result);
}
```

This example shows return value handling:
- **Specifies** the return type explicitly with `-> i32`
- **Returns** a value using an expression (no semicolon)
- **Demonstrates** how the final expression becomes the return value
- **Shows** how return values can be captured and used

### Parameters and Ownership

One of Rust's most important features is how it handles ownership in function parameters. Understanding this concept is crucial for writing correct Rust code and avoiding compiler errors.

```rust
fn take_ownership(s: String) {
    println!("I now own: {}", s);
} // s goes out of scope and is dropped here

fn borrow_value(s: &String) {
    println!("I'm borrowing: {}", s);
} // s goes out of scope but nothing is dropped

fn main() {
    let my_string = String::from("Hello");
    
    borrow_value(&my_string);
    println!("Still have: {}", my_string); // This works
    
    take_ownership(my_string);
    // println!("Can't use: {}", my_string); // This would error
}
```

This example illustrates ownership in function parameters:
- **`take_ownership`** takes ownership of the `String`, consuming it
- **`borrow_value`** borrows a reference, allowing continued use
- **Demonstrates** how parameter types affect what happens to values
- **Shows** why borrowing is often preferred for reading data

For mutable references, you can allow functions to modify borrowed data:

```rust
fn modify_string(s: &mut String) {
    s.push_str(" World!");
}

fn main() {
    let mut message = String::from("Hello");
    modify_string(&mut message);
    println!("{}", message); // Prints "Hello World!"
}
```

Mutable references enable controlled modification:
- **Allows** functions to modify data without taking ownership
- **Requires** the original variable to be declared as mutable
- **Prevents** multiple mutable references to ensure safety
- **Returns** the modified data to the caller automatically

### Return Values and Early Returns

Rust functions can return values in several ways, and understanding these patterns helps you write more expressive and efficient code.

```rust
fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 {
        return None; // Early return for error case
    }
    Some(a / b) // Normal return case
}

fn main() {
    match divide(10.0, 2.0) {
        Some(result) => println!("Result: {}", result),
        None => println!("Cannot divide by zero"),
    }
}
```

This example demonstrates return value patterns:
- **Uses** `Option<T>` to handle potential failure cases
- **Implements** early returns with the `return` keyword
- **Leverages** the final expression as the default return
- **Forces** the caller to handle both success and failure cases

Functions can also return multiple values using tuples:

```rust
fn analyze_number(n: i32) -> (bool, bool, String) {
    let is_positive = n > 0;
    let is_even = n % 2 == 0;
    let description = if is_positive && is_even {
        "positive even".to_string()
    } else if is_positive {
        "positive odd".to_string()
    } else if is_even {
        "negative even".to_string()
    } else {
        "negative odd".to_string()
    };
    
    (is_positive, is_even, description)
}
```

Multiple return values provide rich information:
- **Returns** related data as a tuple
- **Combines** multiple boolean checks with descriptive text
- **Uses** conditional expressions to build complex return values
- **Allows** destructuring assignment in the caller

## Conditional Logic with If/Else

Conditional logic allows programs to make decisions based on data, user input, or environmental conditions. Rust's approach to conditionals emphasizes both safety and expressiveness, with some unique features that make code more concise and reliable.

Unlike many languages where conditionals are purely statements, Rust treats `if` constructs as expressions that can return values. This distinction enables more functional programming patterns and often leads to clearer, more maintainable code.

Understanding when to use `if` as an expression versus a statement, and how to structure complex conditional logic, will make your Rust programs more idiomatic and easier to reason about.

### If Expressions vs If Statements

Rust's `if` construct can be used both as a statement that performs actions and as an expression that produces values. This flexibility allows for more concise and functional programming patterns.

```rust
fn main() {
    let temperature = 75;
    
    // If as a statement
    if temperature > 70 {
        println!("It's warm today!");
    } else {
        println!("It's cool today!");
    }
    
    // If as an expression
    let clothing = if temperature > 70 {
        "shorts and t-shirt"
    } else {
        "jeans and sweater"
    };
    
    println!("Wear: {}", clothing);
}
```

This example shows both uses of `if`:
- **Statement form** performs actions (printing messages)
- **Expression form** produces values that can be assigned
- **Requires** both branches to return the same type when used as expression
- **Eliminates** the need for temporary variables in many cases

Complex conditional logic can be built using multiple conditions:

```rust
fn categorize_score(score: i32) -> &'static str {
    if score >= 90 {
        "Excellent"
    } else if score >= 80 {
        "Good"
    } else if score >= 70 {
        "Average"
    } else if score >= 60 {
        "Below Average"
    } else {
        "Needs Improvement"
    }
}

fn main() {
    let student_score = 85;
    let grade = categorize_score(student_score);
    println!("Grade: {}", grade);
}
```

Multi-branch conditionals provide clear decision logic:
- **Chains** multiple conditions using `else if`
- **Returns** string literals with `'static` lifetime
- **Evaluates** conditions in order, stopping at first match
- **Ensures** all possible cases are handled with final `else`

### Pattern Matching with Match

While `if/else` works well for simple conditions, Rust's `match` expression provides more powerful pattern matching capabilities for complex decision logic.

```rust
fn describe_day(day: u8) -> &'static str {
    match day {
        1 => "Monday - Start of the work week",
        2 => "Tuesday - Getting into the rhythm",
        3 => "Wednesday - Hump day",
        4 => "Thursday - Almost there",
        5 => "Friday - TGIF!",
        6 | 7 => "Weekend - Time to relax",
        _ => "Invalid day number",
    }
}

fn main() {
    for day in 1..=8 {
        println!("Day {}: {}", day, describe_day(day));
    }
}
```

Pattern matching provides exhaustive handling:
- **Matches** specific values with precise patterns
- **Combines** multiple values using the `|` operator
- **Handles** all other cases with the `_` wildcard
- **Ensures** compile-time exhaustiveness checking

Match can also work with more complex data structures:

```rust
fn process_option(value: Option<i32>) -> String {
    match value {
        Some(n) if n > 0 => format!("Positive number: {}", n),
        Some(n) if n < 0 => format!("Negative number: {}", n),
        Some(0) => "Zero".to_string(),
        None => "No value".to_string(),
    }
}

fn main() {
    let values = vec![Some(42), Some(-10), Some(0), None];
    
    for val in values {
        println!("{}", process_option(val));
    }
}
```

Advanced pattern matching includes:
- **Guard conditions** with `if` clauses for additional filtering
- **Destructuring** of complex data types like `Option<T>`
- **Specific value matching** combined with range conditions
- **Comprehensive handling** of all possible value states

### Boolean Logic and Complex Conditions

Rust provides standard boolean operators for building complex conditional expressions, with short-circuit evaluation for efficiency and safety.

```rust
fn check_access(age: u8, has_id: bool, is_member: bool) -> String {
    if age >= 18 && has_id {
        if is_member {
            "Full access granted".to_string()
        } else {
            "Basic access granted".to_string()
        }
    } else if age >= 16 && has_id && is_member {
        "Limited access granted".to_string()
    } else {
        "Access denied".to_string()
    }
}

fn main() {
    println!("{}", check_access(20, true, true));   // Full access
    println!("{}", check_access(17, true, true));   // Limited access  
    println!("{}", check_access(15, true, false));  // Access denied
}
```

Complex boolean logic enables sophisticated decision making:
- **Combines** multiple conditions with `&&` (and) and `||` (or)
- **Uses** short-circuit evaluation for efficiency
- **Nests** conditions for hierarchical decision logic
- **Provides** clear, readable condition evaluation

You can also use boolean logic in match guards:

```rust
fn classify_number(n: i32, check_even: bool) -> &'static str {
    match n {
        x if x > 0 && (!check_even || x % 2 == 0) => "Positive (and even if checking)",
        x if x < 0 && (!check_even || x % 2 == 0) => "Negative (and even if checking)",
        0 => "Zero",
        _ => "Positive/Negative odd (when checking even)",
    }
}
```

Guard conditions with boolean logic allow:
- **Complex conditions** within pattern matching
- **Conditional logic** that depends on multiple factors
- **Flexible matching** that can be enabled or disabled
- **Clear expression** of complex business rules

## Loops and Iteration

Loops allow programs to repeat actions efficiently, whether processing collections of data, waiting for conditions to change, or implementing algorithms that require iteration. Rust provides several loop constructs, each optimized for different use cases and patterns.

Rust's approach to loops emphasizes safety and performance. The compiler can often optimize loops heavily, and the ownership system ensures that loop bodies can't accidentally create memory safety issues. Understanding when to use each loop type will help you write more efficient and readable code.

Unlike some languages where loop choice is mostly stylistic, Rust's different loop types have distinct characteristics that make them better suited for specific scenarios. Choosing the right loop type isn't just about personal preference—it's about expressing intent clearly and leveraging compiler optimizations.

### The Loop Construct

The `loop` keyword creates an infinite loop that continues until explicitly broken. This is useful for event loops, servers, or any situation where you need to continue processing until a specific condition is met.

```rust
fn find_target(numbers: &[i32], target: i32) -> Option<usize> {
    let mut index = 0;
    
    loop {
        if index >= numbers.len() {
            break None; // Target not found
        }
        
        if numbers[index] == target {
            break Some(index); // Target found, return position
        }
        
        index += 1;
    }
}

fn main() {
    let numbers = [1, 5, 3, 8, 2, 7];
    
    match find_target(&numbers, 8) {
        Some(pos) => println!("Found at position: {}", pos),
        None => println!("Not found"),
    }
}
```

The `loop` construct provides maximum control:
- **Continues** indefinitely until explicit `break`
- **Allows** complex exit conditions with `break` values
- **Enables** early exits from nested logic
- **Guarantees** that the loop body executes at least once (if reached)

Loops can return values through the `break` statement:

```rust
fn get_user_choice() -> i32 {
    loop {
        println!("Enter a number between 1 and 10:");
        
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).expect("Failed to read line");
        
        match input.trim().parse::<i32>() {
            Ok(num) if num >= 1 && num <= 10 => break num,
            Ok(_) => println!("Number must be between 1 and 10"),
            Err(_) => println!("Please enter a valid number"),
        }
    }
}
```

Breaking with values enables:
- **Return values** from loop expressions
- **Error handling** within loop logic
- **Clean exit** conditions with computed results
- **Validation loops** that continue until correct input

### While Loops

While loops continue executing as long as a condition remains true. They're perfect for situations where you need to repeat an action until a specific state is reached.

```rust
fn countdown(mut seconds: u32) {
    while seconds > 0 {
        println!("{}...", seconds);
        seconds -= 1;
        std::thread::sleep(std::time::Duration::from_secs(1));
    }
    println!("Blast off! 🚀");
}

fn main() {
    countdown(5);
}
```

While loops provide condition-based iteration:
- **Tests** condition before each iteration
- **Exits** automatically when condition becomes false
- **Allows** modification of loop variables within the body
- **Provides** clear, readable iteration logic

While loops work well with complex conditions:

```rust
fn process_queue<T>(queue: &mut Vec<T>) -> usize 
where 
    T: std::fmt::Debug,
{
    let mut processed = 0;
    
    while !queue.is_empty() && processed < 100 {
        if let Some(item) = queue.pop() {
            println!("Processing: {:?}", item);
            processed += 1;
        }
    }
    
    processed
}

fn main() {
    let mut work_queue = vec![1, 2, 3, 4, 5];
    let count = process_queue(&mut work_queue);
    println!("Processed {} items", count);
}
```

Complex while conditions enable:
- **Multiple exit criteria** with boolean logic
- **Resource limits** to prevent infinite processing
- **State-dependent** iteration control
- **Flexible termination** based on various factors

### For Loops and Iterators

For loops provide the most ergonomic way to iterate over collections, ranges, and other iterable data structures. Rust's for loops are built on top of a powerful iterator system that enables both safety and performance.

```rust
fn main() {
    // Iterating over arrays
    let numbers = [1, 2, 3, 4, 5];
    for num in numbers {
        println!("Number: {}", num);
    }
    
    // Iterating over ranges
    for i in 0..5 {
        println!("Index: {}", i);
    }
    
    // Iterating with indices
    let names = ["Alice", "Bob", "Charlie"];
    for (index, name) in names.iter().enumerate() {
        println!("{}: {}", index, name);
    }
}
```

For loops provide elegant iteration:
- **Automatically** handles bounds checking and safety
- **Works** with arrays, vectors, ranges, and custom iterators
- **Provides** both values and indices when needed
- **Eliminates** manual index management and off-by-one errors

Iterator methods enable powerful data processing:

```rust
fn analyze_scores(scores: &[i32]) -> (f64, i32, i32) {
    let total: i32 = scores.iter().sum();
    let average = total as f64 / scores.len() as f64;
    
    let max_score = *scores.iter().max().unwrap_or(&0);
    let min_score = *scores.iter().min().unwrap_or(&0);
    
    (average, max_score, min_score)
}

fn main() {
    let test_scores = [85, 92, 78, 96, 88, 73, 91];
    let (avg, max, min) = analyze_scores(&test_scores);
    
    println!("Average: {:.1}", avg);
    println!("Highest: {}", max);
    println!("Lowest: {}", min);
    
    // Filter and collect
    let high_scores: Vec<i32> = test_scores
        .iter()
        .filter(|&&score| score >= 90)
        .copied()
        .collect();
    
    println!("High scores: {:?}", high_scores);
}
```

Iterator chains enable functional programming:
- **Chains** multiple operations for data transformation
- **Provides** lazy evaluation for efficiency
- **Enables** functional programming patterns
- **Maintains** memory safety throughout the pipeline

## Expressions vs Statements

Understanding the distinction between expressions and statements is crucial for writing idiomatic Rust code. This difference affects how you structure code, handle return values, and express logic concisely.

In many languages, this distinction is largely academic, but in Rust it's a practical tool that affects daily programming. Expressions produce values and can be used wherever a value is expected. Statements perform actions but don't produce values. This distinction enables more functional programming patterns and often leads to more readable code.

Learning to think in terms of expressions rather than statements will make your Rust code more concise and often more performant, as the compiler can better optimize expression-based code.

### Understanding the Distinction

Expressions evaluate to a value, while statements perform an action. This fundamental difference shapes how you write Rust code and enables powerful patterns not available in statement-based languages.

```rust
fn main() {
    // Statements - perform actions, don't return values
    let x = 5;                    // Variable binding statement
    let y = 10;                   // Another statement
    
    // Expression - evaluates to a value
    let sum = x + y;              // x + y is an expression
    
    // Block expression
    let result = {
        let doubled = x * 2;      // Statement inside block
        doubled + y               // Expression (no semicolon)
    };
    
    println!("Sum: {}, Result: {}", sum, result);
}
```

This example demonstrates the distinction:
- **Variable bindings** (`let x = 5;`) are statements
- **Arithmetic operations** (`x + y`) are expressions
- **Blocks** can be expressions when the last line has no semicolon
- **Semicolons** turn expressions into statements

Function calls and method calls are expressions:

```rust
fn calculate_area(length: f64, width: f64) -> f64 {
    length * width  // Expression - no semicolon
}

fn main() {
    // Function call is an expression
    let area = calculate_area(5.0, 3.0);
    
    // Method chains are expressions
    let message = "hello world"
        .to_uppercase()
        .replace("WORLD", "RUST");
    
    println!("Area: {}, Message: {}", area, message);
}
```

Expression-based programming enables:
- **Direct assignment** of computed values
- **Chaining** of operations for data transformation
- **Elimination** of temporary variables
- **More functional** programming patterns

### Using Expressions for Concise Code

Expression-oriented thinking leads to more concise and often more readable code by eliminating intermediate variables and making data flow more explicit.

```rust
fn classify_grade(score: i32) -> String {
    format!("Grade: {}", 
        if score >= 90 { "A" }
        else if score >= 80 { "B" }
        else if score >= 70 { "C" }
        else if score >= 60 { "D" }
        else { "F" }
    )
}

fn process_temperature(celsius: f64) -> String {
    let fahrenheit = celsius * 9.0 / 5.0 + 32.0;
    
    format!("{:.1}°C = {:.1}°F ({})", 
        celsius, 
        fahrenheit,
        match fahrenheit {
            f if f > 80.0 => "hot",
            f if f > 60.0 => "warm",
            f if f > 40.0 => "cool",
            _ => "cold",
        }
    )
}

fn main() {
    println!("{}", classify_grade(85));
    println!("{}", process_temperature(25.0));
}
```

Expression-based patterns provide:
- **Inline conditions** for direct value assignment
- **Nested expressions** that build complex results
- **Elimination** of intermediate variables
- **Clear data flow** from input to output

Complex expressions can be broken across lines for readability:

```rust
fn calculate_monthly_payment(principal: f64, rate: f64, years: i32) -> f64 {
    let monthly_rate = rate / 12.0;
    let num_payments = years * 12;
    
    principal * (
        monthly_rate * (1.0 + monthly_rate).powi(num_payments)
    ) / (
        (1.0 + monthly_rate).powi(num_payments) - 1.0
    )
}

fn loan_summary(principal: f64, rate: f64, years: i32) -> String {
    let monthly = calculate_monthly_payment(principal, rate, years);
    let total = monthly * (years * 12) as f64;
    let interest = total - principal;
    
    format!(
        "Loan: ${:.2}\nMonthly: ${:.2}\nTotal: ${:.2}\nInterest: ${:.2}",
        principal, monthly, total, interest
    )
}
```

Multi-line expressions maintain readability while:
- **Preserving** the expression nature of complex calculations
- **Breaking** long lines for better readability
- **Maintaining** clear mathematical relationships
- **Enabling** direct use in further expressions

### Block Expressions and Scope

Blocks in Rust are expressions that can contain statements and end with an expression. This enables creating local scopes for intermediate calculations while still producing a final value.

```rust
fn main() {
    let result = {
        let base = 10;
        let exponent = 3;
        let power = base.pow(exponent);
        
        // This expression becomes the block's value
        power + 1000
    }; // Variables base, exponent, power are dropped here
    
    println!("Result: {}", result); // Only result is available here
}
```

Block expressions provide:
- **Local scope** for intermediate calculations
- **Automatic cleanup** of temporary variables
- **Expression semantics** for assignment and return values
- **Clear separation** of complex calculation logic

Blocks are particularly useful in function definitions:

```rust
fn analyze_text(text: &str) -> (usize, usize, f64) {
    let word_count = {
        text.split_whitespace().count()
    };
    
    let char_count = {
        text.chars().filter(|c| c.is_alphabetic()).count()
    };
    
    let average_word_length = {
        if word_count > 0 {
            char_count as f64 / word_count as f64
        } else {
            0.0
        }
    };
    
    (word_count, char_count, average_word_length)
}

fn main() {
    let text = "Hello, Rust programming world!";
    let (words, chars, avg_len) = analyze_text(text);
    
    println!("Words: {}, Characters: {}, Average length: {:.1}", 
             words, chars, avg_len);
}
```

Block-based organization enables:
- **Logical grouping** of related calculations
- **Intermediate variable isolation** to prevent naming conflicts
- **Clear structure** for complex functions
- **Maintainable code** with well-defined scope boundaries

## Assignment

Now it's time to apply your understanding of functions and control flow by building a comprehensive application that demonstrates all the concepts you've learned. This assignment will challenge you to organize code logically, implement proper control flow, and create a user-friendly interface.

**Project: Restaurant Menu System**

Create a Rust program that implements a text-based menu system for a restaurant. Users should be able to view menu items, add items to their order, calculate totals with tax and discounts, and complete their order. This project will test your ability to organize code into functions, implement control flow logic, and handle user interactions.

### Requirements

Your restaurant menu system should:

1. **Display a menu** with categories (appetizers, mains, desserts) and prices
2. **Allow users to add items** to their order with quantity selection
3. **Show current order** with items, quantities, and subtotals
4. **Calculate totals** including tax and applicable discounts
5. **Apply discounts** based on order value or special promotions
6. **Handle invalid input** gracefully with clear error messages
7. **Provide a complete ordering workflow** from menu browsing to checkout

### Expected Behavior

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

Please select an option (1-6): 2

Enter item number (1-8): 5
Enter quantity: 2
Added 2x Beef Burger to your order.

Please select an option (1-6): 3

=== YOUR ORDER ===
2x Beef Burger - $33.00
Subtotal: $33.00
Tax (8.5%): $2.81
Total: $35.81

Please select an option (1-6): 5

=== CHECKOUT ===
Final Order:
2x Beef Burger - $33.00

Subtotal: $33.00
Tax (8.5%): $2.81
Total: $35.81

Thank you for dining with us!
```

### Technical Requirements

- Use functions to organize different parts of the system (display menu, add items, calculate totals, etc.)
- Implement proper control flow with loops for the main menu and input validation
- Use appropriate data structures (vectors, tuples, or structs) to represent menu items and orders
- Handle user input validation with helpful error messages
- Use expressions where appropriate to make code more concise
- Implement at least one discount system (percentage off, buy-one-get-one, etc.)

### Learning Goals

This assignment helps you practice:
- **Organizing code into logical functions** with clear responsibilities
- **Implementing control flow** with loops and conditional logic
- **Handling user input and menu systems** with proper validation
- **Using expressions and statements** appropriately for clean code
- **Managing program state** across multiple function calls
- **Creating intuitive user interfaces** for command-line applications

### Implementation Hints

- Create separate functions for each menu option (view_menu, add_item, etc.)
- Use a loop for the main menu that continues until the user chooses to exit
- Consider using enums or constants for menu items to avoid magic numbers
- Implement input validation functions that can be reused
- Use match statements for handling menu selections
- Consider using a vector of tuples or a simple struct to represent the current order

Take your time to plan the structure before coding. Think about what data needs to be passed between functions and how to organize the code for maximum readability and maintainability.

## Solution

Here's a complete implementation of the Restaurant Menu System that demonstrates professional code organization, proper control flow, and user-friendly interface design in Rust.

```rust
use std::io;
use std::io::Write;

#[derive(Debug, Clone)]
struct MenuItem {
    id: u8,
    name: String,
    price: f64,
    category: String,
}

#[derive(Debug, Clone)]
struct OrderItem {
    menu_item: MenuItem,
    quantity: u32,
}

struct Restaurant {
    menu: Vec<MenuItem>,
    order: Vec<OrderItem>,
    tax_rate: f64,
    discount_rate: f64,
}
```

The data structures establish the foundation:
- **Defines** clear types for menu items and order items
- **Uses** `Clone` trait to allow copying when needed
- **Organizes** restaurant state in a single struct
- **Separates** concerns between menu data and order data

```rust
impl Restaurant {
    fn new() -> Self {
        Restaurant {
            menu: Self::create_menu(),
            order: Vec::new(),
            tax_rate: 0.085,
            discount_rate: 0.0,
        }
    }
    
    fn create_menu() -> Vec<MenuItem> {
        vec![
            MenuItem { id: 1, name: "Caesar Salad".to_string(), price: 8.50, category: "Appetizers".to_string() },
            MenuItem { id: 2, name: "Chicken Wings".to_string(), price: 12.00, category: "Appetizers".to_string() },
            MenuItem { id: 3, name: "Garlic Bread".to_string(), price: 6.00, category: "Appetizers".to_string() },
            MenuItem { id: 4, name: "Grilled Salmon".to_string(), price: 24.00, category: "Main Courses".to_string() },
            MenuItem { id: 5, name: "Beef Burger".to_string(), price: 16.50, category: "Main Courses".to_string() },
            MenuItem { id: 6, name: "Pasta Primavera".to_string(), price: 18.00, category: "Main Courses".to_string() },
            MenuItem { id: 7, name: "Chocolate Cake".to_string(), price: 7.50, category: "Desserts".to_string() },
            MenuItem { id: 8, name: "Ice Cream".to_string(), price: 5.00, category: "Desserts".to_string() },
        ]
    }
}
```

The initialization methods provide:
- **Factory method** for creating new restaurant instances
- **Static menu creation** with predefined items
- **Proper categorization** of menu items
- **Realistic pricing** for a restaurant context

```rust
impl Restaurant {
    fn display_menu(&self) {
        println!("\n=== MENU ===");
        
        let categories = ["Appetizers", "Main Courses", "Desserts"];
        
        for category in categories {
            println!("{}:", category);
            for item in &self.menu {
                if item.category == category {
                    println!("  {}. {} - ${:.2}", item.id, item.name, item.price);
                }
            }
            println!();
        }
    }
    
    fn add_item_to_order(&mut self) {
        self.display_menu();
        
        let item_id = loop {
            match get_user_input("Enter item number (1-8): ").parse::<u8>() {
                Ok(id) if id >= 1 && id <= 8 => break id,
                _ => println!("Please enter a valid item number (1-8)."),
            }
        };
        
        let quantity = loop {
            match get_user_input("Enter quantity: ").parse::<u32>() {
                Ok(q) if q > 0 => break q,
                _ => println!("Please enter a valid quantity (greater than 0)."),
            }
        };
        
        if let Some(menu_item) = self.menu.iter().find(|item| item.id == item_id).cloned() {
            let order_item = OrderItem { menu_item: menu_item.clone(), quantity };
            self.order.push(order_item);
            println!("Added {}x {} to your order.", quantity, menu_item.name);
        }
    }
}
```

The menu and ordering functions demonstrate:
- **Clear separation** of display and interaction logic
- **Input validation loops** ensuring correct user input
- **Error handling** with helpful feedback messages
- **Menu item lookup** using iterator methods

```rust
impl Restaurant {
    fn view_current_order(&self) {
        println!("\n=== YOUR ORDER ===");
        
        if self.order.is_empty() {
            println!("Your order is empty.");
            return;
        }
        
        for order_item in &self.order {
            let item_total = order_item.menu_item.price * order_item.quantity as f64;
            println!("{}x {} - ${:.2}", 
                     order_item.quantity, 
                     order_item.menu_item.name, 
                     item_total);
        }
        
        let (subtotal, tax, total) = self.calculate_totals();
        println!("\nSubtotal: ${:.2}", subtotal);
        
        if self.discount_rate > 0.0 {
            let discount_amount = subtotal * self.discount_rate;
            println!("Discount ({:.1}%): -${:.2}", self.discount_rate * 100.0, discount_amount);
            let discounted_subtotal = subtotal - discount_amount;
            let discounted_tax = discounted_subtotal * self.tax_rate;
            println!("Tax ({:.1}%): ${:.2}", self.tax_rate * 100.0, discounted_tax);
            println!("Total: ${:.2}", discounted_subtotal + discounted_tax);
        } else {
            println!("Tax ({:.1}%): ${:.2}", self.tax_rate * 100.0, tax);
            println!("Total: ${:.2}", total);
        }
    }
    
    fn calculate_totals(&self) -> (f64, f64, f64) {
        let subtotal = self.order.iter()
            .map(|item| item.menu_item.price * item.quantity as f64)
            .sum();
        
        let discounted_subtotal = if self.discount_rate > 0.0 {
            subtotal * (1.0 - self.discount_rate)
        } else {
            subtotal
        };
        
        let tax = discounted_subtotal * self.tax_rate;
        let total = discounted_subtotal + tax;
        
        (subtotal, tax, total)
    }
}
```

The order management functions provide:
- **Comprehensive order display** with formatting
- **Detailed cost breakdown** including tax and discounts
- **Flexible calculation logic** handling discount scenarios
- **Clear financial summary** for customer review

```rust
impl Restaurant {
    fn apply_discount_code(&mut self) {
        let code = get_user_input("Enter discount code: ");
        
        match code.to_uppercase().as_str() {
            "WELCOME10" => {
                self.discount_rate = 0.10;
                println!("Applied 10% welcome discount!");
            }
            "STUDENT15" => {
                self.discount_rate = 0.15;
                println!("Applied 15% student discount!");
            }
            "FAMILY20" => {
                self.discount_rate = 0.20;
                println!("Applied 20% family discount!");
            }
            _ => {
                println!("Invalid discount code. Please try again.");
            }
        }
    }
    
    fn checkout(&mut self) {
        if self.order.is_empty() {
            println!("Your order is empty. Please add items before checkout.");
            return;
        }
        
        println!("\n=== CHECKOUT ===");
        println!("Final Order:");
        
        for order_item in &self.order {
            let item_total = order_item.menu_item.price * order_item.quantity as f64;
            println!("{}x {} - ${:.2}", 
                     order_item.quantity, 
                     order_item.menu_item.name, 
                     item_total);
        }
        
        let (subtotal, tax, total) = self.calculate_totals();
        println!("\nSubtotal: ${:.2}", subtotal);
        
        if self.discount_rate > 0.0 {
            let discount_amount = subtotal * self.discount_rate;
            println!("Discount ({:.1}%): -${:.2}", self.discount_rate * 100.0, discount_amount);
        }
        
        println!("Tax ({:.1}%): ${:.2}", self.tax_rate * 100.0, tax);
        println!("Total: ${:.2}", total);
        println!("\nThank you for dining with us!");
        
        // Clear the order for next customer
        self.order.clear();
        self.discount_rate = 0.0;
    }
}
```

The discount and checkout systems demonstrate:
- **Code-based discount system** with multiple options
- **Case-insensitive input handling** for user convenience
- **Complete transaction processing** with order clearing
- **Professional checkout experience** with detailed receipts

```rust
fn get_user_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read input");
    input.trim().to_string()
}

fn display_main_menu() {
    println!("\nMain Menu:");
    println!("1. View Menu");
    println!("2. Add Item to Order");
    println!("3. View Current Order");
    println!("4. Apply Discount Code");
    println!("5. Checkout");
    println!("6. Exit");
}

fn main() {
    let mut restaurant = Restaurant::new();
    
    println!("=== Welcome to Rusty's Restaurant ===");
    
    loop {
        display_main_menu();
        
        match get_user_input("\nPlease select an option (1-6): ").parse::<u8>() {
            Ok(1) => restaurant.display_menu(),
            Ok(2) => restaurant.add_item_to_order(),
            Ok(3) => restaurant.view_current_order(),
            Ok(4) => restaurant.apply_discount_code(),
            Ok(5) => restaurant.checkout(),
            Ok(6) => {
                println!("Thank you for visiting Rusty's Restaurant!");
                break;
            }
            _ => println!("Please enter a valid option (1-6)."),
        }
    }
}
```

The main program flow provides:
- **Clean utility functions** for input and display
- **Main menu loop** with proper exit handling
- **Comprehensive option handling** using match expressions
- **User-friendly interface** with clear prompts and feedback

### Key Learning Points

This solution demonstrates advanced Rust concepts and best practices:

**Function Organization:**
```rust
impl Restaurant {
    fn display_menu(&self) { /* read-only operations */ }
    fn add_item_to_order(&mut self) { /* state modification */ }
}
```
- **Groups** related functionality in implementation blocks
- **Uses** appropriate mutability (`&self` vs `&mut self`)
- **Separates** concerns into focused, single-purpose functions

**Control Flow Patterns:**
```rust
loop {
    match get_user_input().parse::<u8>() {
        Ok(id) if id >= 1 && id <= 8 => break id,
        _ => println!("Please enter a valid item number."),
    }
}
```
- **Combines** loops with pattern matching for robust input validation
- **Uses** guard conditions for range checking
- **Provides** clear error feedback for invalid input

**Expression-Based Design:**
```rust
let discounted_subtotal = if self.discount_rate > 0.0 {
    subtotal * (1.0 - self.discount_rate)
} else {
    subtotal
};
```
- **Uses** if expressions for conditional value assignment
- **Eliminates** temporary variables where possible
- **Maintains** clear mathematical relationships

## Quiz

Test your understanding of functions and control flow concepts:

**Question 1:** What's the difference between `if` as an expression vs a statement in Rust?

a) Expressions return values, statements don't ✓  
b) There is no difference  
c) Expressions are faster  

**Question 2:** Which loop type is best for iterating over a collection with automatic bounds checking?

a) `loop`  
b) `while`  
c) `for` ✓  

**Answers:**

**Question 1:** a) Expressions return values, statements don't

**Explanation:** In Rust, expressions evaluate to a value and can be used anywhere a value is expected, while statements perform actions but don't return values. This distinction allows you to write more concise code by using `if` expressions for conditional assignment: `let x = if condition { 5 } else { 10 };` rather than using temporary variables and separate assignment statements.

**Question 2:** c) `for`

**Explanation:** For loops in Rust are specifically designed for iterating over collections and provide automatic bounds checking, making them the safest choice. They work with iterators and prevent common errors like off-by-one mistakes or accessing invalid indices. While `loop` and `while` can iterate over collections, they require manual index management and bounds checking, making them more error-prone for this use case.

## Summary

Congratulations! You've mastered the essential tools for controlling program flow and organizing code in Rust. This chapter has equipped you with the knowledge to write programs that can make decisions, repeat actions efficiently, and structure complex logic in maintainable ways.

### What You've Accomplished

**Technical Mastery:**
- Learned to define and call functions with proper parameter handling and ownership semantics
- Mastered conditional logic using if/else constructs both as statements and expressions
- Implemented all three loop types (loop, while, for) and understand when to use each
- Distinguished between expressions and statements to write more concise and functional code
- Handled complex control flow patterns including early returns and nested logic
- Organized code into logical, reusable functions that work seamlessly with Rust's ownership system

**Problem-Solving Skills:**
- Built a complete restaurant menu system with multiple interacting components
- Implemented robust user input validation with helpful error messages
- Designed intuitive user interfaces for command-line applications
- Created flexible systems that handle edge cases and invalid input gracefully
- Applied functional programming concepts using expressions and iterator chains

**Software Design Understanding:**
- Experienced how proper function organization leads to maintainable code
- Learned to balance code reuse with clarity and single responsibility
- Understood how control flow choices affect both performance and readability
- Developed patterns for handling user interaction and state management

### Key Insights for Your Rust Journey

**Functions as Building Blocks:** Rust functions are more than code organization tools—they're integral to the ownership system. Understanding how ownership flows through function calls will help you design better APIs and avoid common borrowing issues as your programs grow in complexity.

**Expression-Oriented Thinking:** Learning to prefer expressions over statements will make your Rust code more concise and often more performant. This functional approach scales well to complex data transformations and makes code easier to reason about.

**Control Flow as a Design Tool:** The choice between different loop types and conditional patterns isn't just about personal preference—it communicates intent and helps the compiler optimize your code. Using the right construct for each situation makes programs more readable and maintainable.

**Safety Through Structure:** Rust's control flow constructs eliminate entire categories of bugs common in other languages. The compiler ensures that all code paths are safe, loops don't access invalid memory, and pattern matching is exhaustive.

### The Foundation for Advanced Concepts

The concepts you've learned in this chapter are fundamental to everything that follows in Rust programming. Understanding functions prepares you for more advanced topics like generics, traits, and lifetimes. Control flow mastery enables you to write complex algorithms and handle sophisticated data processing. Expression-based thinking sets you up for success with functional programming patterns and iterator chains.

As your programs grow in complexity, these fundamentals become even more valuable. The patterns you've learned here—organizing code into focused functions, using appropriate control flow, and thinking in terms of expressions—scale seamlessly to large applications and complex systems.

### Next Steps

In the next chapter, we'll explore Rust's most distinctive feature: the ownership system. You'll learn how Rust prevents memory safety errors without garbage collection, understand borrowing and references, and discover how ownership rules help you write more reliable programs. The function concepts you've mastered here will be essential as you learn how ownership flows through function calls and returns.

The control flow patterns you've practiced will become the backbone of more sophisticated algorithms and data processing pipelines. As you progress through the remaining chapters, you'll see how these fundamental concepts combine with Rust's more advanced features to create a powerful and expressive programming environment.

Remember that mastery comes through practice. Try implementing variations of the restaurant system—perhaps a library checkout system, a simple game, or a task manager. Each project will reinforce these concepts while introducing new challenges that prepare you for advanced Rust programming.

Every expert Rust developer has internalized these patterns of function organization and control flow. You're now equipped with the same foundational tools they use to build everything from command-line utilities to web servers to systems software. The logical thinking and code organization skills you've developed here will serve you well throughout your programming career, in Rust and beyond.