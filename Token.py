# Hey so ik the file name is crazze but you it's true i'll be trying that here so wise me luck. 

def generate_token(entered_mail):
    logger.info("Generating token. !")
    try:
        user = session.scalars(
            select(Users).where(Users.mail == entered_mail)
        ).first()

        if user == None:
            logger.error("User not found. !")
            return {"msg" : "fetching user from mail went wrong in toke.py"}
    except Exception as e:
        logger.error(f"Error fetching user: {e} !")
        return {"msg" : "fetching user from mail went wrong in toke.py"}
    
    try:
        header = encoded_make_header(make_header()) 
        payload = encoded_make_payload(make_payload(payload_data(user_id=user.id, mail=user.mail))) 
        signature = make_signature(header , payload)
        return f"{header}.{payload}.{signature}"
    except Exception as e:
        logger.error(f"Error generating token: {e} !")
        return {"msg" : "Error generating token. !"}

from pydantic import EmailStr , BaseModel
from datetime import datetime , timedelta
import hmac as HMAC
import hashlib
from BaseEncode64_CHATGPT import encoded_make_header , encoded_make_payload , base64url_encode
from engine import session 
from JWTmodels import Users 
from sqlalchemy import select
from Logs.zlogger import logger

ALGORITH = "HS256"
SECRET_KEY = "tHI_IS_my_first_secrate_key" 

#what are the things i need 
#what are the things i need 
#what are the things i need 
#what are the things i need 

#first I need a header -> 
def make_header():
    return {
        "alg": ALGORITH,
        "typ": "JWT"
        }

#header header hdeader 
#what do I need 
#what do I need 
#Yes I need a payload 

class payload_data(BaseModel):
    user_id : int 
    mail : EmailStr 



def make_payload(data : payload_data):
    #fuckass nigga payload is sent when logging in it does not have thast kind of data which the user is typing or trying to save. 



    return {
        "user_id" : data.user_id ,
        "sub" : data.mail , 
        "iat" : int(datetime.utcnow().timestamp()) ,
        "exp" : int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
    }


#ok 
#ok .. now we need to verify the credintials. 


# <--- One Thousand years later --->
# offf .. okie now the user is being verified and then the gen_token is being called .. payload is also ready .. 
#   and header is also ready .. now the hard part Signature .. 

def make_signature(encoded_header , encoded_payload):

    message = encoded_header + "." + encoded_payload

    signature = HMAC.new(SECRET_KEY.encode() , message.encode() , hashlib.sha256).digest()
    
    return base64url_encode(signature)


print(f"\n\nThe Token is: {generate_token("tester@gmail.com")}")