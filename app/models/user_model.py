from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    nickname: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    nickname: str
    email: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str | None = None
    nickname: str | None = None
    email: str | None = None
    

