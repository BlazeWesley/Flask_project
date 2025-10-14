import sqlite3
import os
from datetime import datetime

def export_database_to_sql():
    """Export database to SQL file"""
    if not os.path.exists('database/picknpay.db'):
        print("Database file not found")
        return
    
    conn = sqlite3.connect('database/picknpay.db')
    cursor = conn.cursor()
    
    with open('database/picknpay.sql', 'w', encoding='utf-8') as sql_file:
        sql_file.write(f'-- Pick n Pay Database Export\n')
        sql_file.write(f'-- Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            if table_name == 'sqlite_sequence':
                continue
                
            # Write table schema
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
            schema = cursor.fetchone()[0]
            sql_file.write(f'{schema};\n\n')
            
            # Write table data
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            if rows:
                sql_file.write(f'-- Data for {table_name}\n')
                for row in rows:
                    values = []
                    for value in row:
                        if value is None:
                            values.append('NULL')
                        elif isinstance(value, str):
                            values.append(f"'{value.replace("'", "''")}'")
                        else:
                            values.append(str(value))
                    
                    sql_file.write(f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n")
                sql_file.write('\n')
    
    conn.close()
    print("Database exported to database/picknpay.sql")

if __name__ == '__main__':
    export_database_to_sql()