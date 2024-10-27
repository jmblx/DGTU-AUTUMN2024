from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from infrastructure.db_models.user.models import User
from infrastructure.db_models.achievement.models import Achievement, user_achievement
from infrastructure.db_models.reward.models import Reward, user_reward
from infrastructure.db_models.event.models import Event, UserEvent

async def seed_user_with_data(session: AsyncSession):
    user_data = {
        "id": "cTqj1BzxfWS9gQGgn033WIcmn4e2",
        "name": "Eco Warrior",
        "first_name": "Egor",
        "last_name": "Ybica",
        "email": "zhora.zhilin.06@mail.ru",
    }
    await session.execute(insert(User).values(user_data))

    user_achievements_data = [
        {"user_id": user_data["id"], "achievement_id": 1, "progress": 3},
        {"user_id": user_data["id"], "achievement_id": 2, "progress": 10},
        {"user_id": user_data["id"], "achievement_id": 3, "progress": 20},
    ]
    await session.execute(insert(user_achievement).values(user_achievements_data))

    # Связываем награды с пользователем через user_reward с прогрессом
    user_rewards_data = [
        {"user_id": user_data["id"], "reward_id": 1, "amount": 10, "is_used": False, "received_date": datetime.now()},
        {"user_id": user_data["id"], "reward_id": 2, "amount": 50, "is_used": False, "received_date": datetime.now()},
        {"user_id": user_data["id"], "reward_id": 6, "amount": 1, "is_used": False, "received_date": datetime.now()},
    ]
    await session.execute(insert(user_reward).values(user_rewards_data))

    # Применяем изменения
    await session.commit()
