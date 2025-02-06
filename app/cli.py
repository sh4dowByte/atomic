import argparse
import platform

from openai import AsyncOpenAI
from app.config import update_env_variable, API_KEY, BASE_URL, MODEL_NAME, AI_NAME
from app.chat import ask, chat
from rich.console import Console

console = Console()

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Atomic - Advanced Terminal Operation & Machine Intelligent Commander."
    )
    parser.add_argument("-a", "--ask", nargs="?", const=True, type=str, help="Ask a question.")
    parser.add_argument("-t", "--terminal", nargs="?", const=True, type=str, help="Ask a termnial question.")
    parser.add_argument("-c", "--coder", nargs="?", const=True, type=str, help="Ask as a programmer.")

    parser.add_argument("--API_KEY", type=str, help=f"Change API key (default: {API_KEY})")
    parser.add_argument("--BASE_URL", type=str, help=f"Change Base Url (default: {BASE_URL})")
    parser.add_argument("--MODEL", type=str, help=f"Change Model Name (default: {MODEL_NAME})")
    
    return parser.parse_args()

async def handle_cli(args):
    """Handle CLI-based AI interaction."""

    client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

    if args.API_KEY:
        update_env_variable("API_KEY", args.API_KEY)
    if args.BASE_URL:
        update_env_variable("BASE_URL", args.BASE_URL)
    if args.MODEL:
        update_env_variable("MODEL_NAME", args.MODEL)

    if args.terminal:
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

        if isinstance(args.terminal, str): 
           chat_history.append({"role": "user", "content": args.terminal})
           await ask(client, chat_history)
        else: 
            await chat(client, chat_history)

    elif args.coder:
        chat_history = [{
            "role": "system", 
            "content": (
                "You are a highly skilled programming assistant. "
                "Your primary role is to help users write, debug, and optimize code. "
                "Provide clear, efficient, and well-documented code snippets. "
                "When relevant, include explanations in concise bullet points. "
            )
        }]
        
    
        if isinstance(args.coder, str): 
            chat_history.append({"role": "user", "content": args.coder})
            await ask(client, chat_history)
        else: 
            await chat(client, chat_history)

    else:
        chat_history = [{
            "role": "system",
            "content": (
                f"You are {AI_NAME}, a highly intelligent and helpful AI assistant. "
                "Your primary goal is to provide accurate, clear, and concise responses. "
                "Adapt your answers based on user intent and provide step-by-step guidance when necessary. "
                "Keep responses informative and to the point."
            )
        }]

        if isinstance(args.ask, str): 
            chat_history.append({"role": "user", "content": args.ask})
            await ask(client, chat_history)
        else: 
            await chat(client, chat_history)
