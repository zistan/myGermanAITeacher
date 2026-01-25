"""Test database insert to diagnose registration error"""
import sys
import traceback
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import get_password_hash

def test_user_creation():
    """Test creating a user in the database"""
    db = SessionLocal()

    try:
        # Hash password
        hashed_password = get_password_hash("SecurePass123")

        # Create user
        db_user = User(
            username="testuser_direct",
            email="testdirect@example.com",
            password_hash=hashed_password,
            native_language="it",
            target_language="de",
            proficiency_level="C1",
            settings={}
        )

        print(f"Created user object: {db_user}")

        # Add to database
        db.add(db_user)
        print("Added to session")

        # Commit
        db.commit()
        print("Committed successfully")

        # Refresh
        db.refresh(db_user)
        print(f"User created with ID: {db_user.id}")

        return True

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        db.rollback()
        return False

    finally:
        db.close()

if __name__ == "__main__":
    success = test_user_creation()
    sys.exit(0 if success else 1)
