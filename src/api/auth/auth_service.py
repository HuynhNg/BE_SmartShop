from src.model.users_model import Users_model

class AuthService():
    def get_user_byEmail(self, Email: str):
        return Users_model.get_user_byEmail(Email)
    
    def register(self, new_user, role_id : int):
        return Users_model.register(new_user, role_id)
    
    def login(self, user):
        return Users_model.login(user)