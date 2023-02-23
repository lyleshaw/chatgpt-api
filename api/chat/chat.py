import os
from typing import Optional

from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot

from api.logger import logger
from api.model import ChatRequest, ChatResponse

chatbot: Optional[Chatbot] = None
load_dotenv(verbose=True)
config = {
    "access_token": os.environ.get("ACCESS_TOKEN")
}


def _get_chatbot() -> Chatbot:
    global chatbot
    if chatbot is None:
        chatbot = Chatbot(config)
    return chatbot


def chat_replay(request: ChatRequest) -> ChatResponse:
    logger.info("chat_replay start")
    chatbot = _get_chatbot()
    data = None
    logger.info("chat_replay request: %s", request)
    if request.options is None:
        for data in chatbot.ask(
                request.prompt,
        ):
            response = data["message"]
    else:
        for data in chatbot.ask(
                request.prompt,
                conversation_id=request.options.conversationId,
                parent_id=request.options.parentMessageId
        ):
            response = data["message"]
    logger.info("chat_replay data: %s", data)
    logger.info("chat_replay end")
    return ChatResponse(
        id=data["parent_id"],
        parentMessageId=data["parent_id"],
        conversationId=data["conversation_id"],
        text=data["message"]
    )


if __name__ == "__main__":
    chat_replay(ChatRequest(prompt="Hello world"))
