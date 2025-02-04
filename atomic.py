import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live

console = Console(force_interactive=True)

# Muat variabel lingkungan dari .env
load_dotenv()

client = AsyncOpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

ai_name = 'Jarvis'

chat_history = [
    {"role": "system", "content": "You are "+ai_name+" helpful assistant."},
]

model_name = "llama-3.1-8b-instant"

async def chat():
    global model_name
    console.print("[bold cyan]🤖 {} siap![/] Ketik [bold red]exit[/] untuk keluar. Ketik [bold blue]model[/] untuk mengganti model.\n".format(ai_name))

    while True:
        user_input = Prompt.ask("[bold yellow]You[/]")
        if user_input.lower() == "exit":
            console.print("\n[bold red]{}:[/] Goodbye! 👋\n".format(ai_name))
            break
        elif user_input.lower() == "model":
            model_name = Prompt.ask("Masukkan nama model: ")
            console.print(f"[bold blue]Model changed to {model_name}[/]\n")
            continue
        if not user_input.strip():
            continue

        chat_history.append({"role": "user", "content": user_input})

        stream = await client.chat.completions.create(
            model=model_name,
            messages=chat_history,
            stream=True
        )

        console.print("\n[bold cyan]{}:[/]".format(ai_name))

        bot_response = ""

        with Live("", console=console, refresh_per_second=10) as live:
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    bot_response += chunk.choices[0].delta.content
                    live.update(Markdown(bot_response))
        
        console.print("\n")
        chat_history.append({"role": "assistant", "content": bot_response})

asyncio.run(chat())
