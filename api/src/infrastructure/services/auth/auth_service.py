class AuthorizationService:
    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def authorize(self) -> bool:
        # Реализуйте свою логику авторизации здесь
        # Например, проверка токена
        return self.auth_token == "valid_token"
