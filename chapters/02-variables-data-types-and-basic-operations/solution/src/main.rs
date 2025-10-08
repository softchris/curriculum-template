use std::io;
use std::io::Write;

fn main() {
    println!("=== Personal Budget Calculator ===");
    println!();
    
    // Get monthly income from user
    let income = get_monthly_income();
    println!("Income recorded: ${:.2}", income);
    println!();
    
    // Collect expenses from user
    let expenses = collect_expenses();
    
    // Calculate and display budget summary
    display_budget_summary(income, &expenses);
}

/// Prompts the user for their monthly income and validates the input
fn get_monthly_income() -> f64 {
    loop {
        print!("Enter your monthly income: $");
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin()
            .read_line(&mut input)
            .expect("Failed to read line");
        
        // Remove $ symbol if present and parse
        let cleaned_input = input.trim().trim_start_matches('$');
        
        match cleaned_input.parse::<f64>() {
            Ok(amount) if amount >= 0.0 => return amount,
            Ok(_) => println!("Income cannot be negative. Please try again."),
            Err(_) => println!("Please enter a valid dollar amount (e.g., 3500.50)"),
        }
        println!();
    }
}

/// Collects expense entries from the user until they type 'done'
fn collect_expenses() -> Vec<(String, f64)> {
    let mut expenses = Vec::new();
    
    println!("Enter expense categories and amounts (type 'done' when finished):");
    println!();
    
    loop {
        // Get expense category
        print!("Expense category: ");
        io::stdout().flush().unwrap();
        
        let mut category = String::new();
        io::stdin()
            .read_line(&mut category)
            .expect("Failed to read line");
        
        let category = category.trim().to_string();
        
        // Check if user wants to finish
        if category.to_lowercase() == "done" {
            break;
        }
        
        if category.is_empty() {
            println!("Category cannot be empty. Please try again.");
            continue;
        }
        
        // Get expense amount
        let amount = get_expense_amount();
        
        expenses.push((category.clone(), amount));
        println!("Added: {} - ${:.2}", category, amount);
        println!();
    }
    
    expenses
}

/// Gets a valid expense amount from the user
fn get_expense_amount() -> f64 {
    loop {
        print!("Amount: $");
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin()
            .read_line(&mut input)
            .expect("Failed to read line");
        
        let cleaned_input = input.trim().trim_start_matches('$');
        
        match cleaned_input.parse::<f64>() {
            Ok(amount) if amount >= 0.0 => return amount,
            Ok(_) => println!("Amount cannot be negative. Please try again."),
            Err(_) => println!("Please enter a valid dollar amount (e.g., 150.75)"),
        }
    }
}

/// Displays a formatted budget summary and analysis
fn display_budget_summary(income: f64, expenses: &[(String, f64)]) {
    println!("=== Budget Summary ===");
    
    // Calculate total expenses
    let total_expenses: f64 = expenses.iter().map(|(_, amount)| amount).sum();
    let remaining_budget = income - total_expenses;
    
    // Display financial overview
    println!("Monthly Income:    ${:>10.2}", income);
    println!("Total Expenses:    ${:>10.2}", total_expenses);
    println!("Remaining Budget:  ${:>10.2}", remaining_budget);
    println!();
    
    // Display detailed expense breakdown if there are expenses
    if !expenses.is_empty() {
        println!("Expense Breakdown:");
        for (category, amount) in expenses {
            let percentage = (amount / income) * 100.0;
            println!("  {:<15} ${:>8.2} ({:>5.1}%)", category, amount, percentage);
        }
        println!();
    }
    
    // Provide budget status and advice
    display_budget_status(remaining_budget, income, total_expenses);
}

/// Analyzes budget status and provides helpful feedback
fn display_budget_status(remaining: f64, income: f64, expenses: f64) {
    if remaining >= 0.0 {
        println!("Status: ✓ You're within budget! Well done.");
        
        if remaining < income * 0.1 {
            println!("Tip: You're using most of your income. Consider building an emergency fund.");
        } else if remaining > income * 0.3 {
            println!("Tip: Great savings potential! Consider investing or saving more.");
        }
    } else {
        println!("⚠️  WARNING: You're overspending by ${:.2}!", remaining.abs());
        println!("You need to reduce expenses or increase income.");
        
        // Suggest percentage reduction needed
        let reduction_needed = (expenses - income) / expenses * 100.0;
        println!("Consider reducing expenses by {:.1}% to break even.", reduction_needed);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_budget_calculation() {
        let income = 3000.0;
        let expenses = vec![
            ("Rent".to_string(), 1200.0),
            ("Groceries".to_string(), 400.0),
        ];
        
        let total_expenses: f64 = expenses.iter().map(|(_, amount)| amount).sum();
        let remaining = income - total_expenses;
        
        assert_eq!(total_expenses, 1600.0);
        assert_eq!(remaining, 1400.0);
    }

    #[test]
    fn test_budget_status_positive() {
        // Test should not panic for positive budget
        display_budget_status(500.0, 3000.0, 2500.0);
    }

    #[test]
    fn test_budget_status_negative() {
        // Test should not panic for negative budget
        display_budget_status(-200.0, 3000.0, 3200.0);
    }

    #[test]
    fn test_empty_expenses() {
        let income = 3000.0;
        let expenses = vec![];
        
        // Should not panic with empty expenses
        display_budget_summary(income, &expenses);
    }
}