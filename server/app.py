import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# The dot indicates it's in the same folder (server/)
from .inference import clean_data

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online", "mode": "multi-mode-ready"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(request: Request):
    try:
        payload = await request.json()
        records = payload.get("records", []) if isinstance(payload, dict) else payload
        
        if not isinstance(records, list):
            records = [records]

        # Use the imported function
        cleaned_records = [clean_data(str(item)) for item in records]

        return {
            "status": "success",
            "data": cleaned_records
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def main():
    # Points to this file and the FastAPI instance 'app'
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    main()
