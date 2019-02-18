import datetime
from user import User

def check_athorization(func_name):
    def real_decorator(func):
        def wrapper(caller, *args):
            if caller.user_id == User.logged_in:
                func(caller, *args)
                return
            input(f'{User.logged_in}님께는 해당 글 {func_name} 권한이 없습니다!')
        return wrapper
    return real_decorator

class Post():
    pid = 1

    def __init__(self, title, user_id, pid=None, created_at=None, deleted=False):
        self.pid = Post.pid if pid is None else pid
        self.title = title
        self.user_id = user_id
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if created_at is None else created_at
        self.deleted = deleted
        Post.pid += 1

    def __str__(self):
        return '{:^8} | {:60.60} | {:^10.10} | {}'.format(self.pid, self.title, self.user_id, self.created_at)
    
    @check_athorization('수정')
    def update(self, new):
        self.title = new

    def has_pid(self, pid):
        return self.pid == pid

    @check_athorization('삭제')
    def delete(self):
        self.deleted = True

    def is_not_deleted(self):
        return self.deleted == False
        
    @classmethod
    def from_csv(cls, csv):
        pid, title, user_id, created_at, deleted = csv[:-1].split(',')
        pid = int(pid)
        deleted = False if deleted == 'False' else True
        return cls(title, user_id, pid, created_at, deleted)
    
    def to_csv(self):
        return '{},{},{},{},{}'.format(self.pid, self.title, self.user_id, self.created_at, self.deleted)