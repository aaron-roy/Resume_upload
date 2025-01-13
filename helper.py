import fitz  # PyMuPDF
import spacy
import re

def clean_phone_number(phone: str) -> str:
    """Clean phone number by removing non-digit characters."""
    return ''.join(char for char in phone if char.isdigit())

# Load SpaCy's pre-trained model (English)
nlp = spacy.load("en_core_web_sm")
def parse_resume(text: str)->dict:
    """
        Parse resume text into structured format using spaCy and regex.

        Args:
            text (str): Raw text extracted from resume PDF

        Returns:
            Dict[str, Any]: Structured resume data
    """
    # Load spaCy model
    # nlp = spacy.load("en_core_web_sm")

    # Clean up the text - remove extra whitespace and normalize newlines
    text = re.sub(r'\n+', '\n', text.strip())
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Initialize result structure
    result = {
        "introduction": {
            "first_name": "",
            "last_name": "",
            "title": "",
            "tagline": ""
        },
        "contact": {
            "email": "",
            "phone": "",
            "address_line": "",
            "address_city": "",
            "address_state": "",
            "address_zipcode": "",
            "address_country": "",
            "linkedin": ""
        },
        "summary": {
            "description": ""
        }
    }

    # Extract name (assumed to be first line)
    if lines:
        # Use spaCy for name extraction
        name_doc = nlp(lines[0])
        person_names = [ent.text for ent in name_doc.ents if ent.label_ == "PERSON"]
        if person_names:
            name_parts = person_names[0].split()
            if len(name_parts) >= 2:
                result["introduction"]["first_name"] = name_parts[0]
                result["introduction"]["last_name"] = name_parts[-1]
        else:  # Fallback to simple splitting
            name_parts = lines[0].split()
            if len(name_parts) >= 2:
                result["introduction"]["first_name"] = name_parts[0]
                result["introduction"]["last_name"] = name_parts[-1]

    # Extract title (assumed to be second line)
    if len(lines) > 1:
        result["introduction"]["title"] = lines[1]

    # Extract tagline (assumed to be third line)
    if len(lines) > 2:
        result["introduction"]["tagline"] = lines[2]

    # Extract contact information using regex patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\+?1?\s*[\(-]?\d{3}[\)-]?\s*\d{3}[-.]?\s*\d{4}'
    linkedin_pattern = r'linkedin\.com/[^\s]+'

    email_match = re.search(email_pattern, text)
    if email_match:
        result["contact"]["email"] = email_match.group()

    phone_match = re.search(phone_pattern, text)
    if phone_match:
        result["contact"]["phone"] = clean_phone_number(phone_match.group())

    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        result["contact"]["linkedin"] = linkedin_match.group()

    # Improved address parsing
    # First find the street address with number
    address_line_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Circle|Cir|Court|Ct|Place|Pl|Terrace|Ter|Way|Parkway|Pkwy)\b'
    address_match = re.search(address_line_pattern, text, re.IGNORECASE)
    if address_match:
        result["contact"]["address_line"] = address_match.group().strip()

        # Look for city, state, zip after the street address
        after_street = text[address_match.end():]
        city_state_pattern = r'([A-Za-z\s]+),\s*([A-Z]{2})\s*,?\s*(\d{5})(?:[,-]\s*([^,\n]+))?'
        location_match = re.search(city_state_pattern, after_street)
        if location_match:
            result["contact"]["address_city"] = location_match.group(1).strip()
            result["contact"]["address_state"] = location_match.group(2).strip()
            result["contact"]["address_zipcode"] = location_match.group(3).strip()
            if location_match.group(4):  # Country is optional
                result["contact"]["address_country"] = location_match.group(4).strip()

    # Extract summary
    # Find the content after contact information
    contact_elements = [
        result["contact"]["email"],
        result["contact"]["phone"],
        result["contact"]["linkedin"],
        result["contact"]["address_line"]
    ]

    # Find the last position of contact information
    last_contact_pos = max(
        (text.find(elem) + len(elem) for elem in contact_elements if elem),
        default=0
    )

    # Get the text after the last contact information
    summary_text = text[last_contact_pos:].strip()

    # Split into paragraphs and take the first substantial paragraph
    summary_paragraphs = summary_text.split('\n\n')
    for paragraph in summary_paragraphs:
        cleaned_paragraph = paragraph.strip()
        if len(cleaned_paragraph) > 100 and '@' not in cleaned_paragraph and 'linkedin' not in cleaned_paragraph.lower():
            result["summary"]["description"] = re.sub(r'\s+', ' ', cleaned_paragraph)
            break

    return result

# Convert PDF to String (given pdf_path)
def extract_pdf_text(pdf_path: str)->str:
    """
            Convert pdf file to string format

            Args:
                pdf_path (str): path to pdf

            Returns:
                str: pdf content as a string
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

