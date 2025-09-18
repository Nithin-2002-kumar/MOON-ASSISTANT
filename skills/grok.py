from xai_sdk import Client
from xai_sdk.chat import user, system
from core import config  # import your config file


# Initialize Grok client with API key from config.py
grok_client = Client(
    api_key=config.XAI_API_KEY,
    timeout=3600,  # Longer timeout for reasoning models
)


def ask_grok(prompt: str, system_prompt: str = "You are Grok, a highly intelligent, helpful AI assistant."):
    """
    Ask Grok (Grok-4) for a response.
    """
    chat = grok_client.chat.create(model="grok-4")
    chat.append(system(system_prompt))
    chat.append(user(prompt))
    response = chat.sample()
    return response.content
