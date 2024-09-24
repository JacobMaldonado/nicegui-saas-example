from google.cloud import firestore

from models.User import User


class UserRepository:

    COLLECTION_NAME = "users"   

    def __init__(self):
        self.analysis = firestore.Client(project="confidentier")

    def get_user(self, user_id):
        user_result = self.analysis.collection(self.COLLECTION_NAME).document(user_id).get().to_dict()
        if user_result is None:
            return None
        return User.model_validate(user_result)
    
    def update_user(self, user_id, user):
        self.analysis.collection(self.COLLECTION_NAME).document(user_id).update(user.model_dump(exclude_none=True))
    
    def create_user(self, user: User):
        self.analysis.collection(self.COLLECTION_NAME).document(user.id).set(user.model_dump(exclude_none=True))