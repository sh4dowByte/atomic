from app.chat import ask, chat
from app.config import AI_NAME

async def prompt(client, coder_input):
    """Handle Assistant-related AI interactions."""
    chat_history = [{
        "role": "system",
        "content": (
            f"You are {AI_NAME}, a highly intelligent and helpful AI assistant. "
            "Your primary goal is to provide accurate, clear, and concise responses. "
            "Adapt your answers based on user intent and provide step-by-step guidance when necessary. "
            "Keep responses informative and to the point."
        )
    }]

    if isinstance(coder_input, str): 
        chat_history.append({"role": "user", "content": coder_input})
        await ask(client, chat_history)
    else: 
        await chat(client, chat_history)
