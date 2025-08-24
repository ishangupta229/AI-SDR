import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

# Database
DATABASE_URL = "sqlite:///./ai_sdr.db"

# AI Settings
MAX_TOKENS = 1000
TEMPERATURE = 0.7

# Email Settings
MAX_FOLLOW_UPS = 5
FOLLOW_UP_DAYS = [2, 5, 10, 15, 21]
