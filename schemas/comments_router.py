from pydantic import BaseModel
from typing import List, Optional

class CommentModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    content: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "id": 1,
            "post_id": 1,
            "user_id": 1,

        }

class CommentCreateModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    content: Optional[str]


class CommentUpdateModel(BaseModel):
    id: Optional[int]
    post_id: Optional[int]
    user_id: Optional[int]
    content: Optional[str]

