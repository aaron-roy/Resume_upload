from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Define the "Introduction" part of the resume
class IntroductionModel(BaseModel):
    first_name: str = Field(..., example="User Name")
    last_name: str = Field(..., example="User Last Name")
    title: str = Field(..., example="User Title")
    tagline: str = Field(..., example="Prudent Software Engineer.")

# Define the "Contact" part of the resume
class ContactModel(BaseModel):
    email: EmailStr = Field(..., example="abc@woyage.ai")
    phone: str = Field(..., example="1111111111")
    address_line: str = Field(..., example="abc Dr")
    address_city: str = Field(..., example="San Francisco")
    address_state: str = Field(..., example="CA")
    address_zipcode: str = Field(..., example="00000")
    address_country: str = Field(..., example="United States")
    linkedin: Optional[str] = Field(None, example="linkedin.com/user-111")

# Define the "Summary" part of the resume
class SummaryModel(BaseModel):
    description: str = Field(..., example="Highly motivated software engineer with expertise in backend development.")

# Define the entire resume schema
class ResumeSchema(BaseModel):
    introduction: IntroductionModel
    contact: ContactModel
    summary: SummaryModel

    class Config:
        json_schema_extra = {
            "example": {
                "introduction": {
                    "first_name": "User Name",
                    "last_name": "User Last Name",
                    "title": "User Title",
                    "tagline": "Prudent Software Engineer."
                },
                "contact": {
                    "email": "abc@woyage.ai",
                    "phone": "1111111111",
                    "address_line": "abc Dr",
                    "address_city": "San Francisco",
                    "address_state": "CA",
                    "address_zipcode": "00000",
                    "address_country": "United States",
                    "linkedin": "linkedin.com/user-111"
                },
                "summary": {
                    "description": "Highly motivated software engineer with expertise in backend development."
                }
            }
        }

# Example function for generating a response model (you can use it to format responses)
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message,
    }
