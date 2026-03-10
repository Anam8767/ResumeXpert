# import os
# from config import constants
# from utils.backgroud_exeption import handleExceptions
# from utils.processor import parse_pdf,parse_text
# from dotenv import load_dotenv
# from pinecone import Pinecone
# load_dotenv()
# from langchain_pinecone import  PineconeVectorStore
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate 
# from langchain_mistralai import ChatMistralAI,MistralAIEmbeddings
 

# embed_model = MistralAIEmbeddings(
#     model=os.getenv('MISTRAL_EMBED_MODEL'), 
#     api_key=os.getenv('MISTRAL_API_KEY'),
    
# )

# llm = ChatMistralAI(
#             mistral_api_key=os.getenv('MISTRAL_API_KEY'),
#             model=os.getenv('MISTRAL_MODEL'),
#             temperature=0, 
#              )

# pc=Pinecone(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENV'))

# class PineconeService:  
    
#     # @handleExceptions
#     # async def vectorize_documents_main(self, namespace_id: str):
#     #     import traceback
#     #     print("=" * 70)
#     #     print(f"[INFO] Starting vectorization for namespace: {namespace_id}")
#     #     in_process_dir: str = os.path.join(constants.UPLOAD_DIR, namespace_id, constants.PRIMARY_FOLDER)
#     #     print(f"[INFO] Upload folder path: {in_process_dir}")

#     #     if not os.path.exists(in_process_dir):
#     #         print(f"[ERROR] Directory not found: {in_process_dir}")
#     #         return {"error": "Upload directory not found"}

#     #     documents = {namespace_id: []}
        
#     #     for file in os.listdir(in_process_dir):
#     #         file_path: str = os.path.join(in_process_dir, file)
#     #         if os.path.isdir(file_path):
#     #             print(f"[SKIP] Skipping subdirectory: {file}")
#     #             continue

#     #         file_ext = file.split('.')[-1].lower()
#     #         print(f"[INFO] Processing file: {file} (type: {file_ext})")

#     #         try:
#     #             if file_ext == 'txt':
#     #                 docs = parse_text(file_path)
#     #             elif file_ext == 'pdf':
#     #                 docs = parse_pdf(file_path)
#     #             else:
#     #                 print(f"[WARN] Unsupported file type: {file_ext}. Skipping.")
#     #                 continue

#     #             print(f"[DEBUG] Parsed {len(docs)} text chunks from {file}")
#     #             documents[namespace_id].extend(docs)

#     #             os.remove(file_path)
#     #             print(f"[INFO] Removed file after processing: {file_path}")

#     #         except Exception as e:
#     #             print(f"[ERROR] Failed to parse {file}: {str(e)}")
#     #             traceback.print_exc()

#     #     if not documents[namespace_id]:
#     #         print("[WARN] No text extracted from any document. Nothing to embed.")
#     #         return {"message": "No valid text found in uploaded documents."}

#     #     try:
#     #         test_vector = embed_model.embed_query("hello world")
#     #         print(f"[DEBUG] Embedding model test successful. Vector dimension = {len(test_vector)}")
#     #     except Exception as e:
#     #         print(f"[ERROR] Embedding model failed: {e}")
#     #         traceback.print_exc()
#     #         return {"error": "Embedding model not working properly"}

#     #     try:
#     #         index_name = os.getenv('PINECONE_INDEX')
#     #         print(f"[INFO] Checking Pinecone index: {index_name}")
#     #         existing_indexes = [idx.name for idx in pc.list_indexes()]
#     #         print(f"[DEBUG] Existing indexes: {existing_indexes}")
#     #         if index_name not in existing_indexes:
#     #             print(f"[WARN] Index '{index_name}' not found. Creating new index...")
#     #             pc.create_index(name=index_name, dimension=len(test_vector), metric="cosine")
#     #     except Exception as e:
#     #         print(f"[ERROR] Failed to connect or create Pinecone index: {e}")
#     #         traceback.print_exc()
#     #         return {"error": "Pinecone index connection failed"}
#     #     try:
#     #         print(f"[INFO] Uploading embeddings to Pinecone namespace: {namespace_id}")
#     #         vectorstore = PineconeVectorStore.from_documents(
#     #             documents[namespace_id],
#     #             index_name=index_name,
#     #             embedding=embed_model,
#     #             namespace=namespace_id
#     #         )
#     #         print("[SUCCESS] Embeddings uploaded successfully to Pinecone!")
#     #     except Exception as e:
#     #         print(f"[ERROR] Pinecone upload failed: {e}")
#     #         traceback.print_exc()
#     #         return {"error": "Failed to upload vectors to Pinecone"}
#     #     try:
#     #         index = pc.Index(index_name)
#     #         stats = index.describe_index_stats()
#     #         count = stats.get("namespaces", {}).get(namespace_id, {}).get("vector_count", 0)
#     #         print(f"[INFO] Namespace '{namespace_id}' now contains {count} vectors in Pinecone.")
#     #     except Exception as e:
#     #         print(f"[WARN] Could not fetch Pinecone stats: {e}")

#     #     print("=" * 70)
#     #     return {"message": "File uploaded and embedded successfully!"}
    
#     async def vectorize_documents_main(self, namespace_id: str):
#         in_process_dir = os.path.join(
#             constants.UPLOAD_DIR,
#             namespace_id,
#             constants.PRIMARY_FOLDER
#         )

#         all_documents = []

#         for file in os.listdir(in_process_dir):
#             file_path = os.path.join(in_process_dir, file)

#             if os.path.isdir(file_path):
#                 continue

#             file_ext = file.split(".")[-1].lower()

#             if file_ext == "txt":
#                 docs = parse_text(file_path)
#                 doc_type = "txt"
#             elif file_ext == "pdf":
#                 docs = parse_pdf(file_path)
#                 doc_type = "pdf"
#             else:
#                 continue

#             for doc in docs:
#                 doc.metadata = doc.metadata or {}
#                 doc.metadata["name"] = file                  
#                 doc.metadata["namespace_id"] = namespace_id  
#                 doc.metadata["type"] = doc_type

#             all_documents.extend(docs)

#             os.remove(file_path)

#         if not all_documents:
#             return {"message": "No documents to vectorize"}

#         PineconeVectorStore.from_documents(
#             documents=all_documents,
#             index_name=os.getenv("PINECONE_INDEX"),
#             embedding=embed_model,
#             namespace=namespace_id
#         )

#         return {"message": "Files vectorized successfully"}
    

#     @handleExceptions
#     async def delete_vectorized_docs(self, namespace_id: str, key: str, values: list[str]):
#         index = pc.Index(os.getenv('PINECONE_INDEX'))   
#         filter_condition = {key: {"$in": values}}
#         response = index.delete(delete_all=False, namespace=namespace_id, filter=filter_condition)
#         return response   
    
    

#     async def chain_resp(self,namespace_id: str,question: str, chatHistory: str):
       

# #         template = """
# # You are a Resume Analysis Assistant.

# # Your task is to answer the user's question strictly based on the provided resume content.

# # ========================
# # INPUT
# # ========================
# # Resume Content:
# # {fileContent}

# # Chat History:
# # {chatHistory}

# # User Question:
# # {question}

# # ========================
# # CRITICAL RULES (HIGHEST PRIORITY — DO NOT VIOLATE)
# # ========================

# # 1. GREETING HANDLING (STRICT):
# # - If the user's message is a greeting or casual message such as:
# #   "hi", "hii", "hello", "hey", "thanks", "how are you"
# # - AND the resume content is EMPTY, NULL, or NOT PROVIDED,
# #   THEN respond with ONLY the following sentence and NOTHING ELSE:

# #   "Hello 👋 Please upload your resume or ask me to analyze it."

# # - STOP immediately.
# # - Do NOT add explanations.
# # - Do NOT include any analysis, summary, skills, or scores.

# # 2. RESUME REQUIRED CHECK:
# # - If the user requests resume analysis but {fileContent} is missing,
# #   politely ask them to upload the resume before proceeding.

# # 3. RESUME ANALYSIS RULES:
# # - Perform analysis ONLY when valid resume content is provided.
# # - Base all responses strictly on the given resume.
# # - Do NOT assume, infer, or invent any skills, experience, or projects.

# # 4. RESUME ACCURACY SCORE:
# # - Provide an overall score between 0–100%.
# # - The score must be based on:
# #   - Resume structure
# #   - Clarity
# #   - Skills relevance
# #   - Projects
# #   - Job readiness
# # - Provide a brief justification.

# # 5. LANGUAGE RULE:
# # - Respond in the SAME language as the user's question.

# # ========================
# # OUTPUT FORMAT
# # (Use ONLY when resume content is provided)
# # ========================

# # Resume Summary:
# # (Write a concise 2–3 line professional summary based on the resume.)

# # Resume Accuracy Score:
# # Overall Score: XX%
# # Reason: (Short and clear justification.)

# # Good Skills Identified:
# # - Skill 1
# # - Skill 2
# # - Skill 3

# # Recommended Skills to Add:
# # - Skill 1 (reason)
# # - Skill 2 (reason)

# # Areas of Improvement:
# # - Area 1
# # - Area 2
# # - Area 3

# # Resume Improvement Suggestions:
# # - Suggestion 1
# # - Suggestion 2

# # Job Readiness Level:
# # Beginner / Intermediate / Job-Ready


# # IMPORTANT:
# # - Use clear line breaks between sections.
# # - Start each section on a new line.
# # - Use bullet points with hyphens (-).
# # - Do NOT merge headings and content.

# # """

#         template = """
# You are a Resume Analysis Assistant.

# Your task is to analyze the resume and answer the user's question strictly based on the provided resume content.

# ========================
# INPUT
# ========================
# Resume Content:
# {fileContent}

# Chat History:
# {chatHistory}

# User Question:
# {question}

# ========================
# CRITICAL RULES (HIGHEST PRIORITY — DO NOT VIOLATE)
# ========================

# 1. GREETING HANDLING (STRICT):
# - If the user's message is a greeting or casual message such as:
#   "hi", "hii", "hello", "hey", "thanks", "how are you"
# - AND the resume content is EMPTY, NULL, or NOT PROVIDED,
#   THEN respond with ONLY the following sentence and NOTHING ELSE:

#   "Hello 👋 Please upload your resume or ask me to analyze it."

# - STOP immediately.
# - Do NOT add explanations.
# - Do NOT include any analysis, summary, skills, or scores.

# 2. RESUME REQUIRED CHECK:
# - If the user requests resume analysis but Resume Content is missing,
#   politely ask them to upload the resume before proceeding.

# 3. STRICT RESUME-BASED ANALYSIS:
# - Perform analysis ONLY when valid resume content is provided.
# - Base all responses strictly on the given resume.
# - Do NOT assume, infer, or invent any skills, experience, tools, or projects.

# 4. RESUME ACCURACY SCORE:
# - Provide an overall score between 0–100%.
# - The score must be based on:
#   - Resume structure
#   - Clarity
#   - Skills relevance
#   - Projects
#   - Job readiness
# - Provide a brief justification.

# 5. LANGUAGE RULE:
# - Respond in the SAME language as the user's question.

# 6. JOB DESCRIPTION GENERATION (SKILLS-BASED ONLY):
# - Generate job roles and job descriptions ONLY using skills explicitly mentioned in the resume.
# - Do NOT add or invent any new skills, tools, or technologies.
# - Generate a maximum of 1–2 relevant job roles.
# - If the resume skills are insufficient to determine a role, clearly state that.

# 7. OUTPUT FORMAT OVERRIDE (MANDATORY):
# - You MUST format the entire response strictly in VALID MARKDOWN.
# - Every section heading MUST start with "## ".
# - NEVER write headings inline with text.
# - ALWAYS leave one blank line after each heading.
# - Bullet points MUST start with "- ".
# - If you violate markdown formatting, the response is INVALID.



# ========================
# OUTPUT FORMAT
# (MANDATORY — MARKDOWN ONLY)
# ========================

# ## Resume Summary:
# (Write a concise 2–3 line professional summary strictly based on the resume.)

# ## Resume Accuracy Score:
# - Overall Score: XX%
# - Reason: (Short and clear justification.)

# ## Good Skills Identified:
# - Skill 1
# - Skill 2
# - Skill 3

# ## Recommended Skills to Add:
# - Skill 1 (reason)
# - Skill 2 (reason)

# ## Areas of Improvement:
# - Area 1
# - Area 2
# - Area 3

# ## Resume Improvement Suggestions:
# - Suggestion 1
# - Suggestion 2

# ## Recommended Job Roles & Descriptions:

# ## Role Name:

# - Short job description based ONLY on resume skills.
# - Key responsibilities aligned with mentioned projects/skills.
# - Required skills: (list ONLY from resume)
# - Suitable for: Fresher / Intern / Entry-level

# ## Job Readiness Level:
# Beginner / Intermediate / Job-Ready

# IMPORTANT:
# - Use clear line breaks between sections.
# - Start each section on a new line.
# - Use bullet points with hyphens (-).
# - Do NOT merge headings and content.
# """


          
      
#         index = pc.Index(os.getenv('PINECONE_INDEX'))

#         prompt_template = ChatPromptTemplate.from_template(template)

#         vectorstore = PineconeVectorStore(
#             index=index,
#             embedding=embed_model,
#             text_key=os.getenv('PINECONE_TEXT_FIELD'),
#             namespace=namespace_id
#         )

#         # Retrieve relevant resume chunks
#         retrieved_data = vectorstore.similarity_search(
#             question,
#             namespace=namespace_id,
#             k=20
#         )

#         fileContent = ""

#         for doc in retrieved_data:
#             if doc.metadata.get("type") == "pdf":
#                 fileContent += (
#                     f"{doc.page_content.strip()}\n"
#                     f"Page No: {doc.metadata.get('page')}\n"
#                     f"File Name: {doc.metadata.get('name')}\n\n"
#                 )
#             else:
#                 fileContent += (
#                     f"{doc.page_content.strip()}\n"
#                     f"File Name: {doc.metadata.get('name')}\n\n"
#                 )

#         # If Pinecone retrieval is weak, still analyze resume
#         if not fileContent.strip():
#             fileContent = "This document is a resume. Analyze the resume holistically."

#         prompt = prompt_template.format(
#             question=question,
#             chatHistory=chatHistory,
#             fileContent=fileContent
#         )

#         chain = llm | StrOutputParser()

#         # ✅ ASYNC STREAMING
#         async for chunk in chain.astream(prompt):
#             yield chunk
#         # async def chain_resp(self,namespace_id: str,question: str, chatHistory: str):
#         # index = pc.Index(os.getenv('PINECONE_INDEX'))

#         # prompt_template = ChatPromptTemplate.from_template(template)

#         # vectorstore = PineconeVectorStore(
#         #     index=index,
#         #     embedding=embed_model,
#         #     text_key=os.getenv('PINECONE_TEXT_FIELD'),
#         #     namespace=namespace_id
#         # )

#         # retrieved_data = vectorstore.similarity_search(question, k=20)

#         # if not retrieved_data:
#         #     yield "Hello 👋 Please upload your resume or ask me to analyze it."
#         #     return

#         # fileContent = ""

#         # for doc in retrieved_data:
#         #     if not doc.page_content.strip():
#         #         continue

#         #     if doc.metadata.get("type") == "pdf":
#         #         fileContent += (
#         #             f"{doc.page_content.strip()}\n"
#         #             f"Page No: {doc.metadata.get('page')}\n"
#         #             f"File Name: {doc.metadata.get('name')}\n\n"
#         #         )
#         #     else:
#         #         fileContent += (
#         #             f"{doc.page_content.strip()}\n"
#         #             f"File Name: {doc.metadata.get('name')}\n\n"
#         #         )

#         # if not fileContent.strip():
#         #     yield "Hello 👋 Please upload your resume or ask me to analyze it."
#         #     return

#         # prompt = prompt_template.format(
#         #     question=question,
#         #     chatHistory=chatHistory,
#         #     fileContent=fileContent
#         # )

#         # chain = llm | StrOutputParser()

#         # for chunk in chain.stream(prompt):
#         #     yield chunk



import os
from config import constants
from utils.backgroud_exeption import handleExceptions
from utils.processor import parse_pdf, parse_text
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
import re
import json
from datetime import datetime

embed_model = MistralAIEmbeddings(
    model=os.getenv('MISTRAL_EMBED_MODEL'),
    api_key=os.getenv('MISTRAL_API_KEY'),
)

llm = ChatMistralAI(
    mistral_api_key=os.getenv('MISTRAL_API_KEY'),
    model=os.getenv('MISTRAL_MODEL'),
    temperature=0,
)

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'), environment=os.getenv('PINECONE_ENV'))


class PineconeService:

    async def vectorize_documents_main(self, namespace_id: str):
        import traceback
        print("=" * 70)
        print(f"[INFO] Starting vectorization for namespace: {namespace_id}")
        
        in_process_dir = os.path.join(
            constants.UPLOAD_DIR,
            namespace_id,
            constants.PRIMARY_FOLDER
        )
        
        print(f"[INFO] Upload folder path: {in_process_dir}")

        if not os.path.exists(in_process_dir):
            print(f"[ERROR] Directory not found: {in_process_dir}")
            return {"error": "Upload directory not found"}

        all_documents = []
        processed_files = []
        failed_files = []

        try:
            for file in os.listdir(in_process_dir):
                file_path = os.path.join(in_process_dir, file)

                if os.path.isdir(file_path):
                    print(f"[SKIP] Skipping subdirectory: {file}")
                    continue

                file_ext = file.split(".")[-1].lower()
                print(f"[INFO] Processing file: {file} (type: {file_ext})")

                try:
                    if file_ext == "txt":
                        docs = parse_text(file_path)
                        doc_type = "txt"
                    elif file_ext == "pdf":
                        docs = parse_pdf(file_path)
                        doc_type = "pdf"
                    else:
                        print(f"[WARN] Unsupported file type: {file_ext}. Skipping.")
                        failed_files.append(file)
                        continue

                    if not docs:
                        print(f"[WARN] No content extracted from {file}")
                        failed_files.append(file)
                        continue

                    print(f"[DEBUG] Extracted {len(docs)} text chunks from {file}")

                    for doc in docs:
                        doc.metadata = doc.metadata or {}
                        doc.metadata["name"] = file
                        doc.metadata["namespace_id"] = namespace_id
                        doc.metadata["type"] = doc_type

                    all_documents.extend(docs)
                    processed_files.append(file)

                    # Remove file after processing
                    os.remove(file_path)
                    print(f"[INFO] Removed file after processing: {file_path}")

                except Exception as e:
                    print(f"[ERROR] Failed to process {file}: {str(e)}")
                    traceback.print_exc()
                    failed_files.append(file)

            if not all_documents:
                print("[WARN] No valid documents to vectorize")
                return {"message": "No valid content found in uploaded documents."}

            print(f"[INFO] Total documents to vectorize: {len(all_documents)}")

            # Test embedding model
            try:
                test_vector = embed_model.embed_query("hello world")
                print(f"[DEBUG] Embedding model test successful. Vector dimension = {len(test_vector)}")
            except Exception as e:
                print(f"[ERROR] Embedding model failed: {e}")
                traceback.print_exc()
                return {"error": "Embedding model not working properly"}

            # Check/create Pinecone index
            try:
                index_name = os.getenv('PINECONE_INDEX')
                print(f"[INFO] Checking Pinecone index: {index_name}")
                existing_indexes = [idx.name for idx in pc.list_indexes()]
                print(f"[DEBUG] Existing indexes: {existing_indexes}")
                
                if index_name not in existing_indexes:
                    print(f"[WARN] Index '{index_name}' not found. Creating new index...")
                    pc.create_index(name=index_name, dimension=len(test_vector), metric="cosine")
                    print(f"[SUCCESS] Index '{index_name}' created successfully")
                    
            except Exception as e:
                print(f"[ERROR] Failed to connect or create Pinecone index: {e}")
                traceback.print_exc()
                return {"error": "Pinecone index connection failed"}

            # Upload to Pinecone
            try:
                print(f"[INFO] Uploading embeddings to Pinecone namespace: {namespace_id}")
                vectorstore = PineconeVectorStore.from_documents(
                    documents=all_documents,
                    index_name=index_name,
                    embedding=embed_model,
                    namespace=namespace_id
                )
                print("[SUCCESS] Embeddings uploaded successfully to Pinecone!")
                
                # Get stats
                index = pc.Index(index_name)
                stats = index.describe_index_stats()
                count = stats.get("namespaces", {}).get(namespace_id, {}).get("vector_count", 0)
                print(f"[INFO] Namespace '{namespace_id}' now contains {count} vectors in Pinecone.")
                
            except Exception as e:
                print(f"[ERROR] Pinecone upload failed: {e}")
                traceback.print_exc()
                return {"error": "Failed to upload vectors to Pinecone"}

            print("=" * 70)
            return {
                "message": f"Successfully processed {len(processed_files)} files and uploaded {len(all_documents)} document chunks to Pinecone.",
                "processed_files": processed_files,
                "failed_files": failed_files,
                "total_vectors": len(all_documents)
            }

        except Exception as e:
            print(f"[CRITICAL ERROR] Vectorization process failed: {e}")
            traceback.print_exc()
            return {"error": f"Vectorization process failed: {str(e)}"}

    def _extract_skills_from_text(self, text: str) -> list:
        """Extract skills dynamically from text"""
        text_lower = text.lower()
        found_skills = []
        
        # Tech skills patterns
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 
            'node.js', 'django', 'flask', 'express', 'spring', 'nestjs',
            'mysql', 'mongodb', 'postgresql', 'redis', 'sqlite', 'oracle',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'jenkins', 'git', 'github', 'gitlab', 'jira', 'confluence',
            'linux', 'bash', 'shell', 'html', 'css', 'typescript',
            'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
            'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
            'machine learning', 'deep learning', 'nlp', 'opencv',
            'android', 'ios', 'react native', 'flutter'
        ]
        
        for skill in tech_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        # Also look for skills in ALL CAPS
        caps_matches = re.findall(r'\b[A-Z]{2,}\b', text)
        for match in caps_matches:
            if len(match) > 2 and match not in found_skills:
                found_skills.append(match)
        
        # Remove duplicates and return
        return list(set(found_skills))

    def _extract_experience_from_text(self, text: str) -> str:
        """Extract experience from text"""
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

    @handleExceptions
    async def delete_vectorized_docs(self, namespace_id: str, key: str, values: list[str]):
        index = pc.Index(os.getenv('PINECONE_INDEX'))
        filter_condition = {key: {"$in": values}}
        response = index.delete(delete_all=False, namespace=namespace_id, filter=filter_condition)
        return response

    async def chain_resp(self, namespace_id: str, question: str, chatHistory: str):
        # SMART AUTO-ANALYSIS SYSTEM
        template = """You are an expert resume analyzer. AUTOMATICALLY analyze the resume content below.

RESUME CONTENT:
{fileContent}

USER QUESTION: {question}

PREVIOUS CONVERSATION:
{chatHistory}

SMART ANALYSIS RULES:
1. If a resume is uploaded, AUTOMATICALLY provide full analysis
2. Give UNIQUE scores (0-100%) based on actual resume content
3. Extract ONLY skills actually mentioned in the resume
4. Provide personalized feedback for THIS specific resume
5. Suggest job roles matching THEIR actual skills
6. Give actionable improvement suggestions

ALWAYS PROVIDE:
- Overall Score (0-100%)
- Skills Found (list actual skills from resume)
- Strengths (specific to this resume)
- Weaknesses (gaps in this resume)
- Job Recommendations (based on their skills)
- Improvement Suggestions (personalized)

Make every analysis unique and specific to the individual resume."""

        index = pc.Index(os.getenv('PINECONE_INDEX'))

        prompt_template = ChatPromptTemplate.from_template(template)

        vectorstore = PineconeVectorStore(
            index=index,
            embedding=embed_model,
            text_key=os.getenv('PINECONE_TEXT_FIELD'),
            namespace=namespace_id
        )

        # Retrieve relevant resume chunks with higher k for better context
        retrieved_data = vectorstore.similarity_search(
            question,
            namespace=namespace_id,
            k=25  # Increased for better context
        )

        fileContent = ""
        all_extracted_skills = set()
        all_experience_info = ""

        # Build comprehensive content from retrieved chunks
        for doc in retrieved_data:
            if doc.page_content.strip():
                fileContent += f"{doc.page_content.strip()}\n"

                # Extract skills from this chunk
                skills_from_chunk = self._extract_skills_from_text(doc.page_content)
                all_extracted_skills.update(skills_from_chunk)
                
                # Extract experience from this chunk
                exp_from_chunk = self._extract_experience_from_text(doc.page_content)
                if exp_from_chunk != "Experience not specified":
                    all_experience_info = exp_from_chunk

        # If no skills found in metadata, scan the entire content
        if not all_extracted_skills:
            all_extracted_skills = set(self._extract_skills_from_text(fileContent))
        
        if not all_experience_info:
            all_experience_info = self._extract_experience_from_text(fileContent)

        # Handle empty content case
        if not fileContent.strip():
            yield "I don't see any resume content to analyze. Please upload your resume first, and I'll provide personalized feedback based on your actual experience and skills."
            return

        # Prepare skills and experience context
        if all_extracted_skills:
            extractedSkills = "Skills found in your resume: " + ", ".join(sorted(all_extracted_skills))
        else:
            extractedSkills = "No specific technical skills were clearly identified in your resume."

        prompt = prompt_template.format(
            question=question,
            chatHistory=chatHistory,
            fileContent=fileContent[:4000]  # Increased limit for better analysis
        )

        chain = llm | StrOutputParser()

        # Stream the response
        async for chunk in chain.astream(prompt):
            yield chunk