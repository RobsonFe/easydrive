from typing import TypedDict


class UserDataType(TypedDict):
    id: int | None 
    username: str
    email: str
    password: str
    avatar: str | None
    
class SiginDataType(TypedDict):
    email: str
    password: str