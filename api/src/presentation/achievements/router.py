from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, HTTPException

from domain.services.achievement.ach_service_interface import AchievementServiceInterface
from domain.services.event.event_service_interface import EventServiceInterface
from infrastructure.db_models.user.models import User
from presentation.achievements.schemas import ReadAch, ReadAchWithProgress
from presentation.events.schemas import EventRead
from presentation.rewards.shemas import RewardRead

router = APIRouter(tags=["achievements"], route_class=DishkaRoute)


@router.get("/achievements", response_model=list[ReadAchWithProgress])
async def get_user_achievements(
    achievement_service: FromDishka[AchievementServiceInterface],
    user: FromDishka[User]
) -> list[ReadAchWithProgress]:
    """
    Возвращает список достижений с прогрессом для текущего пользователя.
    """
    achievements = await achievement_service.get_user_achievements(user.id)
    return [
        ReadAchWithProgress(
            id=ach.id,
            title=ach.title,
            description=ach.description,
            file_path=ach.file_path,
            goal=ach.goal,
            progress=ach.progress,
            rewards=[
                RewardRead(
                    id=reward.id,
                    title=reward.title,
                    file_path=reward.file_path,
                    amount=reward.amount,
                ) for reward in ach.rewards_ach
            ]
        ) for ach in achievements
    ]

@router.get("/achievements/{achievement_id}", response_model=ReadAchWithProgress)
async def get_user_achievement(
    achievement_id: int,
    achievement_service: FromDishka[AchievementServiceInterface],
    user: FromDishka[User]
) -> ReadAchWithProgress:
    """
    Возвращает конкретное достижение с прогрессом для текущего пользователя.
    """
    achievement = await achievement_service.get_user_achievement_by_id(user.id, achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")

    return ReadAchWithProgress(
        id=achievement.id,
        title=achievement.title,
        description=achievement.description,
        file_path=achievement.file_path,
        goal=achievement.goal,
        progress=achievement.progress,
        rewards=[
            RewardRead(
                id=reward.id,
                title=reward.title,
                file_path=reward.file_path,
                amount=reward.amount,
            ) for reward in achievement.rewards_ach
        ]
    )
