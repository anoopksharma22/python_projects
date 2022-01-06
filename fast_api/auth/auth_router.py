from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from .oauth2 import create_access_token,authenticate_user
from configs.database import get_db
from users import model as user_model

router = APIRouter(
    tags=['auth']
)


@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(),db_session: Session = Depends(get_db)):
    # token = create_access_token()

    user = authenticate_user(db_session=db_session,email=request.username,password=request.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    token = create_access_token(data={'sub':user.email})
    
    return {
       'access_token': token,
       'token_type': 'bearer',
       'user': user
    }