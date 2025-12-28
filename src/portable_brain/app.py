from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# main app, asgi entrypoint
app = FastAPI()

# test endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}
