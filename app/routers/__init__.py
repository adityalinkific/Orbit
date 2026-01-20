from fastapi import APIRouter

from app.modules.auth.auth_routers import router

api_router = APIRouter(prefix= "/api/v1")


api_router.include_router(router)