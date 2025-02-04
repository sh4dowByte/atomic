import asyncio
import os
import signal
import argparse
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live

# Load environment variables
load_dotenv()

# Constants
AI_NAME = "Jarvis"
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# Initialize OpenAI client
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

# Rich console setup
console = Console(force_interactive=True)

# Chat history storage
chat_history = []

def signal_handler(sig, frame):
    """Handles SIGINT (Ctrl+C) to gracefully exit."""
    console.print(f"\n[bold cyan]{AI_NAME}:[/] Goodbye! 👋\n")
    raise SystemExit(0)

# Bind signal handler for keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)

async def ask():
    """Send user input to the AI model and stream the response."""
    stream = await client.chat.completions.create(
        model=MODEL_NAME,
        messages=chat_history,
        stream=True
    )
    
    bot_response = ""
    with Live("", console=console, refresh_per_second=10) as live:
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                bot_response += chunk.choices[0].delta.content
                live.update(Markdown(bot_response))
    console.print("\n")

async def chat():
    """Interactive chat session with AI."""
    global MODEL_NAME
    console.print(f"[bold cyan]{AI_NAME} ready![/] Type [bold red]exit[/] to quit. Type [bold blue]model[/] to change model.\n")
    
    while True:
        user_input = Prompt.ask("[bold yellow]You[/]")
        if user_input.lower() == "exit":
            console.print(f"\n[bold cyan]{AI_NAME}:[/] Goodbye! 👋\n")
            break
        elif user_input.lower() == "model":
            MODEL_NAME = Prompt.ask("Enter model name: ")
            console.print(f"[bold blue]Model changed to {MODEL_NAME}[/]\n")
            continue
        if not user_input.strip():
            continue

        chat_history.append({"role": "user", "content": user_input})

        console.print(f"\n[bold cyan]{AI_NAME}:[/]")
        await ask()

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Atomic - Advanced Terminal Operation & Machine Intelligent Commander."
    )
    parser.add_argument("-a", "--ask", type=str, help="Ask a question.")
    return parser.parse_args()

async def main():
    """Main function to handle both CLI and interactive chat."""
    args = parse_arguments()
    if args.ask:
        chat_history.append({"role": "system", "content": f"You are a command shell ({os.name}), provide terminal commands."})
        chat_history.append({"role": "user", "content": args.ask})
        await ask()
    else:
        chat_history.append({"role": "system", "content": f"You are {AI_NAME}, a helpful assistant."})
        await chat()

if __name__ == "__main__":
    asyncio.run(main())