from engine import session 
from passlib.context import CryptContext
from JWTmodels import Users
from sqlalchemy import select
from Token import ALGORITH , SECRET_KEY 
from fastapi import HTTPException
from Logs.zlogger import logger

import base64
import json



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

def verfiy_user(password : str , entered_mail ) -> bool:
    
    user = session.scalars(
        select(Users).where(Users.mail == entered_mail)
    ).first()


    if user == None:
        logger.error("User not found. !")
        return False

    return password_context.verify(password , user.hashed_password) 

def verify_user_token(token: str):
    try:
        logger.info("Verifying user token. !")
        header, payload, signature = token.split(".")

        from Token import make_signature
        import hmac
        import datetime

        expected_signature = make_signature(header, payload)
        if not hmac.compare_digest(signature, expected_signature):
            logger.error("Signature verification failed. !")
            return None

        decoded_payload = json.loads(
            base64.urlsafe_b64decode(payload + "==")
        )
        
        exp = decoded_payload.get("exp")
        if exp and exp < datetime.datetime.utcnow().timestamp():
            logger.error("Token has expired. !")
            return None

        logger.info("User token verified. !")
        return decoded_payload.get("sub")

    except Exception as e:
        logger.error("Error verifying user token. !")
        print("ERROR:", e)
        return None


def is_email_available(entered_mail ) -> bool:
    
    try : 
        logger.info("Checking if email is available. !")
        user = session.scalars(
            select(Users).where(Users.mail == entered_mail)
        ).first()

        if user == None:
            logger.info("Email is available. !")
            return True

        logger.info("Email is not available. !")
        return False
    
    except:
        logger.error("Error checking if email is available. !")
        return False
    

def deleting_user(entered_mail) -> bool:
    try:
        user = session.scalars(
            select(Users).where(Users.mail == entered_mail)
        ).first()

        if not user:
            logger.error("User not found. !")
            return False

        session.delete(user)
        session.commit()

        logger.info("User deleted successfully. !")
        return True
    
    except Exception as e:
        logger.error(f"Error deleting user: {e} !")
        return False