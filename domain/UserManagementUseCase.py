

from models.User import User
from services.UserRepository import UserRepository


class UserManagementUseCase:

    def __init__(self):
        self.userRepository = UserRepository()

    def login_user(self, user: User):
        if not self.userRepository.get_user(user.id):
            self.userRepository.create_user(user)
        return self.userRepository.get_user(user.id)
    
    def consume_credit(self, user_id, credit):
        user = self.userRepository.get_user(user_id)
        if user.plan == 'free':
            if user.credits < credit:
                raise Exception('Insufficient credits. Upgrade to Premiun to get unlimited credits')
            user.credits -= credit
            self.userRepository.update_user(user_id, user)
        return user
    
    def upgrade_plan(self, user_id, plan):
        user = self.userRepository.get_user(user_id)
        user.plan = plan
        user.credits = 0
        self.userRepository.update_user(user_id, user)
        return user