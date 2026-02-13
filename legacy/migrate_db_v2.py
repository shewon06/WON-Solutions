import os
import sqlite3
from sqlalchemy import create_all
from app import create_app
from models import db
from dotenv import load_dotenv

load_dotenv(override=True)

def migrate_data():
    app = create_app()
    mysql_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    if not mysql_uri or 'mysql' not in mysql_uri:
        print("Error: SQLALCHEMY_DATABASE_URI in .env must be a MySQL URI.")
        return

    print(f"Connecting to MySQL: {mysql_uri}")
    
    # SQLite connection
    sqlite_path = 'system.db'
    if not os.path.exists(sqlite_path):
        print(f"Error: SQLite database not found at {sqlite_path}")
        return

    try:
        with app.app_context():
            # Initialize MySQL schema
            db.create_all()
            print("MySQL schema initialized.")

            # Connect to SQLite
            sl_conn = sqlite3.connect(sqlite_path)
            sl_cursor = sl_conn.cursor()

            # Get all tables
            sl_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in sl_cursor.fetchall() if t[0] not in ('sqlite_sequence', 'alembic_version')]

            for table in tables:
                print(f"Migrating table: {table}")
                sl_cursor.execute(f"SELECT * FROM {table}")
                rows = sl_cursor.fetchall()
                if not rows:
                    continue

                # Get columns
                sl_cursor.execute(f"PRAGMA table_info({table})")
                columns = [c[1] for c in sl_cursor.fetchall()]
                placeholders = ', '.join(['%s'] * len(columns))
                col_names = ', '.join(columns)

                # Insert into MySQL via raw SQL for simplicity if models aren't easy to map dynamically
                # But better to use SQLAlchemy core to be safe with types
                table_obj = db.Table(table, db.metadata, autoload_with=db.engine)
                
                # Clear target table first (optional, but safer for re-runs)
                db.session.execute(table_obj.delete())
                
                # Prepare data
                data = [dict(zip(columns, row)) for row in rows]
                
                # Bulk insert
                db.session.execute(table_obj.insert(), data)
                print(f"  Inserted {len(rows)} rows into {table}")

            db.session.commit()
            print("Migration completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == '__main__':
    migrate_data()
