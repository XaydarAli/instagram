from fastapi import APIRouter,status,Depends,HTTPException
from werkzeug.datastructures import Authorization

from database import ENGINE,Session
from models import User
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from schemas.auth_router import Login,ResetPassword,Register
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
session=Session(bind=ENGINE)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.get("/")
async def auth_page(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        return {"message": "Welcome to Auth page"}
    except Exception as e:
        return {"message": "your token is invalid or expired"}

@auth_router.post("/register")
async def register_user(user: Register):
    check_user=session.query(User).filter(User.username==user.username).first()
    if check_user is None:
        new_user=User(
            username=user.username,
            email=user.email,
            password=generate_password_hash(user.password)

        )
        session.add(new_user)
        session.commit()
        data={
            "success": True,
             "code": 200,
            "message": "User registered successfully"
        }
        return jsonable_encoder(data)

    return jsonable_encoder(
        {   "success":False,
            "code":400,
            "message": "Username already registered"
        }
    )

@auth_router.post("/login")
async def login_user(user:Login,Authorize: AuthJWT = Depends()):
    check_user=session.query(User).filter(User.username==user.username).first()
    if check_user:
        if check_password_hash(check_user.password,user.password):
            access_token=Authorize.create_access_token(subject=user.username,expires_time=datetime.timedelta(minutes=10))
            refresh_token=Authorize.create_refresh_token(subject=user.username,expires_time=datetime.timedelta(days=7))


            data={
                "message":"Login successfully",
                "access_token":access_token,
                "refresh_token":refresh_token,
            }



            return jsonable_encoder(data)

        return jsonable_encoder({
            "success": False,
            "code": 400,
            "message": "password is incorrect"
        })

    return jsonable_encoder({
        "success": False,
        "code": 404,
        "message": "Login failed ,user is not found"
    })



@auth_router.post("/reset-password")
async def reset_password(user: ResetPassword,Authorize: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
        if user.password==user.confirm_password:
            current_user=session.query(User).filter(User.username==Authorize.get_jwt_subject()).first()
            if current_user:
                current_user.password=generate_password_hash(user.password)
                session.add(current_user)
                session.commit()
                data={
                    "success": True,
                    "code": 200,
                    "message": "Password reset successfully"
                }
                return jsonable_encoder(data)
            return jsonable_encoder({
                "message":"user not found "
            })
        return jsonable_encoder({
            "message":"password is incorrect"
        })

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")















































