from fastapi import APIRouter, status, Depends
from database import Session, ENGINE
from models import Comments, User
from schemas.comments_router import CommentCreateModel,CommentUpdateModel,CommentModel
from http.client import HTTPException
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

comment_router = APIRouter(prefix="/comments", tags=["Comments"])
session = Session(bind=ENGINE)


@comment_router.get("/")
async def comments():
    comments = session.query(Comments).all()
    return comments


@comment_router.post("/")
async def comment_create(comment: CommentCreateModel):
    check_id = session.query(Comments).filter(Comments.id == comment.id).scalar()
    if check_id is not None:
        return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Comment id already exists")

    new_comment = Comments(
       id=comment.id,
        post_id=comment.post_id,
        user_id=comment.user_id,
        content=comment.content,
    )
    session.add(new_comment)
    session.commit()
    return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Comment is created Successfully")


@comment_router.get("/comment/{id}")
async def comment_detail(id: int):
    comment = session.query(Comments).filter(Comments.id == id).first()
    if comment is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment is not found")

    data = {
        "id": comment.id,
        "post_id": comment.post_id,
        "user_id": comment.user_id,
        "content": comment.content,
    }
    return jsonable_encoder(data)


@comment_router.put('/comment/{id}')
async def update_comment(id: int, data: CommentUpdateModel):
    comment = session.query(Comments).filter(Comments.id == id).first()
    if comment:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(comment, key, value)
        session.commit()
        data = {
            "code": 200,
            "message": "Update comment",
            "object": {
                "id": comment.id,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "content": comment.content,
            }
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comment is not found")


@comment_router.delete("/comment/{id}")
async def comment_delete(id: int):
    comment = session.query(Comments).filter(Comments.id == id).first()
    if comment is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment is not found")

    session.delete(comment)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
