import os
import logging
import sys
from dotenv import load_dotenv

load_dotenv() 
ENVIRONMENT = os.environ.get("SUMMARISER_ENVIRONMENT", "staging").lower()
LOG_TYPE = os.environ.get("SUMMARISER_LOG_TYPE", "INFO").upper()

# Define logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = getattr(logging, LOG_TYPE, logging.INFO)

# Create logs directory if local
if ENVIRONMENT == "local":
    os.makedirs("./logs", exist_ok=True)
    LOG_FILE = "./logs/local.log"
    handlers = [
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
else:
    handlers = [logging.StreamHandler(sys.stdout)]

# Configure root logger
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=handlers
)

# Function to get logger for each module
def get_logger(name: str):
    return logging.getLogger(name)
