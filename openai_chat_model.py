import os
from typing import List, AsyncGenerator, Union
from openai import OpenAI
from openai.types.chat.chat_completion import (
    ChatCompletion as OpenAIChatCompletion,
    Choice as OpenAIChoice,
)
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk as OpenAIChatCompletionChunk,
)
from common import ChatModel


class OpenAIChatModel(ChatModel):
    """
    OpenAI specific chat model implementation.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def send_message(
        self, message: str, stream: bool = False, **kwargs
    ) -> Union[str, AsyncGenerator[str, None]]:
        messages = kwargs.get("messages", [])
        messages.append({"role": "user", "content": message})

        if stream:
            return self._send_streaming_message(messages, **kwargs)
        else:
            return self._send_non_streaming_message(messages, **kwargs)

    def _send_non_streaming_message(self, messages, **kwargs) -> str:
        completion = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=messages,
            stream=False,
        )
        return self.extract_response(completion, stream=False)

    async def _send_streaming_message(
        self, messages, **kwargs
    ) -> AsyncGenerator[str, None]:
        for completion in self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        ):
            yield self.extract_response(completion, stream=True)

    def extract_response(
        self,
        completion,
        stream: bool = False,
    ):
        if stream:
            openai_completion_chunk: OpenAIChatCompletionChunk = completion
            openai_completion_chunk
            choices: List[OpenAIChoice] = openai_completion_chunk.choices
            last_choice = choices[-1]
            if last_choice.finish_reason is None:
                return last_choice.delta.content
            else:
                return ""
        else:
            openai_completion: OpenAIChatCompletion = completion
            choices: List[OpenAIChoice] = openai_completion.choices
            last_choice = choices[-1]
            if last_choice.message.role == "assistant":
                return last_choice.message.content
            else:
                return "Non-text response received."
