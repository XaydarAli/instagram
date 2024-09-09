
from pydantic import BaseModel
from typing import Optional

class LikesModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    comment_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "post_id": 1,
            "user_id": 1,
            "comment_id": 1,
        }


class LikesCreateModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    comment_id: Optional[int]


class LikeUpdateModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    comment_id: Optional[int]
