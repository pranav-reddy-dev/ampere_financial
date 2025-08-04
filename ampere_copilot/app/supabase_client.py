import os
import uuid
import PyPDF2
import io
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_or_create_customer(email: str) -> dict:
    """
    Check if customer exists by email in Supabase.
    If not, create a new customer record with UUID.
    Returns the customer record.
    """
    response = supabase.table("customers").select("*").eq("email", email).execute()
    if response.error:
        raise Exception(f"Error querying Supabase: {response.error.message}")

    data = response.data
    if data:
        return data[0]

    # Create new customer
    customer_id = str(uuid.uuid4())
    new_customer = {
        "id": customer_id,
        "email": email,
    }
    insert_response = supabase.table("customers").insert(new_customer).execute()
    if insert_response.error:
        raise Exception(f"Error inserting customer: {insert_response.error.message}")

    return new_customer

def upload_pdf_to_supabase(uploaded_file, customer_email: str) -> str:
    """
    Upload PDF file to Supabase storage and return the file URL
    """
    try:
        # Get customer ID
        customer = get_or_create_customer(customer_email)
        customer_id = customer["id"]
        
        # Generate unique filename
        file_extension = uploaded_file.name.split('.')[-1]
        file_name = f"{customer_id}_{uuid.uuid4()}.{file_extension}"
        
        # Upload to Supabase storage
        bucket_name = "pdf-uploads"
        file_content = uploaded_file.getvalue()
        
        response = supabase.storage.from_(bucket_name).upload(
            file_name,
            file_content,
            {"content-type": "application/pdf"}
        )
        
        if response.error:
            raise Exception(f"Upload failed: {response.error.message}")
        
        # Get public URL
        file_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        return file_url
        
    except Exception as e:
        raise Exception(f"Error uploading PDF: {str(e)}")

def process_pdf_data(uploaded_file, customer_email: str):
    """
    Process PDF data and extract text content
    """
    try:
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text()
        
        # Store processed data
        pdf_data = {
            "customer_email": customer_email,
            "filename": uploaded_file.name,
            "text_content": text_content,
            "page_count": len(pdf_reader.pages)
        }
        
        return pdf_data
        
    except Exception as e:
        raise Exception(f"Error processing PDF data: {str(e)}")
