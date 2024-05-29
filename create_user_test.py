from faker import Faker
from models import User
import os
from dotenv import load_dotenv
from routers.listing import get_db

load_dotenv()

fake = Faker()


def run_user_test():
    db = next(get_db())
    try:
        for i in range(3):
            user = User(
                userName=fake.user_name(),
                hashedPassword=os.getenv('DEFAULT_USER_PASSWORD')
            )
            db.add(user)
            db.commit()
            print(f"Created user: {user.userName} / {os.getenv('DEFAULT_USER_PASSWORD')}")
    finally:
        db.close()