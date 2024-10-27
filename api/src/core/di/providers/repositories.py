from dishka import Provider, Scope, provide

from domain.repositories.achievement.repo import AchievementRepository
from domain.repositories.event.repo import EventRepository
from domain.repositories.reward.repo import RewardRepository
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.achievement.achievement_repo_impl import AchievementRepositoryImpl
from infrastructure.repositories.event.event_repo_impl import EventRepositoryImpl
from infrastructure.repositories.reward.reward_repo_impl import RewardRepositoryImpl
from infrastructure.repositories.user.user_repo_impl import UserRepositoryImpl


class RepositoriesProvider(Provider):
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )
    event_repo = provide(
        EventRepositoryImpl, scope=Scope.REQUEST, provides=EventRepository
    )
    achievement_repo = provide(AchievementRepositoryImpl, scope=Scope.REQUEST, provides=AchievementRepository)
    reward_repo = provide(RewardRepositoryImpl, scope=Scope.REQUEST, provides=RewardRepository)
