import datetime

class Post():
    pid = 1

    def __init__(self, title, user_id, deleted_at, pid=None, created_at=None):
        self.pid = str(Post.pid) if pid is None else pid
        self.title = title
        self.user_id = user_id
        self.deleted_at = deleted_at
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if created_at is None else created_at
        Post.pid += 1

    def __str__(self):
        return '{:^8} | {:60.60} | {} | {}'.format(self.pid, self.title, self.user_id, self.created_at)
    
    def update(self, new):
        self.title = new
    
    def delete(self):
        self.deleted_at = 'DELETE'

    def is_undeleted(self):
        return self.deleted_at == 'UNDELETED'
             
    def has_pid(self, pid):
        return self.pid == pid
        
    @classmethod
    def from_csv(cls, csv):
        pid, title, user_id, created_at, deleted_at = csv[:-1].split(',')
        return cls(title, user_id, deleted_at, pid, created_at)
    
    def to_csv(self):
        return '{},{},{},{},{}'.format(self.pid, self.title, self.user_id, self.created_at, self.deleted_at)
