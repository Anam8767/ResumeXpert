from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "Ok"}

@app.post("/simple-analyzer/upload-and-analyze")
async def upload_and_analyze(files: list = []):
    return {
        "success": True,
        "filename": "test.pdf",
        "score": 85,
        "skills": ["JavaScript", "React", "Node.js"],
        "job_roles": [{"title": "Frontend Developer", "salary_range": "₹8-12 LPA"}],
        "suggestions": ["Add more projects", "Include certifications"],
        "strengths": ["Good technical skills"],
        "weaknesses": ["Needs more experience"],
        "experience": "2 years",
        "education": "B.Tech"
    }

if __name__ == "__main__":
    print("🚀 Starting HireLens Backend...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
