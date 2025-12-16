from app.models.user_model import UserCreate, UserRead

users = {
    1: {"id": 1, "name": "John Doe", "nickname": "johnd",
        "email": "john.doe@example.com"},
    2: {"id": 2, "name": "Jane Smith", "nickname": "janes",
        "email": "jane.smith@example.com"}
    
}


class UserService:
    def __init__(self):
        pass
    
    def get_all_users(self):
        return list(users.values())
    
    def get_user_by_id(self, user_id: int):
        return users.get(user_id, None)
    
    def create_user(self, user_data: UserCreate):
        new_id = max(users.keys()) + 1 # This will be handy for auto-increment
        users[new_id] = {
            "id": new_id,
            "name": user_data.name,
            "nickname": user_data.nickname,
            "email": user_data.email
        }
        user = UserRead(**users[new_id])
        return user

    def update_user(self, user_id: int, user_data: dict):
        if user_id in users:
            users[user_id].update(user_data)
            return users[user_id]
        return None
    
    def delete_user(self, user_id: int):
        return users.pop(user_id, None)
    