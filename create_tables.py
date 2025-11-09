# create_tables.py
import sys
from sqlalchemy import create_engine, text
from core.config import DATABASE_URL
from database.models import Base

def create_tables():
    try:
        # Create a synchronous SQLite engine
        sync_engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""))
        
        # Drop all tables
        print("Dropping existing tables...")
        Base.metadata.drop_all(sync_engine)
        
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(sync_engine)
        
        # Verify tables were created
        with sync_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND name IN ('insurance_records', 'prediction_results', 'model_metadata')
            """))
            created_tables = {row[0] for row in result}
            expected_tables = {'insurance_records', 'prediction_results', 'model_metadata'}
            
            if created_tables != expected_tables:
                missing = expected_tables - created_tables
                raise Exception(f"Failed to create tables: {', '.join(missing)}")
        
        print("✅ All tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)