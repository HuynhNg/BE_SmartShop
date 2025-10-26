import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.model.users_model import Users_model

class UsersService():
    def get_all_users(self, Page: int):
        return Users_model.get_all_users(Page)
    
    def get_user_byID(self, user_id :int):
        return Users_model.get_user_byID(user_id)
    
    def get_user_byEmail(self, user_email: str):
        return Users_model.get_user_byEmail(user_email)
    
    def update_user(self, user_id, user):
        return Users_model.update_user(user_id, user)