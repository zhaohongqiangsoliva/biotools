from fastapi import APIRouter
from .endpoints import *


v1 = APIRouter(prefix="/job")

v1.include_router(login)
v1.include_router(user)
v1.include_router(jobs)