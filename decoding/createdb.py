import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to SQLite database (creates it if not exists)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create the users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                  )''')

# Commit changes (table creation) and close connection
conn.commit()

def add_user():
    # Get username and password from user input
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        print("Username already exists. Please choose a different username.")
        return

    # Generate password hash
    password_hash = generate_password_hash(password)

    # Insert user into the users table
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))

    # Commit changes (user insertion)
    conn.commit()
    print("User added successfully.")

def view_users():
    # Fetch all users from the database
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Display the users
    if not users:
        print("No users found.")
    else:
        print("Users:")
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}")
            



def modify_user():
    user_id = input("Enter the ID of the user you want to modify: ")
    new_username = input("Enter new username (leave blank to keep current): ")
    new_password = input("Enter new password (leave blank to keep current): ")

    # Fetch the user from the database
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if user:
        # Update username and/or password if provided
        if new_username:
            cursor.execute("UPDATE users SET username=? WHERE id=?", (new_username, user_id))
        if new_password:
            password_hash = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password_hash=? WHERE id=?", (password_hash, user_id))

        # Commit changes
        conn.commit()
        print("User modified successfully.")
    else:
        print("User not found.")

def delete_user():
    user_id = input("Enter the ID of the user you want to delete: ")

    # Delete the user from the database
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))

    # Commit changes
    conn.commit()
    print("User deleted successfully.")

def update_password():
    username = input("Enter username: ")
    old_password = input("Enter old password: ")
    new_password = input("Enter new password: ")

    # Fetch the user from the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        # Check if old password matches
        if check_password_hash(user[2], old_password):
            # Generate password hash for new password
            password_hash = generate_password_hash(new_password)

            # Update password hash in the database
            cursor.execute("UPDATE users SET password_hash=? WHERE username=?", (password_hash, username))

            # Commit changes
            conn.commit()
            print("Password updated successfully.")
        else:
            print("Old password does not match. Password not updated.")
    else:
        print("User not found.")

def menu():
    while True:
        print("\nUser Management System")
        print("1. Add User")
        print("2. View Users")
        print("3. Modify User")
        print("4. Delete User")
        print("5. Update Password")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            view_users()
        elif choice == '3':
            modify_user()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            update_password()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Run the menu
menu()

# Close connection
conn.close()
