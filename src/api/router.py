from fastapi import APIRouter

from api.v1 import auth, post, comment

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth.router)
v1_router.include_router(post.router)
v1_router.include_router(comment.router)

router = APIRouter(prefix="/api")
router.include_router(v1_router)
