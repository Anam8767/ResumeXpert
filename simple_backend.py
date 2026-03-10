from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.simple_analyzer import router as simple_router
import uvicorn

app = FastAPI(title="HireLens Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(simple_router, prefix="/simple-analyzer", tags=["SimpleAnalyzer"])

@app.get("/health")
async def health():
    return {"status": "Ok"}

@app.get("/")
async def root():
    return {"message": "HireLens Backend Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
