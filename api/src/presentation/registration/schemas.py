from pydantic import BaseModel, EmailStr


class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    address: str

class UserLogin(BaseModel):
    id: str
    email: EmailStr
