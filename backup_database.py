import sqlite3
import os
import shutil
from datetime import datetime

def backup_database():
    """Create a backup of the database"""
    if not os.path.exists('database/picknpay.db'):
        print("Database file not found")
        return
    
    # Create backups directory
    os.makedirs('database/backups', exist_ok=True)
    
    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f'database/backups/picknpay_backup_{timestamp}.db'
    
    # Copy database file
    shutil.copy2('database/picknpay.db', backup_file)
    print(f"Database backed up to: {backup_file}")

if __name__ == '__main__':
    backup_database()