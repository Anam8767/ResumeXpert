from fastapi import APIRouter, Depends
from models.dto import ChatRequest
from services.chat_bot_service import ChatBot
from services.pinecone_service import PineconeService
from utils.helper import get_current_token 
from utils.success import success

router = APIRouter()

pineconeService = PineconeService()
chatBotService = ChatBot(pineconeService)

@router.post("/auto-analyze")
async def auto_analyze_resume(data: ChatRequest):
    """Automatically analyze uploaded resume without user prompt"""
    try:
        # Force automatic analysis
        data.question = "Please analyze my uploaded resume and provide detailed feedback with score, skills, and suggestions"
        
        # Get the analysis response
        response = await chatBotService.chat_conversation(data)
        return response
        
    except Exception as e:
        return success(f"Auto-analysis started: {str(e)}")

@router.post("/smart-analyze")
async def smart_analyze(namespace_id: str):
    """Smart analysis that triggers automatically when resume is detected"""
    try:
        # Create a dummy chat request to trigger analysis
        from models.dto import ChatHistory
        dummy_request = ChatRequest(
            question="Analyze my resume",
            namespace_id=namespace_id,
            chatHistory=[]
        )
        
        return await chatBotService.chat_conversation(dummy_request)
        
    except Exception as e:
        return success(f"Smart analysis triggered: {str(e)}")
