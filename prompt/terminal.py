import os
import platform
import re
from app.chat import ask, chat

async def prompt(client, terminal_input):
    """Handle terminal-specific AI interactions."""
    os_name = platform.system()
    chat_history = [{
        "role": "system", 
        "content":  (
            "You are an expert terminal assistant. "
            "Provide accurate and concise terminal commands based on the user's request. "
            f"The current operating system is {os_name}. "
            "Avoid unnecessary explanations unless requested."
        )
    }]

    if isinstance(terminal_input, str): 
        chat_history.append({
            "role": "system", 
            "content": (
                "Provide exactly one terminal command inside a Markdown ```bash``` block. "
                "The command should be precise and directly related to the user's request."
            )
        })

        chat_history.append({"role": "user", "content": terminal_input})
        response = await ask(client, chat_history)

        match = re.search(r'```bash\s*(.*?)\s*```', response, re.DOTALL)
        if match:
            command = match.group(1).strip()
            confirmation = input("Do you want to run the command? (Y/N): ").strip().upper()
            if confirmation == 'Y':
                try:
                    os.system(command)
                except Exception as e:
                    print(f"Failed to run the command: {e}")
    else: 
        await chat(client, chat_history)
