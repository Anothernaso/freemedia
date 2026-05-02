from fastapi import APIRouter

from . import submit_post

router = APIRouter(prefix="/form", tags=["form"])
router.include_router(submit_post.router)
