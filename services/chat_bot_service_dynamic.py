from datetime import datetime
import uuid
from fastapi import BackgroundTasks
from utils.success import error, result,success
from models.schemas import KnowledgeBot, User
from dotenv import load_dotenv
from bson import ObjectId
from fastapi.responses import StreamingResponse


load_dotenv()

 

class ChatBot:
    
    def __init__(self,pineconeService):
        self.pineconeService = pineconeService

    async def create(self,data,request,backgroundTasks:BackgroundTasks):
        try:
            id = request.state.user['id']
            user = User.objects(id = ObjectId(id)).first()
        except AttributeError:
            # No authentication - use super admin for testing
            user = User.objects(role="SUPER_ADMIN").first()
            if not user:
                return error('Super Admin Not Found')
            id = str(user.id)
        namespace_id = str(uuid.uuid4())  
        data_dict = data.dict()  
        data_dict['namespace_id'] = namespace_id
        data_dict['user_id'] = id 

        botData = KnowledgeBot(**data_dict)      
        botData.save()
        
        return result({"namespace_id": namespace_id}, "Congratulations, your created your bot")
    
    async def getBotByUserId(self,request):  
         id = request.query_params.get('id') if request.query_params.get('id') else request.state.user['id']
         items = KnowledgeBot.objects(user_id =ObjectId(id))

         return result([item.to_mongo().to_dict() for item in items])
        
    
    async def getBotById(self,id): 
         cursor = KnowledgeBot.objects(id = ObjectId(id))  
         return result(cursor.first().to_mongo().to_dict())
      
    
    async def chat_conversation(self, data):  
        question = data.question.strip()
        namespace_id = data.namespace_id

    # ---------------- STEP 1: Greeting HARD STOP ----------------
        greetings = ["hi", "hii", "hello", "hey", "thanks", "thank you"]

        if question.lower() in greetings:
            return success("hello 👋 Please upload your resume or ask me to analyze it.")

    # ---------------- STEP 2: Empty question guard ----------------
        if not question or len(question) < 2:
            return error("Please ask a valid question or upload your resume.")

    # ---------------- STEP 3: Build chat history ----------------
        chatHistory = ""
        for chat in data.chatHistory:
            chatHistory += f"User: {chat.question}\nAI: {chat.Ai_response}\n"
    


    # ---------------- STEP 4: ONLY NOW call LLM ----------------
        return StreamingResponse(
        self.pineconeService.chain_resp(namespace_id, question, chatHistory),
        media_type="text/event-stream"
    )
