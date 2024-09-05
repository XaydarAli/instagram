from fastapi import FastAPI
from routers.auth_router import auth_router
from routers.post_router import post_router
from fastapi_jwt_auth import AuthJWT
from schemas.auth_router import Settings
app=FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()
app.include_router(auth_router)
app.include_router(post_router)

@app.get("/")
async def root():
    return {"message": "Main Page"}
