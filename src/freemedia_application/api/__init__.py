from fastapi import APIRouter

from . import post

router = APIRouter(prefix="/api", tags=["api"])
router.include_router(post.router)
