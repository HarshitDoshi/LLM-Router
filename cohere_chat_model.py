import os
from typing import AsyncGenerator, Union
from cohere import Client as Cohere
from cohere.types.streamed_chat_response import (
    StreamedChatResponse_StreamStart as CohereStreamedChatResponse_StreamStart,
)
from cohere.types.streamed_chat_response import (
    StreamedChatResponse_TextGeneration as CohereStreamedChatResponse_TextGeneration,
)
from cohere.types.streamed_chat_response import (
    StreamedChatResponse_StreamEnd as CohereStreamedChatResponse_StreamEnd,
)
from common import ChatModel


class CohereChatModel(ChatModel):
    def __init__(self):
        self.client = Cohere(api_key=os.getenv("COHERE_API_KEY"))

    async def send_message(
        self, message: str, stream: bool = False, **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        chat_history = kwargs.get("chat_history", [])
        model = kwargs.get("model", "command")
        connectors = kwargs.get("connectors", [])

        chat_history.append({"role": "USER", "message": message})

        if stream:
            return self._send_streaming_message(
                chat_history=chat_history,
                message=message,
                model=model,
                connectors=connectors,
            )
        else:
            return self._send_non_streaming_message(
                chat_history=chat_history,
                message=message,
                model=model,
                connectors=connectors,
            )

    def _send_non_streaming_message(self, **kwargs) -> str:
        response = self.client.chat(
            chat_history=kwargs.get("chat_history"),
            message=kwargs.get("message"),
            model=kwargs.get("model"),
            connectors=kwargs.get("connectors"),
        )
        return self.extract_response(response)

    async def _send_streaming_message(self, **kwargs) -> AsyncGenerator[str, None]:
        # This is pseudo-code and needs to be adapted to how Cohere's API would handle streaming
        for chunk in self.client.chat_stream(
            chat_history=kwargs.get("chat_history"),
            message=kwargs.get("message"),
            model=kwargs.get("model"),
            connectors=kwargs.get("connectors"),
        ):
            yield self.extract_response(chunk, stream=True)

    def extract_response(self, response, stream: bool = False):
        if stream:
            if type(response) is CohereStreamedChatResponse_StreamStart:
                return ""
            elif type(response) is CohereStreamedChatResponse_TextGeneration:
                text_generation: CohereStreamedChatResponse_TextGeneration = response
                return text_generation.text
            elif type(response) is CohereStreamedChatResponse_StreamEnd:
                return ""
            else:
                return ""
        else:
            return response.text
