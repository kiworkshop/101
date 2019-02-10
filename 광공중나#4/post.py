from datetime import datetime

def auto_check_permission(action_type):
    def decorated(func):
        def inner(caller, *args, **kwargs):
            if caller.check_permission(*args, action_type = action_type): # 처리하려면 조건 True
                func(caller, *args, **kwargs)
        return inner
    return decorated

class Post():
    CURRENT_POSTING_NUM = 0

    def __init__(self, posting_user, existence_state = None, posting_num = None, posting_title = None, posting_time = None):
        self.posting_user = posting_user
        self.existence_state = True if existence_state is None else existence_state == 'True' # check the validation of this post 
        self.posting_num = Post.CURRENT_POSTING_NUM + 1 if posting_num is None else int(posting_num)
        Post.CURRENT_POSTING_NUM = Post.CURRENT_POSTING_NUM + 1 if posting_num is None else max(Post.CURRENT_POSTING_NUM, int(posting_num))
        self.posting_title = input('작성 > ') if posting_title is None else posting_title
        self.posting_time = datetime.now().strftime('%Y-%m-%d %H:%M') if posting_time is None else posting_time

    def check_permission(self, user_id, action_type):
        action_kwds = ['수정', '삭제']
        if user_id != self.posting_user:
            input('{}님께는 해당 글 {} 권한이 없습니다!'.format(user_id, action_kwds[action_type - 1]))
            return False
        return True

    @auto_check_permission(1)
    def update_posting_title(self, user_id):
        self.posting_title = input('수정 > ')
        input('{}번 글이 성공적으로 수정되었습니다.'.format(self.posting_num))

    @auto_check_permission(2)
    def soft_delete_post(self, user_id):
        self.existence_state = False
        input('{}번 글이 성공적으로 삭제되었습니다.'.format(self.posting_num))

    @classmethod
    def from_csv(cls, csv):
        existence_state, posting_num, posting_title, posting_user, posting_time = csv[:-1].split(',')
        return cls(posting_user, existence_state, posting_num, posting_title, posting_time)
    
    def to_csv(self):
        return '{},{},{},{},{}'.format(self.existence_state, self.posting_num, self.posting_title, self.posting_user, self.posting_time)