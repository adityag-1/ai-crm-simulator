import re

def calculate_reward(task_id, model_output, expected_data=None):
    """
    Evaluates the model_output based on the task difficulty.
    Returns a score between 0.0 and 1.0.
    """
    score = 0.0
    
    # Task 1: EASY - Standardizing Casing
    if task_id == "task_easy":
        # Criteria: Proper Case Name, Lowercase Email
        name_match = re.search(r'[A-Z][a-z]+ [A-Z][a-z]+', model_output)
        email_match = re.search(r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}', model_output)
        
        if name_match and email_match:
            score = 1.0
        elif name_match or email_match:
            score = 0.5

    # Task 2: MEDIUM - Duplicate & Typo Flagging
    elif task_id == "task_medium":
        # Criteria: Must identify 'DUPLICATE' or 'TYPO' in the response
        flags = ["DUPLICATE", "TYPO", "FLAG"]
        if any(flag in model_output.upper() for flag in flags):
            score = 1.0
        else:
            score = 0.0

    # Task 3: HARD - Missing Data Reconstruction
    elif task_id == "task_hard":
        # Criteria: Must reconstruct a valid (XXX) XXX-XXXX phone format
        phone_pattern = r'\(\d{3}\) \d{3}-\d{4}'
        if re.search(phone_pattern, model_output):
            score = 1.0
        else:
            score = 0.2  # Partial credit for trying

    print(f"[STEP] Grader evaluated {task_id}. Score: {score}")
    return score