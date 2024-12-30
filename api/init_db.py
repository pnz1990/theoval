from app import create_app  # Ensure importing from the correct app module
from common.models import db

def init_db():
    """
    Initializes the database by creating all tables.
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
