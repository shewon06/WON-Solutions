import sqlite3
import os

def migrate():
    db_path = 'instance/system.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Starting migration...")

    # Columns to add to 'sale' table
    sale_cols = [
        ('subtotal', 'FLOAT DEFAULT 0.0'),
        ('vat_amount', 'FLOAT DEFAULT 0.0'),
        ('tax_amount', 'FLOAT DEFAULT 0.0'),
        ('is_vat_inclusive', 'BOOLEAN DEFAULT 1')
    ]

    for col_name, col_def in sale_cols:
        try:
            cursor.execute(f"ALTER TABLE sale ADD COLUMN {col_name} {col_def};")
            print(f"Added {col_name} to sale table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists in sale table.")
            else:
                print(f"Error adding {col_name} to sale table: {e}")

    # Columns to add to 'expense' table
    expense_cols = [
        ('vat_amount', 'FLOAT DEFAULT 0.0'),
        ('expense_date', 'DATE'),
        ('is_paid', 'BOOLEAN DEFAULT 1')
    ]

    for col_name, col_def in expense_cols:
        try:
            cursor.execute(f"ALTER TABLE expense ADD COLUMN {col_name} {col_def};")
            print(f"Added {col_name} to expense table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists in expense table.")
            else:
                print(f"Error adding {col_name} to expense table: {e}")
    
    # Columns to add to 'company_master' table
    company_cols = [
        ('website_domain', 'VARCHAR(200)')
    ]

    for col_name, col_def in company_cols:
        try:
            cursor.execute(f"ALTER TABLE company_master ADD COLUMN {col_name} {col_def};")
            print(f"Added {col_name} to company_master table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"Column {col_name} already exists in company_master table.")
            else:
                print(f"Error adding {col_name} to company_master table: {e}")

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == '__main__':
    migrate()
