import asyncio
import os
import signal
import argparse
from openai import AsyncOpenAI
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live

# Pastikan .env tersedia
if not os.path.exists('.env'):
    with open('env.example', 'r') as f:
        with open('.env', 'w') as g:
            g.writelines(f.readlines())

# Load environment variables
load_dotenv()

AI_NAME = "Jarvis"
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

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

async def ask(client):
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

async def chat(client):
    """Interactive chat session with AI."""
    global MODEL_NAME
    console.print(f"[bold cyan]{AI_NAME} ready![/] Type [bold red]exit[/] to quit. Type [bold blue]model[/] to change model.\n")
    
    while True:
        user_input = Prompt.ask("[bold yellow]You[/]")
        if user_input.lower() == "exit":
            console.print(f"\n[bold cyan]{AI_NAME}:[/] Goodbye! 👋\n")
            break
        if not user_input.strip():
            continue

        chat_history.append({"role": "user", "content": user_input})

        console.print(f"\n[bold cyan]{AI_NAME}:[/]")
        await ask(client)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Atomic - Advanced Terminal Operation & Machine Intelligent Commander."
    )
    parser.add_argument("-a", "--ask", type=str, help="Ask a question.")
    parser.add_argument("--API_KEY", type=str, help="Change API key (default: hidden)")
    parser.add_argument("--BASE_URL", type=str, help="Change Base Url (default: "+BASE_URL+")")
    parser.add_argument("--MODEL", type=str, help="Change Model Name (default: "+MODEL_NAME+")")
   
    return parser.parse_args()

async def main():
    """Main function to handle both CLI and interactive chat."""
    args = parse_arguments()

    if args.API_KEY:
        set_key(dotenv_path='.env', key_to_set='API_KEY', value_to_set=args.API_KEY)
        os.environ["API_KEY"] = args.API_KEY
    if args.BASE_URL:
        set_key(dotenv_path='.env', key_to_set='BASE_URL', value_to_set=args.BASE_URL)
        os.environ["BASE_URL"] = args.BASE_URL
    if args.MODEL:
        set_key(dotenv_path='.env', key_to_set='MODEL_NAME', value_to_set=args.MODEL)
        os.environ["MODEL_NAME"] = args.MODEL
    
    load_dotenv(override=True)  # Reload environment variables

    # Inisialisasi client dengan API_KEY yang terbaru
    client = AsyncOpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))

    if args.ask:
        chat_history.append({"role": "system", "content": f"You are a command shell ({os.name}), provide terminal commands."})
        chat_history.append({"role": "user", "content": args.ask})
        await ask(client)
    else:
        chat_history.append({"role": "system", "content": f"You are {AI_NAME}, a helpful assistant."})
        await chat(client)

def main_entry():
    asyncio.run(main())

if __name__ == "__main__":
    main_entry()