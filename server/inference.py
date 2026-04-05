import os
from huggingface_hub import InferenceClient

# Get configuration from Space Variables/Secrets
model_name = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-70B-Instruct")
api_token = os.getenv("HF_TOKEN")

client = InferenceClient(model=model_name, token=api_token)

def clean_data(dirty_text):
    """
    Sends dirty CRM text to Llama-3 and returns a cleaned version.
    """
    system_instructions = (
        "You are a CRM Data Cleansing assistant. "
        "Tasks: 1. Remove all HTML tags. 2. Format dates to YYYY-MM-DD. "
        "3. Standardize phone numbers to +1XXXXXXXXXX format. "
        "Return ONLY the cleaned string, no explanations."
    )
    
    try:
        response = client.text_generation(
            prompt=f"{system_instructions}\n\nDirty Data: {dirty_text}\nCleaned Data:",
            max_new_tokens=150,
            temperature=0.1 # Low temperature for consistent formatting
        )
        return response.strip()
    except Exception as e:
        print(f"Inference Error: {e}")
        return dirty_text # Fallback to original if AI fails
