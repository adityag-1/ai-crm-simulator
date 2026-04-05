from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from inference import clean_data
import uvicorn
import asyncio

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "project": "CRM Spec Compliance", "round": 1}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/reset")
async def reset_simulator():
    return {"status": "success", "message": "Simulator reset"}

@app.post("/process")
async def process_data(request: Request):
    try:
        # 1. The validator sends a JSON object, usually with a key like 'records'
        payload = await request.json()
        
        # Determine if input is a list or a single object
        records = payload.get("records", []) if isinstance(payload, dict) else payload
        
        if not isinstance(records, list):
            records = [records]

        # 2. Process each record through the inference logic
        # We use a loop to clean each item
        cleaned_records = []
        for item in records:
            # If item is a dict, convert to string for the LLM
            input_text = str(item)
            cleaned_text = clean_data(input_text)
            cleaned_records.append(cleaned_text)

        # 3. Return the exact structure 'openenv validate' expects
        return {
            "status": "success",
            "data": cleaned_records
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
