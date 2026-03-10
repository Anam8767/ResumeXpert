from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
import re
import json
import os
import pypdf
from datetime import datetime

def extract_skills_dynamically(text: str) -> list:
    """Extract skills DYNAMICALLY from resume text."""
    text_lower = text.lower()
    
    skills_patterns = {
        'Programming': [
            r'\bpython\b', r'\bjava\b', r'\bjavascript\b', r'\btypescript\b', 
            r'\bc\+\+\b', r'\bc#\b', r'\bphp\b', r'\bruby\b', r'\bgo\b', r'\brust\b',
            r'\bswift\b', r'\bkotlin\b', r'\bdart\b', r'\bscala\b', r'\bperl\b'
        ],
        'Web': [
            r'\bhtml\b', r'\bcss\b', r'\breact\b', r'\bangular\b', r'\bvue\b',
            r'\bnext\.js\b', r'\bdjango\b', r'\bflask\b', r'\bexpress\b', r'\bnode\.js\b',
            r'\bspring\b', r'\bnest\.js\b', r'\blaravel\b', r'\bsymfony\b'
        ],
        'Database': [
            r'\bmysql\b', r'\bmongodb\b', r'\bpostgresql\b', r'\bsqlite\b',
            r'\boracle\b', r'\bredis\b', r'\belasticsearch\b', r'\bdynamodb\b',
            r'\bcassandra\b', r'\bmariadb\b'
        ],
        'Cloud/DevOps': [
            r'\baws\b', r'\bazure\b', r'\bgcp\b', r'\bdocker\b', r'\bkubernetes\b',
            r'\bterraform\b', r'\bjenkins\b', r'\bci/cd\b', r'\bgithub actions\b',
            r'\bansible\b', r'\bprometheus\b', r'\bgrafana\b'
        ],
        'Tools': [
            r'\bgit\b', r'\bgithub\b', r'\bgitlab\b', r'\bjira\b', r'\bconfluence\b',
            r'\blinux\b', r'\bbash\b', r'\bshell\b', r'\bpostman\b', r'\bdocker\b',
            r'\bkubernetes\b', r'\bfigma\b', r'\badobe\b'
        ],
        'Data Science': [
            r'\bpandas\b', r'\bnumpy\b', r'\btensorflow\b', r'\bpytorch\b',
            r'\bscikit-learn\b', r'\bmachine learning\b', r'\bdeep learning\b',
            r'\bnlp\b', r'\bopencv\b', r'\bmatplotlib\b', r'\bseaborn\b'
        ],
        'Mobile': [
            r'\bandroid\b', r'\bios\b', r'\breact native\b', r'\bflutter\b',
            r'\bxcode\b', r'\bandroid studio\b', r'\bkotlin\b', r'\bswift\b'
        ]
    }
    
    found_skills = []
    
    for category, patterns in skills_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    skill = text[match.start():match.end()].strip()
                    if skill and skill not in found_skills:
                        found_skills.append(skill.title())
    
    caps_matches = re.findall(r'\b[A-Z]{2,}\b', text)
    for match in caps_matches:
        if match not in found_skills and len(match) > 2:
            found_skills.append(match)
    
    tool_patterns = [
        r'\b(?:MS\s*)?Office\b', r'\bExcel\b', r'\bWord\b', r'\bPowerPoint\b',
        r'\bPhotoshop\b', r'\bIllustrator\b', r'\bFigma\b', r'\bSketch\b',
        r'\bTableau\b', r'\bPower\s*BI\b', r'\bJupyter\b'
    ]
    
    for pattern in tool_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match and match not in found_skills:
                    found_skills.append(match.strip().title())
    
    return list(set(found_skills))

def extract_experience_dynamically(text: str) -> str:
    """Extract experience information dynamically"""
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
    
    if re.search(r'\bfresher\b|\bentry\s*level\b|\bintern\b|\btrainee\b', text, re.IGNORECASE):
        return "Entry-level/Fresher"
    
    return "Experience not specified"

def parse_pdf(file_path: str) -> list:
    """Parse PDF and extract UNIQUE content for each resume"""
    loader = PyMuPDFLoader(file_path)
    documents = loader.load() 
    file_name = re.search(r'[^/]+$', file_path).group(0)
    
    all_text = ""
    for doc in documents:
        all_text += doc.page_content + " "
    
    skills = extract_skills_dynamically(all_text)
    experience = extract_experience_dynamically(all_text)
    
    has_projects = bool(re.search(r'\bproject\b|\bwork\b|\bexperience\b', all_text, re.IGNORECASE))
    has_education = bool(re.search(r'\beducation\b|\bdegree\b|\bb\.\s*tech\b|\bb\.\s*e\.\b|\bm\.\s*tech\b', all_text, re.IGNORECASE))
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100, separators=["\n", " ", ""])
    docs = text_splitter.split_documents(documents) 
    
    for idx, doc in enumerate(docs):
        docs[idx].metadata['name'] = file_name
        docs[idx].metadata['type'] = 'pdf'
        docs[idx].metadata['extracted_skills'] = skills
        docs[idx].metadata['extracted_experience'] = experience
        docs[idx].metadata['has_projects'] = has_projects
        docs[idx].metadata['has_education'] = has_education
        docs[idx].metadata['total_skills_found'] = len(skills)
        docs[idx].metadata['resume_unique_id'] = hash(file_name + str(len(all_text)))
    
    analysis_file = file_path.replace('.pdf', '_analysis.json')
    with open(analysis_file, 'w') as f:
        json.dump({
            'file_name': file_name,
            'skills_found': skills,
            'experience': experience,
            'has_projects': has_projects,
            'has_education': has_education,
            'total_skills': len(skills),
            'content_length': len(all_text),
            'analysis_timestamp': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"✓ DYNAMIC analysis: Found {len(skills)} unique skills in {file_name}")
    return docs

def parse_text(file_path: str) -> list:
    """Parse text resume"""
    with open(file_path, 'r', encoding='utf-8') as file_data:
        file_content = file_data.read()
    
    file_name = os.path.basename(file_path)
    
    skills = extract_skills_dynamically(file_content)
    experience = extract_experience_dynamically(file_content)
    has_projects = bool(re.search(r'\bproject\b|\bwork\b|\bexperience\b', file_content, re.IGNORECASE))
    has_education = bool(re.search(r'\beducation\b|\bdegree\b', file_content, re.IGNORECASE))
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        length_function=len
    )
    docs = text_splitter.create_documents([file_content]) 
    
    for idx, doc in enumerate(docs):
        docs[idx].metadata['name'] = file_name
        docs[idx].metadata['type'] = 'txt'
        docs[idx].metadata['extracted_skills'] = skills
        docs[idx].metadata['extracted_experience'] = experience
        docs[idx].metadata['has_projects'] = has_projects
        docs[idx].metadata['has_education'] = has_education
        docs[idx].metadata['total_skills_found'] = len(skills)
        docs[idx].metadata['resume_unique_id'] = hash(file_name + str(len(file_content)))
    
    analysis_file = file_path.replace('.txt', '_analysis.json')
    with open(analysis_file, 'w') as f:
        json.dump({
            'file_name': file_name,
            'skills_found': skills,
            'experience': experience,
            'total_skills': len(skills),
            'content_info': {
                'has_projects': has_projects,
                'has_education': has_education,
                'length': len(file_content)
            }
        }, f, indent=2)
    
    print(f"✓ DYNAMIC analysis: Found {len(skills)} unique skills in {file_name}")
    return docs
