import uvicorn
from fastapi import FastAPI, Request
from inference import clean_data

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/reset")
async def reset():
    return {"status": "success"}

@app.post("/process")
async def process(request: Request):
    # Your processing logic
    return {"status": "success", "data": []}

def main():
    # This matches the 'server' script in pyproject.toml
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
