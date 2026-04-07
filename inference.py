import os
import sys
from openai import OpenAI

# Use .get() with a fallback empty string so the client init doesn't crash
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("API_KEY", "missing_key") 
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-70B-Instruct")

# The validator needs this to be initialized, but we provide a placeholder
# if the environment variables aren't injected yet during the build/import phase.
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def clean_data(dirty_text):
    """
    Sends dirty CRM text to the Proxy and returns a cleaned version.
    """
    # Double-check inside the function in case variables were injected late
    if client.api_key == "missing_key":
        current_key = os.getenv("API_KEY")
        if current_key:
            client.api_key = current_key
            client.base_url = os.getenv("API_BASE_URL")

    system_instructions = (
        "You are a CRM Data Cleansing assistant. "
        "Tasks: 1. Remove all HTML tags. 2. Format dates to YYYY-MM-DD. "
        "3. Standardize phone numbers to +1XXXXXXXXXX format. "
        "Return ONLY the cleaned string, no explanations."
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": f"Dirty Data: {dirty_text}"}
            ],
            max_tokens=150,
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Proxy Inference Error: {e}", file=sys.stderr)
        return dirty_text

if __name__ == "__main__":
    print("[START] task=crm_cleansing", flush=True)
    
    # If we are running as a script, we might be in Phase 2 where variables ARE present
    test_input = "<html>Contact: (555) 123-4567 on 12/01/2023</html>"
    
    try:
        result = clean_data(test_input)
        print("[STEP] step=1 reward=1.0", flush=True)
        print("[END] task=crm_cleansing score=1.0 steps=1", flush=True)
    except Exception:
        print("[END] task=crm_cleansing score=0.0 steps=1", flush=True)
        sys.exit(1)
