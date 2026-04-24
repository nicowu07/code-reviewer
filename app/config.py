from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
LOGS_DIR = BASE_DIR / "logs"
