import asyncio
import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import text

from database.session import AsyncSessionLocal, Base, engine, get_db
from database.models import InsuranceRecord  

CSV_FILE = Path("data/insurance.csv")  

# ---------- helpers -------------------------------------------------
def read_csv() -> list[dict]:
    """Return list of row-dicts from CSV."""
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found at {CSV_FILE.absolute()}")
    return pd.read_csv(CSV_FILE).to_dict("records")

async def create_tables():
    """Table creation is now handled by create_tables.py"""
    return True 
     
async def seed_insurance_records():
    """Insert CSV rows into insurance_records with proper transaction handling."""
    try:
        rows = read_csv()
        if not rows:
            print("⚠️ No data to seed")
            return False
            
        async with AsyncSessionLocal() as session:
            try:
                # Verify the table exists
                result = await session.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name='insurance_records'")
                )
                if not result.scalar():
                    raise Exception("insurance_records table does not exist")
                
                # Insert records
                for i, row in enumerate(rows, 1):
                    try:
                        rec = InsuranceRecord(
                            age=int(row["age"]),
                            sex=str(row["sex"]),
                            bmi=float(row["bmi"]),
                            children=int(row["children"]),
                            smoker=str(row["smoker"]),
                            region=str(row["region"]),
                            charges=float(row["charges"]) if pd.notna(row["charges"]) else None,
                            is_training_data=True,
                            source="original",
                        )
                        session.add(rec)
                        # Commit in batches of 50
                        if i % 50 == 0:
                            await session.commit()
                            print(f"✅ Committed {i} records...")
                    except Exception as e:
                        print(f"❌ Error processing row {i}: {e}")
                        continue
                
                # Final commit for remaining records
                await session.commit()
                print(f"✅ Successfully seeded {len(rows)} insurance records")
                return True
                
            except Exception as e:
                await session.rollback()
                print(f"❌ Transaction failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error in seed_insurance_records: {e}")
        return False

# ---------- main ----------------------------------------------------
async def main():
    try:
        print("🚀 Starting database setup...")
        if not await create_tables():
            print("❌ Failed to create tables, aborting...")
            return False
            
        print("🌱 Seeding data...")
        if not await seed_insurance_records():
            print("❌ Failed to seed data")
            return False
            
        print("✅ Database setup and seeding completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        if not success:
            print("❌ Database setup and seeding failed")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)