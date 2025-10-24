from fastapi import APIRouter
from src.dto.user_dto import LoginDTO, RegisterDTO
from src.api.auth.auth_controller import AuthController

router = APIRouter(prefix="/authentication", tags=["authentication"])
auth_ctl = AuthController()

@router.post("/login")
def login(user: LoginDTO):
    return auth_ctl.login(user)

@router.post("/register")
def register(user: RegisterDTO):
    return auth_ctl.register(user)