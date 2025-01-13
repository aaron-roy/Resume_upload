# Resume Parser API

A FastAPI application that parses PDF resumes, extracts information, and stores the parsed data in MongoDB. The application provides endpoints to upload and parse resumes, with support for both local MongoDB and MongoDB Atlas connections.

## Features

- PDF resume parsing
- MongoDB integration (local or Atlas)
- FastAPI backend with async support
- PDF to text conversion
- Structured data extraction from resumes

## Prerequisites

- Python 3.7+
- MongoDB (local installation or MongoDB Atlas account)
- Virtual environment management

## Project Structure

```
project/
├── main.py           # FastAPI application and endpoints
├── helper.py         # PDF parsing and conversion utilities
├── database.py       # MongoDB connection and CRUD operations
├── requirements.txt  # Project dependencies
└── .env             # Environment variables configuration
```

## Setup and Installation

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux
source .venv/bin/activate
# On Windows
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB

#### Option A: Local MongoDB

```bash
# Start MongoDB service (macOS with Homebrew)
brew services start mongodb-community@8.0

# Stop MongoDB service when needed
brew services stop mongodb-community@8.0
```

#### Option B: MongoDB Atlas

1. Create a `.env` file in the project root
2. Add your MongoDB connection string:
```
MONGO_DETAILS="your_mongodb_atlas_connection_string"
```

### 4. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Usage

### Parse Resume Endpoint

To parse a resume, send a POST request to the `/resume/parse` endpoint:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/resume/parse' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/resume.pdf'
```

### API Documentation

FastAPI automatically generates interactive API documentation. After starting the server, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Configuration

### Database Configuration

The application supports both local MongoDB and MongoDB Atlas. In `database.py`:

```python
# For local MongoDB
MONGO_DETAILS = "mongodb://localhost:27017"

# For MongoDB Atlas
MONGO_DETAILS = config("MONGO_DETAILS")
```

## Development

The project uses the following main components:
- `main.py`: FastAPI application and endpoint definitions
- `helper.py`: Utility functions for PDF processing and parsing
- `database.py`: MongoDB connection and database operations

## Error Handling

If you encounter connection issues:
1. Verify MongoDB is running (if using local installation)
2. Check MongoDB Atlas credentials in `.env` file (if using Atlas)
3. Ensure all dependencies are installed correctly
4. Verify the PDF file exists and is accessible

## License

[Add your license information here]
