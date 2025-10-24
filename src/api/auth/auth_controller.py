import re
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.api.auth.auth_service import AuthService
from src.dto.user_dto import UserDTO, LoginDTO, RegisterDTO
from src.utils.authentication import create_access_token

class AuthController():
    def login(self, user: LoginDTO):
        try:
            if not user.Email or not user.Password:
                return JSONResponse(
                    content={
                        "message": "Email or Password is empty",
                    },
                    status_code=404
                )
            
            # Validate email format
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_regex, user.Email):
                return JSONResponse(
                    content={
                        "message": "Email is not valid",
                    },
                    status_code=400
                )

            auth_sv = AuthService()
            user_id, role_id = auth_sv.login(user)
            
            if not user_id or not role_id:
                return JSONResponse(
                    content={
                        "message": "Email & Password invalid",
                    },
                    status_code=404
                )
            
            access_token = create_access_token({
                "user_id": user_id,
                "role_id": role_id
            })

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token
                },
                status_code=200
            )
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def register(self, user: RegisterDTO):
        try:
            # Check required fields
            if not all([user.UserName, user.Password, user.PhoneNumber, user.Address, user.Email]):
                return JSONResponse(
                    content={"message": "Please fill in all required fields"},
                    status_code=400
                )

            # Validate email
            email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.fullmatch(email_regex, user.Email):
                return JSONResponse(
                    content={"message": "Email is not valid"},
                    status_code=400
                )
            
            if len(user.PhoneNumber) != 10:
                return JSONResponse(
                    content={"message": "PhoneNumber is not valid (length = 10)"},
                    status_code=400
                )

            auth_sv = AuthService()
            # Check if email already exists (case-insensitive)
            if auth_sv.get_user_byEmail(user.Email):
                return JSONResponse(
                    content={"message": "Email already exists"},
                    status_code=400
                )

            # Register user with role_id = 2
            auth_sv.register(user, 2)

            return JSONResponse(
                content={"message": "Registered successfully"},
                status_code=201
            )

        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")




