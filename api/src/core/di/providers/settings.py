from dishka import Provider, Scope, provide

from config import MinIOConfig, FirebaseConfig


class SettingsProvider(Provider):
    storage_settings = provide(
        lambda *args: MinIOConfig(), scope=Scope.APP, provides=MinIOConfig
    )
    #firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
