from sqlalchemy.orm import sessionmaker , base , DeclarativeBase
from sqlalchemy import create_engine 
from Logs.zlogger import logger

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "database1.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False}
)
logger.info("Engine created successfully. !")

class Base(DeclarativeBase):
    pass
logger.info("Base class created successfully. !")

Session = sessionmaker(bind = engine)
session = Session()
logger.info("Session created successfully. !")