import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
# Import from the root-level module that was installed
import inference 

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(request: Request):
    try:
        payload = await request.json()
        records = payload.get("records", [])
        
        # Call the function from inference.py
        cleaned_records = [inference.clean_data(str(item)) for item in records]

        return {"status": "success", "data": cleaned_records}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
