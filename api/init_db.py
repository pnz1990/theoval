from app import create_app
from models import db

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
