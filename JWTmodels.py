from sqlalchemy.orm import Mapped , mapped_column 
from sqlalchemy import Integer , String , DateTime , ForeignKey
from sqlalchemy.sql import func
from engine import Base , engine
from datetime import datetime 

class Users(Base):

    __tablename__ = "user" 

    id : Mapped[int] = mapped_column(Integer , primary_key=True , nullable=False)
    username : Mapped[str] = mapped_column(String , nullable= False)
    mail : Mapped[str] = mapped_column(String , nullable= False , unique=True)
    hashed_password : Mapped[str] = mapped_column(String , nullable=False)


class UserNotes(Base) :
    __tablename__ = "UserNotes"

    id : Mapped[int] = mapped_column(Integer , primary_key= True , nullable= False)
    title : Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    mail: Mapped[str] = mapped_column(String, ForeignKey("user.mail"), nullable=False)
    content : Mapped[str] = mapped_column(String)


Base.metadata.create_all(engine)
