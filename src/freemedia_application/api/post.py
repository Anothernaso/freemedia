from fastapi import APIRouter, Depends
from sqlmodel import Session

from freemedia_database import get_session
from freemedia_database.media_post import MediaPost

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/api/post")
def create_post(post: MediaPost, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)

    return post
