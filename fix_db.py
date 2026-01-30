import sqlite3
import os

db_path = 'instance/jewelry.db'

if not os.path.exists(db_path):
    print(f"Database {db_path} not found.")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Checking daily_log table schema...")
    cursor.execute("PRAGMA table_info(daily_log)")
    columns_info = cursor.fetchall()
    
    columns = [info[1] for info in columns_info]
    print(f"Columns found: {columns}")
    
    if 'quantity' not in columns:
        print("Column 'quantity' missing. Attempting to add it...")
        try:
            cursor.execute("ALTER TABLE daily_log ADD COLUMN quantity INTEGER DEFAULT 0")
            conn.commit()
            print("Successfully added 'quantity' column.")
        except Exception as e:
            print(f"Error adding column: {e}")
    else:
        print("Column 'quantity' already exists.")
        
    conn.close()

except Exception as e:
    print(f"Database error: {e}")
