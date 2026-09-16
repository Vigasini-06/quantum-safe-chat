from database import engine, Base
from models import User

print("Creating database...")

Base.metadata.create_all(bind=engine)

print("Database created successfully!")