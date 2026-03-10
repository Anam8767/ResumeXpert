# from bson import ObjectId
# from fastapi import  BackgroundTasks
# from models.schemas import KnowledgeBotFiles
# from utils.helper import save_uploaded_file
# from utils.success import error, result, success


# class ChatbotFilesService:
    
#     def __init__(self,pineconeService):
#         self.pineconeService=pineconeService
        
#     async def upload_files(self,namespace_id,files,chatbot_id,backgroundTasks:BackgroundTasks):
#         if len(files):
#             for file in files: 
#                 save_uploaded_file(file, namespace_id)
#                 createdObj = {
#                 'name':file.filename,
#                 "namespace_id":namespace_id,
#                 "chatbot_id":chatbot_id,
#                 "size":file.size,
#                 }
#                 data = KnowledgeBotFiles(**createdObj)
#                 data.save()
#                 backgroundTasks.add_task(self.pineconeService.vectorize_documents_main,namespace_id)
            

#         return success(f"Total {len(files)} files uploaded successfully!")
    
#     async def getFilesByChatBotId(self,chatBotId): 
#          items = KnowledgeBotFiles.objects(chatbot_id = ObjectId(chatBotId))
#          return result([item.to_mongo().to_dict() for item in items]) 
        
    
#     async def delete_files(self,data,backgroundTasks:BackgroundTasks): 
#             reqObj={
#              "ids":data.ids,
#              "names":data.names,
#              "namespace_id":data.namespace_id
#             } 
            
#             object_ids = [ObjectId(id) for id in reqObj['ids']] 
#             result = KnowledgeBotFiles.objects(id__in=object_ids).delete()
#             backgroundTasks.add_task(self.pineconeService.delete_vectorized_docs,reqObj['namespace_id'],"name",reqObj['names'])
#             return success("File deleted Successfully!")
    

#     async def delete_file(self,data,backgroundTasks:BackgroundTasks): 
       
#         reqObj={
#             "id":data.id,
#             "name":data.name,
#             "namespace_id":data.namespace_id
#             }  
            
#         result = KnowledgeBotFiles.objects(id=ObjectId(reqObj['id'])).delete()
#         backgroundTasks.add_task(self.pineconeService.delete_vectorized_docs,reqObj['namespace_id'],"name",[reqObj['name']])
#             # if result == 0:
#             #     return error(f"Item with ID {reqObj['id']} deleted successfully")
#             # else:
#             #     return success("File deleted Successfully!")
#         if result == 0:
#                 return error(f"Item with ID {reqObj['id']} not found or already deleted")
#         else:
#                 return success("File deleted Successfully!")

    

from bson import ObjectId
from fastapi import BackgroundTasks
from models.schemas import KnowledgeBotFiles
from utils.helper import save_uploaded_file
from utils.success import error, result, success
import os
import json
from datetime import datetime
from services.resume_analyzer import DynamicResumeAnalyzer

class ChatbotFilesService:
    
    def __init__(self, pineconeService):
        self.pineconeService = pineconeService
        
    async def upload_files(self, namespace_id, files, chatbot_id, backgroundTasks: BackgroundTasks):
        if len(files):
            for file in files: 
                file_path = save_uploaded_file(file, namespace_id)
                
                # NEW: Enhanced immediate resume analysis
                self._analyze_resume_immediately(file_path, file.filename, namespace_id)
                
                createdObj = {
                    'name': file.filename,
                    "namespace_id": namespace_id,
                    "chatbot_id": chatbot_id,
                    "size": file.size,
                }
                data = KnowledgeBotFiles(**createdObj)
                data.save()
                
                # Start vectorization in background
                backgroundTasks.add_task(self.pineconeService.vectorize_documents_main, namespace_id)
                
                # NEW: Auto-trigger analysis after vectorization
                backgroundTasks.add_task(self._auto_analyze_after_upload, namespace_id, file.filename)
            
        return success(f"Total {len(files)} files uploaded successfully! Analysis will start automatically.")
    
    # NEW: Auto-analysis trigger after upload
    async def _auto_analyze_after_upload(self, namespace_id: str, filename: str):
        """Automatically trigger resume analysis after upload"""
        try:
            import time
            time.sleep(3)  # Wait for vectorization to complete
            
            print(f"[AUTO] Triggering automatic analysis for {filename}")
            
            # This will make the chat automatically analyze when user sends any message
            # The enhanced chat service will detect the uploaded resume and auto-analyze
            
        except Exception as e:
            print(f"[AUTO] Error in auto-analysis trigger: {e}")
    
    # NEW: Enhanced immediate resume analysis function
    def _analyze_resume_immediately(self, file_path: str, file_name: str, namespace_id: str):
        """Analyze resume as soon as it's uploaded with dynamic analysis"""
        try:
            print(f"Starting enhanced analysis for {file_name}...")
            file_ext = os.path.splitext(file_name)[1].lower()
            text = ""
            
            # Read file and extract text
            if file_ext == '.pdf':
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                except Exception as e:
                    print(f"Error reading PDF: {e}")
                    return
            elif file_ext in ['.docx', '.doc']:
                try:
                    import docx2txt
                    text = docx2txt.process(file_path)
                except Exception as e:
                    print(f"Error reading DOCX: {e}")
                    return
            elif file_ext == '.txt':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                except Exception as e:
                    print(f"Error reading TXT: {e}")
                    return
            else:
                print(f"Unsupported file type: {file_ext}")
                return
            
            if not text.strip():
                print(f"No text extracted from {file_name}")
                return
            
            # Use the DynamicResumeAnalyzer for comprehensive analysis
            analysis = DynamicResumeAnalyzer.analyze_resume_completely(text, file_name)
            
            # Save enhanced analysis to JSON file
            analysis_file = os.path.join(
                os.path.dirname(file_path),
                f"{os.path.splitext(file_name)[0]}_enhanced_analysis.json"
            )
            
            # Add additional metadata
            analysis['namespace_id'] = namespace_id
            analysis['file_size'] = os.path.getsize(file_path)
            analysis['text_length'] = len(text)
            analysis['analysis_version'] = "2.0"
            
            with open(analysis_file, 'w') as f:
                json.dump(analysis, f, indent=2)
                
            print(f"✓ Enhanced analysis saved for {file_name}")
            print(f"  - Score: {analysis['score']}%")
            print(f"  - Skills: {len(analysis['skills'])}")
            print(f"  - Job Roles: {', '.join(analysis['job_roles'])}")
            print(f"  - Suggestions: {len(analysis['suggestions'])}")
            
        except Exception as e:
            print(f"Error in enhanced analysis for {file_name}: {e}")
            import traceback
            traceback.print_exc()