import logging
from app.config import LOGS_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(LOGS_DIR / 'app.log')),
        logging.StreamHandler()  # also print to console
    ]
)

logger = logging.getLogger(__name__)


