import sqlite3
import datetime

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('testtime.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  start_time DATETIME,
                  end_time DATETIME,
                  total_time INTEGER)''')

# Function to calculate total time difference
# class TimeFunction:
def calculate_total_time(start_time, end_time):
    duration = end_time - start_time
    total_seconds = duration.total_seconds()
    total_minutes = int(total_seconds / 60)
    return total_minutes

# Function to log in user
def log_in_user(username):
    return datetime.datetime.now()

# Function to log off user and calculate total time spent
def log_off_user(username, start_time):
    end_time = datetime.datetime.now()
    total_time = calculate_total_time(start_time, end_time)
    #return total_time
    # Insert the user session details into the database
    cursor.execute("INSERT INTO user_sessions (username, start_time, end_time, total_time) VALUES (?, ?, ?, ?)",
                   (username, start_time, end_time, total_time))

    # Commit the changes
    conn.commit()

    # Print a message to confirm successful log off
    print(f"User '{username}' logged off. Total time spent: {total_time} minutes.")

# Example usage
username = "John"  # Replace with the actual username
start_time = log_in_user(username)

# Perform user activities...

log_off_user(username, start_time)

# Close the database connection
conn.close()
