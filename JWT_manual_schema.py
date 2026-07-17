from pydantic import BaseModel , Field , EmailStr
from typing import Annotated 

class user_sent_data_signup(BaseModel):
    username : Annotated[str , Field(min_length= 6)] 
    mail : EmailStr
    password : str


class user_sent_data_login(BaseModel):
    mail : EmailStr
    password : str 


class user_new_note(BaseModel):
    title : str
    content : str


class user_delete_note(BaseModel):
    title : str


class user_delete_account(BaseModel):
    password : str