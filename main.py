import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from inference import run_inference
from grader import calculate_reward

app = FastAPI(title="CRM Data Cleaner - Round 1")

# --- Data Models ---
class TaskRequest(BaseModel):
    task_id: str
    prompt: str

# --- API Endpoints (For HF Spaces/UI) ---

@app.get("/")
def read_root():
    return {"status": "online", "project": "CRM Spec Compliance", "round": 1}

@app.post("/process")
def process_task(request: TaskRequest):
    """
    Endpoint that triggers inference and returns the result + a preliminary score.
    """
    # 1. Execute Inference (Structured tags are printed to stdout)
    result = run_inference(request.prompt)
    
    if not result:
        raise HTTPException(status_code=500, detail="Inference failed to generate output.")

    # 2. Evaluate Performance
    score = calculate_reward(request.task_id, result)
    
    return {
        "task_id": request.task_id,
        "model_output": result,
        "score": score
    }

# --- Standalone Execution (For openenv validator) ---

def run_standalone():
    """
    Allows the validator to run the script directly via 'python main.py'
    using environment variables for configuration.
    """
    print("[STEP] Running in Standalone Mode")
    
    # These are usually injected by the openenv platform
    task_id = os.getenv("TASK_ID", "task_easy")
    sample_prompt = os.getenv("TASK_PROMPT", "Clean record: mArY sMiTh, mary.s@gmial.com")
    
    output = run_inference(sample_prompt)
    if output:
        score = calculate_reward(task_id, output)
        print(f"--- FINAL SUMMARY ---")
        print(f"Task: {task_id}")
        print(f"Score: {score}")

if __name__ == "__main__":
    # If the environment variable 'MODE' is set to 'SERVER', start FastAPI
    # Otherwise, run a standalone validation pass.
    if os.getenv("RUN_MODE") == "SERVER":
        port = int(os.getenv("PORT", 7860))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        run_standalone()