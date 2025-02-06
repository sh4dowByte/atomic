from app.chat import ask, chat

async def prompt(client, coder_input):
    """Handle programming-related AI interactions."""
    chat_history = [{
        "role": "system", 
        "content": (
            "You are a highly skilled programming assistant. "
            "Your primary role is to help users write, debug, and optimize code. "
            "Provide clear, efficient, and well-documented code snippets."
        )
    }]

    if isinstance(coder_input, str): 
        chat_history.append({"role": "user", "content": coder_input})
        await ask(client, chat_history)
    else: 
        await chat(client, chat_history)
