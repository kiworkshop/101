import hashlib

class User():
    def __init__(self, id, pwd):
        self.id = id
        self.pwd = hashlib.sha256(pwd.encode()).hexdigest()

    def to_csv(self):
        return '{},{}'.format(self.id, self.pwd)