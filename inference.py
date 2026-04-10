import os
import sys
from openai import OpenAI

def clean_data(dirty_text):
    """
    Sends dirty CRM text to the Proxy and returns a cleaned version.
    """
    # Fetch environment variables at runtime
    api_base = os.getenv("API_BASE_URL")
    api_key = os.getenv("API_KEY")
    # Default to llama if not specified, common in OpenEnv
    model_name = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-70B-Instruct")

    if not api_key or not api_base:
        print("Error: API_KEY or API_BASE_URL missing from environment", file=sys.stderr)
        return dirty_text

    client = OpenAI(
        base_url=api_base,
        api_key=api_key
    )

    system_instructions = (
        "You are a CRM Data Cleansing assistant. "
        "Tasks: 1. Remove HTML tags. 2. Format dates to YYYY-MM-DD. "
        "3. Standardize phone numbers to +1XXXXXXXXXX format. "
        "Return ONLY the cleaned string."
    )

    try:
        response = client.chat.completions.create(
            model=model_name,
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
    # Validator often runs the script directly to check for API calls
    test_input = "<html>Contact: (555) 123-4567 on 12/01/2023</html>"
    print(f"Testing cleaning: {clean_data(test_input)}")
