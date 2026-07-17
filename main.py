import hashlib
from fastapi import FastAPI , Depends, HTTPException
from JWT_manual_schema import user_sent_data_signup , user_sent_data_login , user_new_note , user_delete_note, user_delete_account
from JWT_manul_auth_utils import verfiy_user  , verify_user_token , is_email_available , deleting_user ,password_context
from Token import generate_token
from engine import session
from JWTmodels import Users , UserNotes
from JWT_manual_auth_depends import get_current_user
from sqlalchemy import select


from jose import jwt 
from datetime import datetime , timedelta
from Token import SECRET_KEY , ALGORITH


from Logs.zlogger import logger
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so the frontend can connect from other origins (like Live Server or local files)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UI_FILE = Path(__file__).parent / "index.html"


@app.get("/")
def serve_ui():
    return FileResponse(UI_FILE)

@app.get("/logo+notes_app.png")
def serve_logo():
    return FileResponse(Path(__file__).parent / "logo+notes_app.png")

@app.get("/brand_icon.png")
def serve_brand_icon():
    return FileResponse(Path(__file__).parent / "brand_icon.png")

@app.post("/signup")
def signup_user(user_data : user_sent_data_signup):
    
    logger.info("Signing up user. !")
    
    if not is_email_available(user_data.mail): 
        raise HTTPException(status_code=409, detail="mail already taken !")
    
    logger.info("User email is available. !")
    
    new_user = Users(
        username=user_data.username,
        mail=user_data.mail,
        hashed_password=password_context.hash(user_data.password)
    )

    session.add(new_user)
    session.commit()

    logger.info("User signed up successfully. !")
    
    # NO need to generate token here cause 
   
    #     👉 Real apps:
    # Signup → just create user
    # Login → issue token
   
    # msg = generate_token(user_data.mail)

    return{
        "msg" : f"User Made"
    }

@app.post("/login")
def login_user(user_data : user_sent_data_login):

    logger.info("Logging in user. !")
    
    if not verfiy_user(user_data.password, user_data.mail):
        raise HTTPException(status_code=401, detail="Invaild Credintials. Thankyiu but try again. !")
    
    token = generate_token(user_data.mail)

    logger.info("User logged in successfully. !")
    
    # payload = {
    #     "sub" : user_data.mail , 
    #     "exp" : datetime.utcnow() + timedelta(minutes=5)
    # }
    # token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITH)
    
    return{
        "access_token": token,
        "token_type": "bearer"
        # "msg" : f"User Made\tBelow is the Token -> \n{msg}"
    }


@app.delete("/delete")
def delete_user(data : user_delete_account , userMail =  Depends(get_current_user)):

    logger.info("Deleting user. !")
    
    if not verfiy_user(data.password , userMail):
        raise HTTPException(status_code=401, detail="wrong password , Try again -_- ")

    if deleting_user(userMail):
        logger.info("User deleted successfully. !")
        return{
            "msg" : f"User deleted Succesfully. ! Come back soon pls."
        }
    
    logger.error("User not deleted. !")
    
    raise HTTPException(status_code=400, detail="Could not delete user for some reason, try again later . ")       


@app.get("/get_user_notes")
def get_notes(userMail : str =  Depends(get_current_user)):

    logger.info("Getting notes. !")
    
    notes = session.scalars(select(UserNotes).where(userMail == UserNotes.mail)).all()

    if not notes:
        logger.info("No notes found. !")
        return {
            "msg" : "No note has been created yet. ! Try making some maybe <__> "
        }
    
    logger.info("Notes found. !")
    
    return [
        {
            "id" : note.id , 
            "title" : note.title ,
            "content" : note.content
        }
        for note in notes
    ]

@app.post("/writeNote")
def writeNote(data : user_new_note , userMail : str = Depends(get_current_user)):

    logger.info("Writing note. !")
    
    try:
        note = UserNotes(title= data.title , mail= userMail , content= data.content)

        session.add(note)
        session.commit()

        logger.info("Note added successfully. !")
        
        return {
            "msg" : "Note added. "
        }
    
    except :
        logger.error("Note not added. !")
        raise HTTPException(status_code=500, detail="Was not able to add note. Sry")

@app.delete("/deleteNote")
def deleteNote(data : user_delete_note , userMail : str = Depends(get_current_user)):

    logger.info("Deleting note. !")
    
    try:
        note = session.scalars(select(UserNotes).where(UserNotes.title == data.title , UserNotes.mail == userMail)).first()
        if note is None:
            logger.error("Note not found. !")
            raise HTTPException(status_code=404, detail="Note not found or not yours")

        session.delete(note)
        session.commit()

        logger.info("Note deleted successfully. !")
        
        return {"msg": "Note deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting note: {e} !")
        raise HTTPException(status_code=500, detail="Unable to delete note")

