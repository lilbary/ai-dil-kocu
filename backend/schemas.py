from pydantic import BaseModel

# Kullanıcıdan kayıt olurken isteyeceğimiz veriler
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True