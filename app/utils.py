import signal
from rich.console import Console
from app.config import AI_NAME

console = Console()

def signal_handler(sig, frame):
    """Handles SIGINT (Ctrl+C) to gracefully exit."""
    console.print(f"\n[bold cyan]{AI_NAME}:[/] Goodbye! 👋\n")
    raise SystemExit(0)

# Bind signal handler for keyboard interrupt
signal.signal(signal.SIGINT, signal_handler)
