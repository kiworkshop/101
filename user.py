class User():
    logged_in = None
    
    def __init__(self, user_id=None, user_pw=None):
        self.user_id = user_id
        self.user_pw = user_pw
    
    @classmethod
    def from_csv(cls, csv):
        user_id, user_pw = csv[:-1].split(',')
        return cls(user_id, user_pw)

    def to_csv(self):
        return '{},{}'.format(self.user_id, self.user_pw)