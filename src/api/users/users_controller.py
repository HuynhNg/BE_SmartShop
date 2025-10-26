from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.api.users.users_service import UsersService
from src.dto.user_dto import RegisterDTO
import re

class UsersController():
    def get_all_users(self, Page: int):
        try:
            users_sv = UsersService()
            users = users_sv.get_all_users(Page)
            return JSONResponse(
                content=jsonable_encoder({
                    "message": "Orders retrieved successfully",
                    "length": len(users),
                    "users": [user.dict() for user in users],
                }),
                status_code=200,
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def get_user_byID(self, user_id, payload):
        try:
            role_id = payload.get("role_id") or payload.get("RoleID")
            if role_id != 1:
                if user_id != payload.get("user_id"):
                    return JSONResponse(
                        content={
                            "message": "User not found",
                        },
                        status_code=404
                    )
            users_sv = UsersService()
            user_deltail = users_sv.get_user_byID(user_id)
            return JSONResponse(
                content={
                    "message": "Users retrieved successfully",
                    "product": user_deltail.dict()
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def get_user_byEmail(self, email, payload):
        try:
            role_id = payload.get("role_id") or payload.get("RoleID")
            users_sv = UsersService()
            user_deltail = users_sv.get_user_byEmail(email)
            if role_id != 1:
                if user_deltail.UserID != payload.get("user_id"):
                    return JSONResponse(
                        content={
                            "message": "User not found",
                        },
                        status_code=404
                    )
            
            return JSONResponse(
                content={
                    "message": "Users retrieved successfully",
                    "product": user_deltail.dict()
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def update_user(self, user: RegisterDTO, payload):
        try:
            user_id = payload.get("user_id")
            user_sv = UsersService()
            old_user = user_sv.get_user_byID(user_id)

            if not old_user:
                return JSONResponse(
                    content={
                        "message": "User not found",
                    },
                    status_code=404
                )

            # ✅ Điền giá trị cũ nếu người dùng không nhập
            user.UserName = user.UserName or old_user.UserName
            user.Address = user.Address or old_user.Address
            user.PhoneNumber = user.PhoneNumber or old_user.PhoneNumber
            user.Email = user.Email or old_user.Email
            user.Password = user.Password or old_user.Password

            # ✅ Kiểm tra định dạng email hợp lệ
            email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
            if not re.match(email_pattern, user.Email):
                return JSONResponse(
                    content={
                        "message": "Invalid email format",
                    },
                    status_code=400
                )

            # ✅ Kiểm tra email trùng lặp (nếu người dùng đổi email)
            if user.Email != old_user.Email and user_sv.get_user_byEmail(user.Email):
                return JSONResponse(
                    content={
                        "message": "Email already exists",
                    },
                    status_code=400
                )

            # ✅ Cập nhật người dùng
            user_sv.update_user(user_id, user)

            return JSONResponse(
                content={"message": "Updated successfully"},
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")