import os
import logging
from openai import OpenAI

# Ensuring output is clean for the grader to parse
logging.basicConfig(level=logging.INFO, format='%(message)s')

def run_inference(prompt):
    """
    Standardized inference engine for OpenEnv Round 1.
    Uses OpenAI Client and structured logging [START], [STEP], [END].
    """
    # [START] - Required by openenv gate
    print("[START]")
    
    # Task 4: Environment Variable Wiring
    api_key = os.getenv("HF_TOKEN")
    base_url = os.getenv("API_BASE_URL")
    model_name = os.getenv("MODEL_NAME")

    # Guard clause for missing configuration
    if not api_key or not base_url:
        print("[STEP] Error: Missing environment variables (HF_TOKEN or API_BASE_URL)")
        print("[END]")
        return None

    # Initialize the compliant OpenAI Client
    client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    try:
        print(f"[STEP] Sending request to model: {model_name}")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a professional CRM Data Auditor. Return only cleaned data or specific flags."},
                {"role": "user", "content": prompt}
            ],
            temperature=0, # Deterministic for grading consistency
            max_tokens=500
        )
        
        output = response.choices[0].message.content
        
        # [STEP] - Process and display the raw output for the grader
        print("[STEP] Inference complete. Resulting data:")
        print(output)
        
        return output

    except Exception as e:
        print(f"[STEP] Critical failure: {str(e)}")
        return None
        
    finally:
        # [END] - Required by openenv gate
        print("[END]")

if __name__ == "__main__":
    # Test execution
    sample_data = "raw_input: 'mArY sMiTh, mary.s@gmial.com, 555-0192'"
    run_inference(f"Clean and format this CRM record: {sample_data}")