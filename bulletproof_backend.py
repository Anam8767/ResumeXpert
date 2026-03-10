from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health')
def health():
    return jsonify({"status": "Ok"})

@app.route('/simple-analyzer/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    try:
        # Get uploaded file
        if 'files' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['files']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Read file content (simplified)
        content = file.read().decode('utf-8', errors='ignore')
        
        # Simple analysis (mock data for now)
        return jsonify({
            "success": True,
            "filename": file.filename,
            "score": 85,
            "skills": ["JavaScript", "React", "Node.js", "Python"],
            "job_roles": [
                {"title": "Frontend Developer", "salary_range": "₹8-12 LPA"},
                {"title": "Full Stack Developer", "salary_range": "₹12-18 LPA"}
            ],
            "suggestions": [
                "Add more projects to showcase your skills",
                "Include specific achievements with numbers",
                "Add certifications to stand out"
            ],
            "strengths": ["Good technical foundation", "Relevant skills"],
            "weaknesses": ["Needs more project details"],
            "experience": "2+ years",
            "education": "Bachelor's Degree"
        })
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting HireLens Backend Server...")
    print("📍 Backend will run on: http://localhost:8000")
    print("🔗 Health check: http://localhost:8000/health")
    print("✅ Server ready!")
    
    app.run(host='0.0.0.0', port=8000, debug=True)
