import re
import json
from datetime import datetime

class DynamicResumeAnalyzer:
    """Truly dynamic resume analyzer - NO TEMPLATES"""
    
    @staticmethod
    def analyze_resume_completely(text: str, filename: str) -> dict:
        """Complete dynamic analysis"""
        
        # Extract EVERYTHING dynamically
        analysis = {
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'skills': DynamicResumeAnalyzer.extract_skills_unique(text),
            'experience': DynamicResumeAnalyzer.extract_experience_info(text),
            'education': DynamicResumeAnalyzer.extract_education_info(text),
            'projects': DynamicResumeAnalyzer.extract_projects_info(text),
            'strengths': DynamicResumeAnalyzer.identify_strengths(text),
            'weaknesses': DynamicResumeAnalyzer.identify_weaknesses(text),
            'suggestions': DynamicResumeAnalyzer.generate_suggestions(text),
            'unique_factors': DynamicResumeAnalyzer.find_unique_factors(text),
            'score': DynamicResumeAnalyzer.calculate_dynamic_score(text),
            'job_roles': DynamicResumeAnalyzer.suggest_job_roles(text)
        }
        
        return analysis
    
    @staticmethod
    def extract_skills_unique(text: str) -> list:
        """Find skills that are ACTUALLY in this resume"""
        skills_found = []
        text_lower = text.lower()
        
        # Comprehensive tech skills database
        tech_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'perl', 'r', 'matlab',
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'nestjs', 'laravel', 'rails', 'next.js', 'gatsby',
            # Databases
            'mysql', 'mongodb', 'postgresql', 'redis', 'sqlite', 'oracle', 'elasticsearch', 'cassandra', 'dynamodb', 'firebase',
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git', 'github', 'gitlab', 'ci/cd', 'ansible', 'puppet',
            # Data Science & AI
            'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'machine learning', 'deep learning', 'nlp', 'opencv', 'spark', 'hadoop',
            # Mobile
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'cordova',
            # Testing
            'jest', 'mocha', 'pytest', 'selenium', 'cypress', 'junit', 'testng',
            # Other Tools
            'jira', 'confluence', 'linux', 'bash', 'shell', 'excel', 'powerpoint', 'word', 'figma', 'sketch', 'postman', 'swagger'
        ]
        
        for skill in tech_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                skills_found.append(skill.title())
        
        return list(set(skills_found))
    
    @staticmethod
    def calculate_dynamic_score(text: str) -> int:
        """Calculate unique score based on actual content"""
        score = 0
        text_lower = text.lower()
        
        # Skills variety (max 25 points)
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        skill_score = min(len(skills) * 2, 25)
        score += skill_score
        
        # Experience depth (max 25 points)
        exp_patterns = [
            r'(\d+)[\+]?\s*(years?|yrs?)\s+experience',
            r'(\d+)\s*\+?\s*years'
        ]
        exp_found = False
        for pattern in exp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                years = int(match.group(1))
                exp_score = min(years * 3, 25)
                score += exp_score
                exp_found = True
                break
        if not exp_found:
            score += 5  # Basic points for having experience section
        
        # Projects quality (max 25 points)
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented', 'designed']
        project_count = sum(text_lower.count(keyword) for keyword in project_keywords)
        project_score = min(project_count * 3, 25)
        score += project_score
        
        # Resume structure (max 25 points)
        structure_elements = ['education', 'experience', 'skills', 'contact', 'email', 'phone']
        structure_count = sum(1 for element in structure_elements if element in text_lower)
        structure_score = min(structure_count * 5, 25)
        score += structure_score
        
        return min(score, 100)
    
    @staticmethod
    def suggest_job_roles(text: str) -> list:
        """Suggest job roles based on ACTUAL skills in resume"""
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        text_lower = text.lower()
        job_roles = []
        
        # Map skills to job roles with detailed descriptions
        if any(skill in ['Python', 'Django', 'Flask', 'Pandas', 'Numpy', 'Tensorflow', 'Pytorch'] for skill in skills):
            if 'machine learning' in text_lower or 'tensorflow' in skills or 'pytorch' in skills:
                job_roles.append({
                    "title": "Machine Learning Engineer",
                    "description": f"Design and implement ML models using {', '.join([s for s in skills if s in ['Python', 'Tensorflow', 'Pytorch', 'Pandas', 'Numpy', 'Scikit-learn']][:3])}",
                    "responsibilities": [
                        "Develop machine learning models and algorithms",
                        "Process and analyze large datasets",
                        "Collaborate with data science team",
                        "Optimize model performance"
                    ],
                    "salary_range": "₹8-15 LPA",
                    "experience_level": "Mid-Senior Level"
                })
            job_roles.append({
                "title": "Python Developer", 
                "description": f"Build applications using {', '.join([s for s in skills if s in ['Python', 'Django', 'Flask', 'FastAPI']][:2])}",
                "responsibilities": [
                    "Develop backend applications",
                    "Write clean and efficient Python code",
                    "Integrate databases and APIs",
                    "Test and debug applications"
                ],
                "salary_range": "₹6-12 LPA",
                "experience_level": "Mid Level"
            })
        
        if any(skill in ['React', 'Angular', 'Vue', 'Javascript', 'Typescript'] for skill in skills):
            if 'node.js' in skills:
                job_roles.append({
                    "title": "Full Stack Developer",
                    "description": f"End-to-end development using {', '.join([s for s in skills if s in ['React', 'Node.js', 'Javascript', 'Typescript', 'MongoDB']][:3])}",
                    "responsibilities": [
                        "Develop both frontend and backend",
                        "Design responsive user interfaces",
                        "Build RESTful APIs",
                        "Database design and management"
                    ],
                    "salary_range": "₹8-18 LPA",
                    "experience_level": "Mid-Senior Level"
                })
            else:
                job_roles.append({
                    "title": "Frontend Developer",
                    "description": f"Create user interfaces with {', '.join([s for s in skills if s in ['React', 'Angular', 'Vue', 'Javascript', 'Typescript']][:2])}",
                    "responsibilities": [
                        "Build responsive web applications",
                        "Implement pixel-perfect designs",
                        "Optimize application performance",
                        "Collaborate with UX team"
                    ],
                    "salary_range": "₹5-12 LPA",
                    "experience_level": "Entry-Mid Level"
                })
        
        if any(skill in ['AWS', 'Docker', 'Kubernetes', 'Terraform', 'Azure', 'GCP'] for skill in skills):
            job_roles.append({
                "title": "DevOps Engineer",
                "description": f"Manage cloud infrastructure using {', '.join([s for s in skills if s in ['AWS', 'Docker', 'Kubernetes', 'Terraform']][:2])}",
                "responsibilities": [
                    "Deploy and manage applications",
                    "Set up CI/CD pipelines",
                    "Monitor system performance",
                    "Ensure security and scalability"
                ],
                "salary_range": "₹10-20 LPA",
                "experience_level": "Mid-Senior Level"
            })
        
        if any(skill in ['Android', 'Flutter', 'React Native', 'Swift', 'Kotlin'] for skill in skills):
            job_roles.append({
                "title": "Mobile App Developer",
                "description": f"Develop mobile applications using {', '.join([s for s in skills if s in ['Android', 'Flutter', 'React Native']][:2])}",
                "responsibilities": [
                    "Design and build mobile apps",
                    "Ensure app performance and quality",
                    "Integrate APIs and backend services",
                    "Publish and maintain apps"
                ],
                "salary_range": "₹6-15 LPA",
                "experience_level": "Mid Level"
            })
        
        if any(skill in ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle'] for skill in skills):
            if len(skills) > 5:  # Has database + other skills
                job_roles.append({
                    "title": "Backend Developer",
                    "description": f"Build server-side applications with {', '.join([s for s in skills if s in ['Node.js', 'Python', 'Java', 'MySQL', 'PostgreSQL', 'MongoDB']][:3])}",
                    "responsibilities": [
                        "Develop server-side logic",
                        "Design and manage databases",
                        "Build and consume APIs",
                        "Ensure application security"
                    ],
                    "salary_range": "₹7-14 LPA",
                    "experience_level": "Mid Level"
                })
        
        # Entry level detection
        if 'fresher' in text_lower or 'intern' in text_lower or 'entry level' in text_lower:
            job_roles = [
                {
                    "title": f"Junior {role['title']}" if isinstance(role, dict) else f"Junior {role}",
                    "description": f"Entry-level position for beginners",
                    "responsibilities": ["Learn and assist senior developers", "Basic coding tasks", "Testing and debugging"],
                    "salary_range": "₹3-6 LPA",
                    "experience_level": "Entry Level"
                } for role in job_roles[:2]
            ]
        
        return job_roles[:3] if job_roles else [{
            "title": "General Software Developer",
            "description": "Software development role based on your skills",
            "responsibilities": ["Develop software applications", "Code testing and debugging", "Collaborate with team"],
            "salary_range": "₹4-8 LPA",
            "experience_level": "Entry Level"
        }]
    
    @staticmethod
    def generate_suggestions(text: str) -> list:
        """Generate UNIQUE suggestions for THIS resume"""
        suggestions = []
        text_lower = text.lower()
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        
        # Score-based suggestions
        score = DynamicResumeAnalyzer.calculate_dynamic_score(text)
        if score < 40:
            suggestions.append("🔴 Your resume needs major improvements. Add more skills, experience details, and projects.")
        elif score < 60:
            suggestions.append("🟡 Good start! Add specific achievements and quantify your results.")
        elif score < 80:
            suggestions.append("🟢 Strong resume! Highlight leadership experience and advanced skills.")
        
        # Skills quantity suggestions
        if len(skills) < 3:
            suggestions.append("📚 List at least 5-7 technical skills relevant to your target role.")
        elif len(skills) < 8:
            suggestions.append("💪 Good skills! Add 2-3 more advanced or specialized technologies.")
        elif len(skills) < 15:
            suggestions.append("🚀 Excellent skills variety! Consider adding cloud or DevOps technologies.")
        
        # Experience section analysis
        if not re.search(r'\bexperience\b|\bwork\b|\bjob\b|\bcareer\b', text_lower):
            suggestions.append("💼 Add detailed work experience section with specific roles and achievements.")
        else:
            # Check if experience has metrics
            if not re.search(r'\d+%|\d+years|\$\d+|\d+x|\d+million|\d+thousand', text_lower):
                suggestions.append("📊 Quantify your achievements with numbers (e.g., 'Improved performance by 30%').")
        
        # Projects section analysis
        if not re.search(r'\bproject\b|\bportfolio\b|\bbuilt\b|\bdeveloped\b|\bcreated\b', text_lower):
            suggestions.append("🚀 Include 2-3 specific projects with technologies used and outcomes.")
        else:
            # Check if projects have details
            if not re.search(r'\bgithub\b|\bgitlab\b|\blive\b|\bdeploy\b|\bproduction\b', text_lower):
                suggestions.append("🔗 Add project links (GitHub) and mention live deployments if available.")
        
        # Education details
        if not re.search(r'\beducation\b|\bdegree\b|\buniversity\b|\bcollege\b', text_lower):
            suggestions.append("🎓 Add education details with degree, institution, and graduation year.")
        
        # Contact information
        if not re.search(r'\bemail\b|\bphone\b|\bcontact\b|\blinkedin\b', text_lower):
            suggestions.append("📞 Add complete contact information including LinkedIn profile.")
        
        # Technical skills gaps based on current skills
        if any(skill in ['Python', 'Java', 'Javascript'] for skill in skills):
            if not any(skill in ['AWS', 'Azure', 'GCP'] for skill in skills):
                suggestions.append("☁️ Add cloud platform skills (AWS/Azure/GCP) for better job opportunities.")
        
        if any(skill in ['React', 'Angular', 'Vue'] for skill in skills):
            if not any(skill in ['Node.js', 'Express', 'Django', 'Flask'] for skill in skills):
                suggestions.append("🔧 Consider adding backend skills (Node.js/Django) for full-stack opportunities.")
        
        if len(skills) > 5 and not any(skill in ['Docker', 'Kubernetes', 'Jenkins'] for skill in skills):
            suggestions.append("🐳 Add DevOps skills (Docker/Kubernetes) to increase your market value.")
        
        # Soft skills indicators
        if not re.search(r'\blead\b|\bteam\b|\bmanage\b|\bcommunicat\b|\bpresent\b', text_lower):
            suggestions.append("👥 Highlight leadership, teamwork, and communication experiences.")
        
        # Certifications and achievements
        if not re.search(r'\bcertifi\b|\baward\b|\bachieve\b|\brecognition\b', text_lower):
            suggestions.append("🏆 Add certifications, awards, or notable achievements to stand out.")
        
        # Resume formatting and structure
        if len(text) < 500:
            suggestions.append("📝 Your resume seems too short. Add more details about your experience and projects.")
        elif len(text) > 3000:
            suggestions.append("✂️ Consider condensing your resume to 1-2 pages for better readability.")
        
        # Action verbs
        if not re.search(r'\b(developed|implemented|led|created|built|designed|managed|achieved|improved|optimized)\b', text_lower):
            suggestions.append("⚡ Use strong action verbs like 'Developed', 'Implemented', 'Led' instead of passive language.")
        
        return suggestions[:8]  # Return top 8 most relevant suggestions
    
    @staticmethod
    def extract_experience_info(text: str) -> str:
        """Extract experience information"""
        patterns = [
            r'(\d+)[\+]?\s*(years?|yrs?)\s+experience',
            r'experience\s+of\s+(\d+)\s*(years?|yrs?)',
            r'(\d+)\s*(years?|yrs?)\s+in\s+',
            r'(\d+)[\+]?\s*(years?|yrs?)\s+of\s+experience',
            r'(\d+)\s*\+?\s*years',
            r'(\d+)\s*-\s*(\d+)\s*years',
            r'over\s+(\d+)\s*years'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years = match.group(1)
                return f"{years} years of experience"
        
        # Check for entry-level/fresher keywords
        if re.search(r'\bfresher\b|\bentry\s*level\b|\bintern\b|\btrainee\b', text, re.IGNORECASE):
            return "Entry-level/Fresher"
        
        return "Experience not specified"
    
    @staticmethod
    def extract_education_info(text: str) -> list:
        """Extract education information"""
        education_patterns = [
            r'(bachelor|master|phd|b\.tech|m\.tech|b\.sc|m\.sc|b\.a|m\.a|b\.e|m\.e)',
            r'(university|college|institute)',
            r'(computer science|information technology|engineering|science|arts|commerce)'
        ]
        
        education_found = []
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education_found.extend(matches)
        
        return list(set(education_found))
    
    @staticmethod
    def extract_projects_info(text: str) -> list:
        """Extract project information"""
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented', 'designed']
        projects = []
        
        for keyword in project_keywords:
            matches = re.findall(rf'{keyword}[^.]*', text, re.IGNORECASE)
            projects.extend(matches[:2])  # Limit to avoid too much text
        
        return projects[:3]  # Return top 3 project mentions
    
    @staticmethod
    def identify_strengths(text: str) -> list:
        """Identify strengths from the resume"""
        strengths = []
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        
        if len(skills) > 8:
            strengths.append("Strong technical skill diversity")
        
        if re.search(r'\blead\b|\bteam\b|\bmanage\b', text, re.IGNORECASE):
            strengths.append("Leadership and teamwork experience")
        
        if re.search(r'\bproject\b.*\bdeploy\b|\blive\b|\bproduction\b', text, re.IGNORECASE):
            strengths.append("Real-world project deployment experience")
        
        if len(DynamicResumeAnalyzer.extract_projects_info(text)) > 2:
            strengths.append("Multiple project experience")
        
        return strengths
    
    @staticmethod
    def identify_weaknesses(text: str) -> list:
        """Identify weaknesses or gaps"""
        weaknesses = []
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        
        if len(skills) < 3:
            weaknesses.append("Limited technical skills mentioned")
        
        if not re.search(r'\bexperience\b|\bwork\b|\bjob\b', text, re.IGNORECASE):
            weaknesses.append("No work experience section")
        
        if not re.search(r'\beducation\b|\bdegree\b', text, re.IGNORECASE):
            weaknesses.append("Education details missing")
        
        if not re.search(r'\bemail\b|\bphone\b|\bcontact\b', text, re.IGNORECASE):
            weaknesses.append("Contact information incomplete")
        
        return weaknesses
    
    @staticmethod
    def find_unique_factors(text: str) -> list:
        """Find unique factors in this resume"""
        unique = []
        text_lower = text.lower()
        
        # Check for unique combinations
        skills = DynamicResumeAnalyzer.extract_skills_unique(text)
        
        if any(skill in ['tensorflow', 'pytorch', 'machine learning'] for skill in skills):
            unique.append("AI/ML expertise")
        
        if any(skill in ['aws', 'azure', 'gcp'] for skill in skills) and len(skills) > 5:
            unique.append("Cloud architecture skills")
        
        if re.search(r'\bopen\s*source\b|\bcontribut\b', text_lower):
            unique.append("Open source contributions")
        
        if re.search(r'\bpublished\b|\bresearch\b|\bpaper\b', text_lower):
            unique.append("Research or publications")
        
        return unique
