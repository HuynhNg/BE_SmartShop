from fastapi import APIRouter, Depends
from src.middlewares.verify_middleware import admin_verify, user_verify 
from src.api.users.users_controller import UsersController
from src.dto.user_dto import RegisterDTO
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/users", tags=["Users"])
users_ctl = UsersController()

@router.get("/", dependencies=[Depends(admin_verify)])
@cache(expire=300)
def get_all_users(Page: int = 1):
    return users_ctl.get_all_users(Page)

@router.get("/{id}", dependencies=[])
def get_user_byID(user_id: int, payload=Depends(user_verify)):
    return users_ctl.get_user_byID(user_id, payload)

@router.get("/email/{email}", dependencies=[])
def get_user_byEmail(email: str, payload=Depends(user_verify)):
    return users_ctl.get_user_byEmail(email, payload)

@router.put("/", dependencies=[])
def update_user(user: RegisterDTO, payload=Depends(user_verify)):
    return users_ctl.update_user(user, payload)
