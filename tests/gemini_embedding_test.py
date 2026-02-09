from google import genai
import os
from pathlib import Path
from dotenv import load_dotenv

"""
Test script to verify gemini embedding functionality.
"""

APP_ENV = os.getenv("APP_ENV", "dev")

# Define the path to the .env file relative to this config file's location.
# This file is in tests/, so we go up one level to project root
SERVICE_ROOT = Path(__file__).resolve().parents[1]
env_file_path = SERVICE_ROOT / f".env.{APP_ENV}"

# Load the .env file manually
print(f"Loading env file from: {env_file_path}")
load_dotenv(dotenv_path=env_file_path)

# Get the API key
google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")

# example usage provided by Google GenAI documentation
client = genai.Client(api_key=google_api_key)

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents= [
            "What is the meaning of life?",
            "What is the purpose of existence?",
            "How do I bake a cake?"
        ]
)

if result and result.embeddings:
    print(f"Embedding successful!")
    for embedding in result.embeddings:
        print(embedding)
