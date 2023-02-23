from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.chat.chat import chat_replay
from api.logger import logger
from api.model import ChatRequest

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def success_response(message: str = None, data: (list, dict) = None) -> JSONResponse:
    result = {
        'status': "Success",  # error code
        'message': message,  # show for user
        'data': data,  # data if success else null, be list or dict
    }
    return JSONResponse(result, media_type="application/json")


def error_response(message: str = None, data: (list, dict) = None) -> JSONResponse:
    result = {
        'status': "Fail",  # error code
        'message': message,  # show for user
        'data': data,  # data if success else null, be list or dict
    }
    return JSONResponse(result, media_type="application/json")


# Path: /api/chat
# Param: ChatRequest
# Return: JSONResponse
@app.post("/api/chat")
async def chat(request: ChatRequest) -> JSONResponse:
    logger.info("chat start")
    logger.info("HTTP /chat request: %s", request)
    try:
        data = chat_replay(request)
    except Exception as e:
        logger.error("chat error: %s", e)
        return error_response(message="OpenAI error, maybe you touched the limit.")
    logger.info("HTTP /chat data: %s", data)
    logger.info("chat end")
    return success_response(data=data.dict())


# Path: /api/chat-process
# Param: ChatRequest
# Return: JSONResponse
@app.post("/api/chat-process")
async def chat_progress(request: ChatRequest) -> JSONResponse:
    logger.info("chat_progress start")
    logger.info("HTTP /chat-process request: %s", request)
    try:
        data = chat_replay(request)
    except Exception as e:
        logger.error("chat error: %s", e)
        return error_response(message="OpenAI error, maybe you touched the limit.")
    logger.info("HTTP /chat-process data: %s", data)
    logger.info("chat_progress end")
    return success_response(message="success", data=data.dict())


# start server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3002)
