import os
from dotenv import load_dotenv, set_key

# Load environment variables
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

AI_NAME = "Atomic"
BASE_URL = os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
API_KEY = os.getenv("API_KEY", "YOUR_API_KEY")

def update_env_variable(key: str, value: str):
    """Update environment variable and reload .env."""
    set_key(env_path, key_to_set=key, value_to_set=value)
    os.environ[key] = value
    load_dotenv(env_path, override=True)
