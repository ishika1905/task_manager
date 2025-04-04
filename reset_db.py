# reset_db.py

from app.database import Base, engine
import app.models  # Ensure models are imported so Base is aware of them

# Drop all tables
Base.metadata.drop_all(bind=engine)
print("All tables dropped.")

# Create all tables
Base.metadata.create_all(bind=engine)
print("All tables created.")
