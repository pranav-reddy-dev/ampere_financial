import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL and KEY must be set in environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_or_create_customer(email: str) -> str:
    """
    Check if customer exists by email in Supabase.
    If not, create a new customer record with UUID.
    Returns the customer UUID.
    """
    try:
        # Check if customer exists
        response = supabase.table("customers").select("*").eq("email", email).execute()
        
        if response.data:
            return response.data[0]["id"]
        
        # Create new customer
        customer_id = str(uuid.uuid4())
        new_customer = {
            "id": customer_id,
            "email": email,
        }
        
        insert_response = supabase.table("customers").insert(new_customer).execute()
        
        if insert_response.error:
            raise Exception(f"Error creating customer: {insert_response.error.message}")
        
        return customer_id
        
    except Exception as e:
        raise Exception(f"Supabase error: {str(e)}")
