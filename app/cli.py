import argparse
import importlib
from pathlib import Path
from openai import AsyncOpenAI
from app.config import update_env_variable, API_KEY, BASE_URL, MODEL_NAME

# Define the path to the 'prompt' directory
PROMPT_DIR = Path(__file__).parent / "../prompt"

# Dynamically load all modules from the 'prompt' directory that contain a 'prompt' function
handlers = {}
for file in PROMPT_DIR.glob("*.py"):
    if file.stem == "__init__":
        continue  # Skip '__init__.py'

    module = importlib.import_module(f"prompt.{file.stem}")
    if hasattr(module, "prompt"):
        handlers[file.stem] = module.prompt  # Store the 'prompt' function from each module


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Atomic - Advanced Terminal Operation & Machine Intelligent Commander."
    )

    # Define command-line options for different prompt handlers
    parser.add_argument("-t", "--terminal", nargs="?", const=True, type=str, help="Ask a terminal-related question.")
    parser.add_argument("-c", "--coder", nargs="?", const=True, type=str, help="Ask a programming-related question.")
    parser.add_argument("-a", "--ask", nargs="?", const=True, type=str, help="Ask a general question.")

    # Define command-line options for API configuration
    parser.add_argument("--API_KEY", type=str, help=f"Change API key (default: {API_KEY})")
    parser.add_argument("--BASE_URL", type=str, help=f"Change Base URL (default: {BASE_URL})")
    parser.add_argument("--MODEL", type=str, help=f"Change Model Name (default: {MODEL_NAME})")

    return parser.parse_args()


async def handle_cli(args):
    """Handle CLI-based AI interactions."""
    
    client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

    # Update API configurations if provided via command-line arguments
    if args.API_KEY:
        update_env_variable("API_KEY", args.API_KEY)
    if args.BASE_URL:
        update_env_variable("BASE_URL", args.BASE_URL)
    if args.MODEL:
        update_env_variable("MODEL_NAME", args.MODEL)

    # Execute the corresponding handler based on the provided argument
    for key, handler in handlers.items():
        arg_value = getattr(args, key, None)
        if arg_value:
            await handler(client, arg_value)
            break
    else:
        # Default to 'assistant' if no specific argument is provided
        await handlers["assistant"](client, args.ask)
