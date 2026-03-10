from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Form
from services.resume_analyzer import DynamicResumeAnalyzer
import json
import os
from datetime import datetime

router = APIRouter()

@router.post("/simple-analyze")
async def simple_analyze(files: list[UploadFile] = File(...)):
    """Simple resume analysis without external APIs"""
    try:
        results = []
        
        for file in files:
            # Read file content
            content = await file.read()
            text = ""
            
            if file.filename.endswith('.pdf'):
                try:
                    import PyPDF2
                    import io
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                except Exception as e:
                    return {"error": f"Error reading PDF: {str(e)}"}
            elif file.filename.endswith('.txt'):
                text = content.decode('utf-8')
            else:
                return {"error": "Only PDF and TXT files supported"}
            
            # Analyze with our dynamic analyzer
            analysis = DynamicResumeAnalyzer.analyze_resume_completely(text, file.filename)
            
            results.append({
                "filename": file.filename,
                "score": analysis['score'],
                "skills": analysis['skills'],
                "job_roles": analysis['job_roles'],
                "suggestions": analysis['suggestions'],
                "strengths": analysis['strengths'],
                "weaknesses": analysis['weaknesses']
            })
        
        return {
            "success": True,
            "message": f"Analyzed {len(files)} resume(s)",
            "results": results
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

@router.post("/upload-and-analyze")
async def upload_and_analyze(files: list[UploadFile] = File(...)):
    """Upload and automatically analyze resumes"""
    try:
        if not files:
            return {"error": "No files uploaded"}
        
        # Analyze first file
        file = files[0]
        content = await file.read()
        text = ""
        
        if file.filename.endswith('.pdf'):
            try:
                import PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception as e:
                return {"error": f"Error reading PDF: {str(e)}"}
        elif file.filename.endswith('.txt'):
            text = content.decode('utf-8')
        else:
            return {"error": "Only PDF and TXT files supported"}
        
        # Analyze with our dynamic analyzer
        analysis = DynamicResumeAnalyzer.analyze_resume_completely(text, file.filename)
        
        return {
            "success": True,
            "filename": file.filename,
            "score": analysis['score'],
            "skills": analysis['skills'],
            "job_roles": analysis['job_roles'],
            "suggestions": analysis['suggestions'],
            "strengths": analysis['strengths'],
            "weaknesses": analysis['weaknesses'],
            "experience": analysis['experience'],
            "education": analysis['education'],
            "message": "Resume analyzed successfully!"
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
