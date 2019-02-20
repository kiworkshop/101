import datetime

# Post Class만들기
class Post:
    max_post_no = 0

    def __init__(self, post_title, post_register, post_no=None, post_deleted=None ,post_inserted_time=None):
        self.post_title = post_title
        self.post_register = post_register
        print(Post.max_post_no)
        if post_no != None and int(post_no) > Post.max_post_no:
            Post.max_post_no = int(post_no)
        if post_no == None:
            post_no = Post.max_post_no + 1
            Post.max_post_no = post_no
        self.post_no = int(post_no)
        # self.post_no = post_no if post_deleted is not None else 
        if post_deleted is None:
            post_deleted = 'N'
        self.post_deleted = post_deleted
        if post_inserted_time is None:
            post_inserted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.post_inserted_time = post_inserted_time

    def __lt__(self, other): # 별도 모듈 없이 클래스 정렬을 위함
        return self.post_no < other.post_no

    def save_to_file(self):
        return [self.post_title, self.post_register, self.post_no, self.post_deleted, self.post_inserted_time]

    @staticmethod
    def load_from_file(file_post_title, file_post_register, file_post_no, file_post_deleted, file_post_inserted_time):
        new_post = Post(file_post_title, file_post_register, file_post_no, file_post_deleted, file_post_inserted_time)
        return new_post

    def logical_delete(self):
        self.post_deleted = 'Y'

    def update_post_title(self, updated_post_title):
        self.post_title = updated_post_title

    def check_authority(self, signed_in_user_id):
        if self.post_register == signed_in_user_id:
            return True
        if self.post_register != signed_in_user_id:
            return False
    