import csv
import logging
import datetime
import os
import socket

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging settings
logging.basicConfig(filename='logs/login.log', 
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def get_local_ip():
    """Retrieve the local IP address of the computer."""
    try:
        # Create a socket connection to a remote server (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        logging.error(f"Failed to retrieve IP address: {e}")
        return "Unknown IP"

def login(username, password):
    """Authenticate the user using credentials from a CSV file."""
    try:
        with open("UserInfo/UserAccounts.csv", newline='') as csvfile:
            reader = csv.reader(csvfile)
            user_found = False
            for row in reader:
                if username == row[0]:
                    user_found = True
                    if password == row[1]:
                        return True
                    else:
                        return False
            if not user_found:
                print("---> User not found.")
                return "not_found"
    except FileNotFoundError:
        logging.error("UserAccounts.csv file not found")
        return False

def log_user_not_found(username):
    """Log when the entered username is not found."""
    ip_address = get_local_ip()
    message = (
        f"Login Failed - User not found\n"
        f"  Account\t\t\t: {username}\n"
        f"  IP Address\t: {ip_address}\n"
        f"  Timestamp\t\t: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    logging.warning(message)

def log_login_success(username):
    """Log a successful login attempt."""
    ip_address = get_local_ip()
    greeting = "Login Successful!"
    log_message = (
        f"Login Successful\n"
        f"  Greeting\t\t: {greeting}\n"
        f"  Account\t\t\t: {username}\n"
        f"  IP Address\t: {ip_address}\n"
        f"  Timestamp\t\t: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    logging.info(log_message)
    print(greeting)

def log_login_failure(username):
    """Log a failed login attempt."""
    ip_address = get_local_ip()
    error_message = "Login Failed, Please Try Again!"
    log_message = (
        f"Login Failed\n"
        f"  Error\t\t\t\t: {error_message}\n"
        f"  Account\t\t\t: {username}\n"
        f"  IP Address\t: {ip_address}\n"
        f"  Timestamp\t\t: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    logging.warning(log_message)
    print(error_message)

def get_input_with_cancel(prompt):
    """Get input with cancel option."""
    user_input = input(prompt + "").strip()
    if user_input.lower() in ["cancel", "exit", "quit", "esc"]:
        print("\n---> Operation cancelled")
        return None
    return user_input

def authenticate_user():
    """Handle the user authentication process and return success status and username"""
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        print('\n======================================================= LOGIN SYSTEM ========================================================')
        
        username = get_input_with_cancel("- Enter Username\t.\t.\t.\t.\t.\t.\t: ")
        if username is None:
            return False, None
            
        password = get_input_with_cancel("- Enter Password\t.\t.\t.\t.\t.\t.\t: ")
        if password is None:
            return False, None
            
        print('\t')
        
        # Authenticate the user
        result = login(username, password)
        if result is True:
            log_login_success(username)
            return True, username
        elif result == "not_found":
            # Log the event and reprompt without counting as an attempt
            log_user_not_found(username)
            continue
        else:
            attempt += 1
            log_login_failure(username)
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"Login failed. {remaining} attempts remaining.")
            else:
                print("Maximum login attempts exceeded. Access denied.")
                
    return False, None