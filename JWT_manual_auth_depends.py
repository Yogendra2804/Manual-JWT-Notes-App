from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials 
from fastapi import Depends , HTTPException
from JWT_manul_auth_utils import verify_user_token
from Logs.zlogger import logger

oauth_schema = HTTPBearer()

def get_current_user(token : HTTPAuthorizationCredentials =  Depends(oauth_schema)):
    
    logger.info("Getting current user. !")
    
    token = token.credentials
    userMail = verify_user_token(token) 

    if not userMail:
        raise HTTPException(status_code=401 , detail="Unauthorized")
    
    return userMail