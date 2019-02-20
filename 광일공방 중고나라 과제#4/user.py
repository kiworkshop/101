import hashlib

class User:
    def __init__(self, user_id, user_password):
        self.user_id = user_id
        encoded_password = user_password.encode()
        self.user_password = hashlib.sha256(encoded_password).hexdigest()

    def save_to_file(self):
        return [self.user_id, self.user_password]    

    @staticmethod
    def load_from_file(file_user_id, file_user_password):
        new_user = User(file_user_id, file_user_password)
        return new_user