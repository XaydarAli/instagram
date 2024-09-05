from fastapi import FastAPI, status, Depends, APIRouter,HTTPException
from database import ENGINE,Session
from models import  User,Post
from fastapi_jwt_auth import AuthJWT
from schemas.post_router import PostCreateModel,PostUpdateModel
from fastapi.encoders import jsonable_encoder

session=Session(bind=ENGINE)

post_router = APIRouter(prefix="/posts",tags=["posts"])

@post_router.get("/")
async def get_posts(Authorization:AuthJWT=Depends()):
    try:
        Authorization.jwt_required()
        check_user=session.query(User).filter(User.username==Authorization.get_jwt_subject()).first()
        if check_user:
            posts=session.query(Post).filter(Post.user==check_user).all()

            data={

                "success":True,
                "code":200,
                "messages":f"Posts by {check_user.username}",
                "posts":posts
            }

            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")




@post_router.post("/")
async def create_post(post: PostCreateModel,Authorization:AuthJWT=Depends()):
    try:
        Authorization.jwt_required()
        check_user=session.query(User).filter(User.username==Authorization.get_jwt_subject()).first()
        if check_user:
            new_post=Post(
                caption=post.caption,
                user_id=check_user.id,
                image_path=post.image_path
            )
            session.add(new_post)
            session.commit()


            data={
                "success":True,
                "code":200,
                "messages":f"Post created by {Authorization.get_jwt_subject()}"
            }
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")










@post_router.get('/{id}')
async def post_detail(id: str,Authorization:AuthJWT=Depends()):
    try:
        Authorization.jwt_required()
        check_user=session.query(User).filter(User.username==Authorization.get_jwt_subject()).first()
        if check_user:
            post = session.query(Post).filter(Post.id == id).first()

            post = session.query(Post).filter(Post.id == id).first()
            if post is not None:
                context = {
                    "id": post.id,
                    "caption": post.caption,
                    "image_path": post.image_path,
                    "user_id": post.user_id,
                    "created_at": post.created_at
                }
                return jsonable_encoder(context)

            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post is not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")





@post_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: str,Authorization:AuthJWT=Depends()):
    try:
        Authorization.jwt_required()
        check_user=session.query(User).filter(User.username==Authorization.get_jwt_subject()).first()
        if check_user:

            post = session.query(Post).filter(Post.id == id).first()
            if post:
                session.delete(post)
                session.commit()
                data = {
                    "code": 200,
                    "message": f"Post with  {id} is deleted successfully ",
                }
                return jsonable_encoder(data)

            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this post is not found")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")






@post_router.put('/{id}')
async def update_post(id: str, data: PostUpdateModel,Authorization:AuthJWT=Depends()):
    try:
        Authorization.jwt_required()
        check_user=session.query(User).filter(User.username==Authorization.get_jwt_subject()).first()
        if check_user:

            post = session.query(Post).filter(Post.id == id).first()
            if post:
                for key, value in data.dict(exclude_unset=True).items():
                    setattr(post, key, value)
                session.commit()
                data = {
                    "code": 200,
                    "message": "Post IS UPDATED succesfully"
                }
                return jsonable_encoder(data)

            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this post is not found")
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found")









