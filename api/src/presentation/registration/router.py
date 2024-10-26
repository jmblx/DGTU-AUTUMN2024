from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.services.user.user_service_interface import UserServiceInterface
from presentation.registration.schemas import UserRegistration, UserLogin

router = APIRouter(route_class=DishkaRoute, tags=["reg", "auth"])


@router.post("/user")
async def registration(data: UserRegistration, user_service: FromDishka[UserServiceInterface], login_data: FromDishka[UserLogin]):
    combined_data = {**data.dict(), **login_data.dict()}
    return await user_service.create(combined_data)
