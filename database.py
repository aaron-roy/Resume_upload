import motor.motor_asyncio
from decouple import config
import certifi
from bson.objectid import ObjectId

# MongoDB connection details for local
# MONGO_DETAILS = "mongodb://localhost:27017"

MONGO_DETAILS = config("MONGO_DETAILS")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())

# Select database and collection
database = client.resumes
resume_collection = database.get_collection("resumes_collection")

# Helper function to convert resume MongoDB document to dictionary
def resume_helper(resume) -> dict:
    return {
        "id": str(resume["_id"]),
        "introduction": {
            "first_name": resume["introduction"]["first_name"],
            "last_name": resume["introduction"]["last_name"],
            "title": resume["introduction"]["title"],
            "tagline": resume["introduction"]["tagline"]
        },
        "contact": {
            "email": resume["contact"]["email"],
            "phone": resume["contact"]["phone"],
            "address_line": resume["contact"]["address_line"],
            "address_city": resume["contact"]["address_city"],
            "address_state": resume["contact"]["address_state"],
            "address_zipcode": resume["contact"]["address_zipcode"],
            "address_country": resume["contact"]["address_country"],
            "linkedin": resume["contact"].get("linkedin", None)  # Optional field
        },
        "summary": resume["summary"]
    }

# Retrieve all resumes from the database
async def retrieve_resumes():
    resumes = []
    async for resume in resume_collection.find():
        resumes.append(resume_helper(resume))
    return resumes


# Add a new resume to the database
async def add_resume(resume_data: dict) -> dict:
    resume = await resume_collection.insert_one(resume_data)
    new_resume = await resume_collection.find_one({"_id": resume.inserted_id})
    return resume_helper(new_resume)


# Retrieve a resume with a matching ID
async def retrieve_resume(id: str) -> dict:
    resume = await resume_collection.find_one({"_id": ObjectId(id)})
    if resume:
        return resume_helper(resume)
    return None  # In case resume not found


# Update a resume with a matching ID
async def update_resume(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    resume = await resume_collection.find_one({"_id": ObjectId(id)})
    if resume:
        updated_resume = await resume_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_resume.modified_count > 0:
            # Return the updated resume
            updated_resume = await resume_collection.find_one({"_id": ObjectId(id)})
            return resume_helper(updated_resume)
        return False
    return False  # In case resume not found


# Delete a resume from the database
async def delete_resume(id: str):
    resume = await resume_collection.find_one({"_id": ObjectId(id)})
    if resume:
        await resume_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False  # In case resume not found