import logging
from math import log
import os

Logs_dir = os.path.dirname(__file__)

JWT_dir = os.path.dirname(Logs_dir)

logging_dir = os.path.join(JWT_dir , "Logs")

file_logger_dir = os.path.join(logging_dir , "app.log")

logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    filename=file_logger_dir,
    format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)