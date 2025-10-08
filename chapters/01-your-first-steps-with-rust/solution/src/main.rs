use std::io;
use std::io::Write;

fn main() {
    println!("Welcome to the Personal Information Display Program!");
    println!();
    
    // Get user's name
    let name = get_user_input("Please enter your name: ");
    
    // Get user's age with validation
    let age = loop {
        let age_input = get_user_input("Please enter your age: ");
        match age_input.parse::<u32>() {
            Ok(age) => break age,
            Err(_) => println!("Please enter a valid number for age."),
        }
    };
    
    // Get user's favorite color
    let color = get_user_input("Please enter your favorite color: ");
    
    // Display the formatted information
    display_user_info(&name, age, &color);
}

/// Prompts the user with the given message and returns their input as a trimmed String
fn get_user_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap(); // Ensure prompt appears before input
    
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
    
    input.trim().to_string()
}

/// Displays the user's information in a formatted manner
fn display_user_info(name: &str, age: u32, color: &str) {
    println!();
    println!("=== Your Information ===");
    println!("Name: {}", name);
    println!("Age: {} years old", age);
    println!("Favorite Color: {}", color);
    println!();
    println!("Thank you for using our program, {}!", name);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_display_user_info() {
        // This test verifies the function compiles and runs without panicking
        display_user_info("Test User", 25, "green");
    }
}