import os
from openai import OpenAI

def process_task(input_data):
    # 1. Fetch the injected environment variables
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("API_BASE_URL")

    # 2. Initialize the client using the PROXY variables
    # This is the CRITICAL part for the "Task Validation" check
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    # 3. Make the call (ensure you're using a model name allowed by OpenEnv)
    response = client.chat.completions.create(
        model="gpt-4o-mini", # or the specific model required for Phase 2
        messages=[{"role": "user", "content": input_data}]
    )
    
    return response.choices[0].message.content
