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
        id = request.state.user['id']
        user = User.objects(id = ObjectId(id)).first()
        if not user:
             return error('User Not Found')
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
      
    
    # async def chat_conversation(self,data):  
    #         question = data.question
    #         namespace_id = data.namespace_id 
    #         chatHistory = ""
    #         for chat in data.chatHistory:
    #             chatHistory += f"User: {chat.question}\nAI: {chat.Ai_response}\n"
            
    #         return StreamingResponse(self.pineconeService.chain_resp(namespace_id,question,chatHistory), media_type="text/event-stream")
    

    async def chat_conversation(self, data):
        question = data.question
        namespace_id = data.namespace_id

    # 🔴 STEP 1: namespace valid hai ya nahi
        bot = KnowledgeBot.objects(namespace_id=namespace_id).first()
        if not bot:
            return error("No resume / document found. Please upload again.")

        chatHistory = ""
        for chat in data.chatHistory:
            chatHistory += f"User: {chat.question}\nAI: {chat.Ai_response}\n"

        return StreamingResponse(
                self.pineconeService.chain_resp(namespace_id, question, chatHistory),
        media_type="text/event-stream"
    )


    async def delete_bot(self, namespace_id: str):
        # 🔴 STEP 2.1: MongoDB se delete
            bot = KnowledgeBot.objects(namespace_id=namespace_id).first()
            if not bot:
                return error("Bot / Resume not found")

            bot.delete()

        # 🔴 STEP 2.2: Pinecone se vectors delete
            await self.pineconeService.delete_namespace(namespace_id)

            return success("Resume and chatbot data deleted successfully")

    


