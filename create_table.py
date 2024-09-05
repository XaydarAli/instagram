from models import User, Post, Comments, Likes, Followers, PostTags, Messages
from database import Base, ENGINE
Base.metadata.create_all(bind=ENGINE)