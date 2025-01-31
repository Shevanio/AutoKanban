from app import db
from app.models import User
from werkzeug.security import generate_password_hash

def create_user(username, email, password):
    """Create a new user and add them to the database."""
    try:
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print(f"User {username} created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Failed to create user {username}: {e}")
    finally:
        db.session.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a new user.")
    parser.add_argument("username", type=str, help="Username for the new user")
    parser.add_argument("email", type=str, help="Email for the new user")
    parser.add_argument("password", type=str, help="Password for the new user")

    args = parser.parse_args()
    create_user(args.username, args.email, args.password)
