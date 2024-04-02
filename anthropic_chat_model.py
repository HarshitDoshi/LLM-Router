import os
from typing import AsyncGenerator, List, Union
from anthropic import Anthropic
from anthropic.types.message import Message as AnthropicMessage
from anthropic.types.content_block import ContentBlock as AnthropicContentBlock
from anthropic.types.content_block_start_event import (
    ContentBlockStartEvent as AnthropicContentBlockStartEvent,
)
from anthropic.types.content_block_delta_event import (
    ContentBlockDeltaEvent as AnthropicContentBlockDeltaEvent,
    TextDelta as AnthropicTextDelta,
)
from anthropic.types.message_start_event import (
    MessageStartEvent as AnthropicMessageStartEvent,
)
from common import ChatModel


class AnthropicChatModel(ChatModel):
    """
    Anthropic specific chat model implementation.
    """

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
        response = self.client.messages.create(
            model=kwargs.get("model", "claude-2.1"),
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=messages,
            stream=False,
        )
        return self.extract_response(response)

    async def _send_streaming_message(
        self, messages, **kwargs
    ) -> AsyncGenerator[str, None]:
        for chunk in self.client.messages.create(
            model=kwargs.get("model", "claude-2.1"),
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=messages,
            stream=True,
        ):
            yield self.extract_response(chunk, stream=True)

    def extract_response(self, response, stream: bool = False) -> str:
        if stream:
            if type(response) is AnthropicMessageStartEvent:
                message_start_event: AnthropicMessageStartEvent = response
                message: AnthropicMessage = message_start_event.message
                content: List[AnthropicContentBlock] = message.content
                if len(content) == 0:
                    return ""
                else:
                    last_content_block = content[0]
                    if last_content_block.type == "text":
                        return last_content_block.text
                    else:
                        return "Non-text response received."
            elif type(response) is AnthropicContentBlockStartEvent:
                content_block_start_event: AnthropicContentBlockStartEvent = response
                content_block: AnthropicContentBlock = (
                    content_block_start_event.content_block
                )
                if content_block.type == "text":
                    return content_block.text
                else:
                    return "Non-text response received."
            elif type(response) is AnthropicContentBlockDeltaEvent:
                content_block_delta_event: AnthropicContentBlockDeltaEvent = response
                text_delta: AnthropicTextDelta = content_block_delta_event.delta
                return text_delta.text
            elif type(response) is AnthropicContentBlock:
                content_block: AnthropicContentBlock = response
                if content_block.type == "text":
                    return content_block.text
                else:
                    return "Non-text response received."
        else:
            message: AnthropicMessage = response
            content: List[AnthropicContentBlock] = message.content
            last_content_block = content[0]
            if last_content_block.type == "text":
                return last_content_block.text
            else:
                return "Non-text response received."
