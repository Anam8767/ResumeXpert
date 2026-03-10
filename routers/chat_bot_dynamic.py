# from fastapi import APIRouter,UploadFile,File,BackgroundTasks,Form,Request,Depends
# from models.dto import DeleteFileDTO,ChatRequest,CreateBot,DeleteFilesDTO
# from services.chat_bot_service import ChatBot
# from typing import List
# from services.pinecone_service import PineconeService
# from utils.helper import get_current_token 
# router = APIRouter() 

# pineconeService = PineconeService()
# chatBotService = ChatBot(pineconeService)

 

# @router.post("")
# async def create(data:CreateBot,request: Request,backgroundTasks: BackgroundTasks = None):
#     return await chatBotService.create(data,request,backgroundTasks)

# @router.get("/all")
# async def getBotByUserId(request: Request):
#     return await chatBotService.getBotByUserId(request)


# @router.post("/chat")
# async def chatConversation(data: ChatRequest):
#     return await chatBotService.chat_conversation(data)

# @router.get("/{id}",dependencies=[Depends(get_current_token)])
# async def getBotById(id: str):
#     return await chatBotService.getBotById(id)

# # @router.post("/fileUpload")
# # async def upload(namespace_id: str= Form(...),files: List[UploadFile] = File(...),backgroundTasks: BackgroundTasks = None):
# #     return await chatBotService.upload_files(namespace_id,files,backgroundTasks)

# # @router.get("/files")
# # async def getFiles(namespace_id: str):
# #     return await chatBotService.get_files(namespace_id)

# # @router.delete("/files")
# # async def deleteFiles(data:DeleteFilesDTO,backgroundTasks: BackgroundTasks):
# #     return await chatBotService.delete_files(data,backgroundTasks)

# # @router.delete("/file")
# # async def deleteFile(data:DeleteFileDTO,backgroundTasks: BackgroundTasks):
# #     return await chatBotService.delete_file(data,backgroundTasks)



 

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Form, Request, Depends
from models.dto import DeleteFileDTO, ChatRequest, CreateBot, DeleteFilesDTO
from services.chat_bot_service import ChatBot
from typing import List
from services.pinecone_service import PineconeService
from utils.helper import get_current_token

router = APIRouter(prefix="/bot", tags=["Bot"])

# Initialize services
pineconeService = PineconeService()
chatBotService = ChatBot(pineconeService)


# ✅ Create Bot
@router.post("/")
async def create(
    data: CreateBot,
    request: Request,
    backgroundTasks: BackgroundTasks
):
    return await chatBotService.create(data, request, backgroundTasks)


# ✅ Get All Bots By User
@router.get("/all")
async def getBotByUserId(request: Request):
    return await chatBotService.getBotByUserId(request)


# ✅ Chat Conversation
@router.post("/chat")
async def chatConversation(data: ChatRequest):
    return await chatBotService.chat_conversation(data)


# ✅ Get Bot By ID (Protected)
@router.get("/{id}", dependencies=[Depends(get_current_token)])
async def getBotById(id: str):
    return await chatBotService.getBotById(id)


# ✅ Upload Files
@router.post("/fileUpload")
async def upload(
    namespace_id: str = Form(...),
    files: List[UploadFile] = File(...),
    backgroundTasks: BackgroundTasks = None
):
    return await chatBotService.upload_files(namespace_id, files, backgroundTasks)


# ✅ Get Files
@router.get("/files")
async def getFiles(namespace_id: str):
    return await chatBotService.get_files(namespace_id)


# ✅ Delete Multiple Files
@router.delete("/files")
async def deleteFiles(data: DeleteFilesDTO, backgroundTasks: BackgroundTasks):
    return await chatBotService.delete_files(data, backgroundTasks)


# ✅ Delete Single File
@router.delete("/file")
async def deleteFile(data: DeleteFileDTO, backgroundTasks: BackgroundTasks):
    return await chatBotService.delete_file(data, backgroundTasks)