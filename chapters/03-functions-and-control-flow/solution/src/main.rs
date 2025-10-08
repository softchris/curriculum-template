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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_restaurant_creation() {
        let restaurant = Restaurant::new();
        assert_eq!(restaurant.menu.len(), 8);
        assert_eq!(restaurant.order.len(), 0);
        assert_eq!(restaurant.tax_rate, 0.085);
        assert_eq!(restaurant.discount_rate, 0.0);
    }

    #[test]
    fn test_menu_items() {
        let restaurant = Restaurant::new();
        let caesar_salad = restaurant.menu.iter().find(|item| item.id == 1).unwrap();
        assert_eq!(caesar_salad.name, "Caesar Salad");
        assert_eq!(caesar_salad.price, 8.50);
        assert_eq!(caesar_salad.category, "Appetizers");
    }

    #[test]
    fn test_calculate_totals_no_discount() {
        let mut restaurant = Restaurant::new();
        
        // Add a burger (id: 5, price: 16.50)
        let burger = restaurant.menu.iter().find(|item| item.id == 5).unwrap().clone();
        restaurant.order.push(OrderItem { menu_item: burger, quantity: 2 });
        
        let (subtotal, tax, total) = restaurant.calculate_totals();
        assert_eq!(subtotal, 33.0); // 16.50 * 2
        assert!((tax - 2.805).abs() < 0.01); // 33.0 * 0.085
        assert!((total - 35.805).abs() < 0.01); // 33.0 + 2.805
    }

    #[test]
    fn test_calculate_totals_with_discount() {
        let mut restaurant = Restaurant::new();
        restaurant.discount_rate = 0.10; // 10% discount
        
        // Add a burger (id: 5, price: 16.50)
        let burger = restaurant.menu.iter().find(|item| item.id == 5).unwrap().clone();
        restaurant.order.push(OrderItem { menu_item: burger, quantity: 2 });
        
        let (subtotal, tax, total) = restaurant.calculate_totals();
        assert_eq!(subtotal, 33.0); // 16.50 * 2
        let discounted_subtotal = 33.0 * 0.9; // 29.7
        let expected_tax = discounted_subtotal * 0.085; // 2.5245
        let expected_total = discounted_subtotal + expected_tax; // 32.2245
        
        assert!((total - expected_total).abs() < 0.01);
    }

    #[test]
    fn test_empty_order() {
        let restaurant = Restaurant::new();
        let (subtotal, tax, total) = restaurant.calculate_totals();
        assert_eq!(subtotal, 0.0);
        assert_eq!(tax, 0.0);
        assert_eq!(total, 0.0);
    }

    #[test]
    fn test_multiple_items() {
        let mut restaurant = Restaurant::new();
        
        // Add Caesar Salad (id: 1, price: 8.50) and Ice Cream (id: 8, price: 5.00)
        let salad = restaurant.menu.iter().find(|item| item.id == 1).unwrap().clone();
        let ice_cream = restaurant.menu.iter().find(|item| item.id == 8).unwrap().clone();
        
        restaurant.order.push(OrderItem { menu_item: salad, quantity: 1 });
        restaurant.order.push(OrderItem { menu_item: ice_cream, quantity: 2 });
        
        let (subtotal, _tax, _total) = restaurant.calculate_totals();
        assert_eq!(subtotal, 18.5); // 8.50 + (5.00 * 2)
    }
}