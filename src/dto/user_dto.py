from pydantic import BaseModel

class RegisterDTO(BaseModel):
    UserName: str
    PhoneNumber: str
    Address: str
    Email: str
    Password: str

class LoginDTO(BaseModel):
    Email: str
    Password: str

class UserDTO(BaseModel):
    UserID: int
    UserName: str
    PhoneNumber: str
    Address: str
    Email: str
    Password: str
    RoleID: int