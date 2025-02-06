import readline
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from app.config import AI_NAME, MODEL_NAME

# Rich console setup
console = Console(force_interactive=True)

async def ask(client, chat_history):
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
    
    return bot_response

async def chat(client, chat_history):
    """Interactive chat session with AI."""
    console.print(f"[bold cyan]{AI_NAME} ready![/] Type [bold red]exit[/] to quit.\n")
    
    while True:
        readline.parse_and_bind("tab: complete")
        user_input = input("\033[1;33mYou: \033[0m")
        if user_input.lower() == "exit":
            console.print(f"\n[bold cyan]{AI_NAME}:[/] Goodbye! 👋\n")
            break
        if not user_input.strip():
            continue

        chat_history.append({"role": "user", "content": user_input})
        console.print(f"\n[bold cyan]{AI_NAME}:[/]")
        await ask(client, chat_history)
