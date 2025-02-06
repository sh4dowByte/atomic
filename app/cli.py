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
    parser.add_argument("-a", "--ask", type=str, help="Ask a question.")
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

    if args.ask:
        os_name = platform.system()
        chat_history = [{"role": "system", "content": f"You are as terminal helper, response with terminal command. Your operating system is {os_name}."}]
        print(chat_history)
        chat_history.append({"role": "user", "content": args.ask})
        await ask(client, chat_history)
    else:
        chat_history = [{"role": "system", "content": f"You are {AI_NAME}, a helpful assistant."}]
        await chat(client, chat_history)
