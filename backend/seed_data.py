import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    print("🌱 Seeding database...")
    
    # Clear existing data
    await db.users.delete_many({})
    await db.departments.delete_many({})
    await db.complaints.delete_many({})
    
    # Seed departments
    departments = [
        {
            "department_id": "DEPT_UTIL",
            "name": "Utilities Department",
            "categories": ["Utilities", "Water", "Electricity"],
            "zones": ["North", "South", "East", "West"],
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "department_id": "DEPT_MUN",
            "name": "Municipal Department",
            "categories": ["Sanitation", "Waste"],
            "zones": ["North", "South", "East", "West"],
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "department_id": "DEPT_POL",
            "name": "Police Department",
            "categories": ["Safety", "Police"],
            "zones": ["North", "South", "East", "West"],
            "created_at": datetime.utcnow().isoformat()
        },
        {
            "department_id": "DEPT_HLT",
            "name": "Health Department",
            "categories": ["Health", "Medical"],
            "zones": ["North", "South", "East", "West"],
            "created_at": datetime.utcnow().isoformat()
        }
    ]
    
    await db.departments.insert_many(departments)
    print(f"✅ Seeded {len(departments)} departments")
    
    # Seed users
    users = [
        {
            "user_id": "USR_ADMIN1",
            "name": "Admin User",
            "email": "admin@grievance.gov.in",
            "phone": "+919876543210",
            "role": "admin",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "USR_OFF001",
            "name": "Rajesh Kumar",
            "email": "rajesh.officer@grievance.gov.in",
            "phone": "+919876543211",
            "role": "officer",
            "department_id": "DEPT_UTIL",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "USR_OFF002",
            "name": "Priya Sharma",
            "email": "priya.officer@grievance.gov.in",
            "phone": "+919876543212",
            "role": "officer",
            "department_id": "DEPT_MUN",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    ]
    
    await db.users.insert_many(users)
    print(f"✅ Seeded {len(users)} users")
    
    print("🎉 Database seeding complete!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
