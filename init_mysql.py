from app import create_app
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

def init_db():
    print(f"Connecting to: {os.getenv('SQLALCHEMY_DATABASE_URI')}")
    try:
        with app.app_context():
            db.create_all()
            print("Database schema initialized successfully in MySQL.")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    init_db()
