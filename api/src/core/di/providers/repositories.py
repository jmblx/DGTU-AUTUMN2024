from dishka import Provider, Scope, provide

from domain.repositories.event.repo import EventRepository
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.event.event_repo_impl import EventRepositoryImpl
from infrastructure.repositories.user.user_repo_impl import UserRepositoryImpl


class RepositoriesProvider(Provider):
    user_repo = provide(
        UserRepositoryImpl, scope=Scope.REQUEST, provides=UserRepository
    )
    event_repo = provide(
        EventRepositoryImpl, scope=Scope.REQUEST, provides=EventRepository
    )
