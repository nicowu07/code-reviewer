from pathlib import Path
from fastapi.templating import Jinja2Templates
import os

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
LOGS_DIR = BASE_DIR / "logs"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CODE_LIMIT = 100000
