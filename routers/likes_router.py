from fastapi import APIRouter, status, Depends
from database import Session, ENGINE
from models import Likes, User
from schemas.likes_router import LikeUpdateModel,LikesCreateModel,LikesModel
from http.client import HTTPException
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


like_router = APIRouter(prefix="/like", tags=["Likes"])
session = Session(bind=ENGINE)


@like_router.get("/")
async def likes():
    likes = session.query(Likes).all()
    return likes


@like_router.post("/create-likes")
async def like_create(like: LikesCreateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        check_user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
        if check_user:
            new_like = Likes(
                id=like.id,
                post_id=like.post_id,
                user_id=like.user_id,
                comment_id=like.comment_id,

            )
            session.add(new_like)
            session.commit()
            data = {
                "success": True,
                "code": 201,
                "message": "Like is created successfully"
            }
            return jsonable_encoder(data)
        return {"success": False, "code": 400, "message": "Bad Request"}
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token is invalid or expired")

@like_router.get("/like/{id}")
async def like_detail(id: int):
    like = session.query(Likes).filter(Likes.id == id).first()
    if like is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like is not found")

    data = {
        "id": like.id,
        "post_id": like.post_id,
        "user_id": like.user_id,
        "comment_id": like.comment_id,
    }
    return jsonable_encoder(data)


@like_router.put('/likes/{id}')
async def update_like(id: int, data: LikeUpdateModel):
    like = session.query(Likes).filter(Likes == id).first()
    if like:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(like, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Update comment",
            "object": {
                "id": like.id,
                "post_id": like.post_id,
                "user_id": like.user_id,
                "comment_id": like.comment_id,
            }
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Like is not found")


@like_router.delete("/like/{id}")
async def like_delete(id: int):
    like = session.query(Likes).filter(Likes.id == id).first()
    if like is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like is not found")

    session.delete(like)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)


