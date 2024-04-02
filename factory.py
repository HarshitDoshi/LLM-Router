from openai_chat_model import OpenAIChatModel
from anthropic_chat_model import AnthropicChatModel
from cohere_chat_model import CohereChatModel
from common import ChatModel


class ChatModelFactory:
    """
    Factory for creating chat model instances.
    """

    @staticmethod
    def create(chat_model_name: str, **kwargs) -> ChatModel:
        if chat_model_name == "openai":
            return OpenAIChatModel(**kwargs)
        elif chat_model_name == "anthropic":
            return AnthropicChatModel(**kwargs)
        elif chat_model_name == "cohere":
            return CohereChatModel(**kwargs)
        else:
            raise ValueError(f"Unsupported model: {chat_model_name}")
