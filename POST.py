import datetime
from USER import User, UserManager

class NotAuthorizedError(Exception):
    pass

def check_authorization(action_name):
    def wrapper(func):
        def inner(caller, *args, **kwargs):
            try:
                if not caller.is_same_writer():
                    raise NotAuthorizedError
                func(caller, *args, **kwargs)
            except NotAuthorizedError:
                print("{}님께 {} 권한이 없습니다.".format(UserManager.LOGINNED_USER.user_id, action_name))
        return inner
    return wrapper

class Post:
    COUNT = 0 
    
    def __init__(self, post_title, post_writer, post_no = None, post_time=None, post_shown_status=None):
        Post.COUNT += 1                  
        self.post_no = Post.COUNT if post_no is None else post_no            
        self.post_title = post_title
        self.post_writer = post_writer
        self.post_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M') if post_time is None else post_time
        self.post_shown_status = True if post_shown_status is None else post_shown_status

    def __str__(self):
        return f"{self.post_no:^8} | {self.post_title:60.60} | {self.post_writer:^10.10} | {self.post_time}"

    @check_authorization("수정")
    def update_title(self):       
        updated_title = input('수정>')
        self.post_title = updated_title

    @check_authorization("삭제")
    def change_shown_status(self):              
        self.post_shown_status = False

    def has_post_no(self, post_no):
        return self.post_no == post_no and self.post_shown_status == True

    def is_same_writer(self):
        return self.post_writer == UserManager.LOGINNED_USER.user_id

    @classmethod
    def from_csv(cls, csv):
        post_no, post_title, post_writer, post_time, post_shown_status = csv.strip('\n').split(',')
        return cls(post_title, post_writer, post_no = int(post_no), post_time = post_time, post_shown_status = post_shown_status == "True")
        
    def to_csv(self):
        return f"{self.post_no},{self.post_title},{self.post_writer},{self.post_time},{self.post_shown_status}"
