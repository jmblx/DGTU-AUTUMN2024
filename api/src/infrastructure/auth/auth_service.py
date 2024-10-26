from fastapi import HTTPException, Depends
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth, credentials

from config import FirebaseConfig

cred = credentials.Certificate(FirebaseConfig.from_env().rd_uri)
firebase_admin.initialize_app(cred)


def get_user_info(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_email = decoded_token.get("email")
        user_uid = decoded_token.get("uid")
        # Вы можете извлечь и другие доступные данные
        return {"email": user_email, "uid": user_uid}
    except Exception as e:
        print("Error verifying token:", e)
        return None


class UserEmail(BaseModel):
    email: str


class TokenValidationService:
    @staticmethod
    async def validate_token(id_token: str) -> dict | None:
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_email = decoded_token.get("email")
            user_uid = decoded_token.get("uid")
            return {"email": user_email, "uid": user_uid}
        except Exception as e:
            print("Error verifying token:", e)
            return None
