import asyncio
from app.cli import parse_arguments, handle_cli
from app.utils import signal_handler

def main_entry():
    """Main entry point for the application."""
    args = parse_arguments()
    asyncio.run(handle_cli(args))

if __name__ == "__main__":
    main_entry()