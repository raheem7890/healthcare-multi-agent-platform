from fastapi import APIRouter

from app.api import routes_appointments, routes_chat, routes_memory, routes_profiles


api_router = APIRouter()
api_router.include_router(routes_profiles.router)
api_router.include_router(routes_chat.router)
api_router.include_router(routes_appointments.router)
api_router.include_router(routes_memory.router)

