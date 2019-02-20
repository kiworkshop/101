import datetime
import csv
from post import Post

POST_DATA_PATH = 'second-hand_shop_post_data.csv'

class Board():
    def __init__(self, signed_in_user_id):
        self.signed_in_user_id = signed_in_user_id
        self.posts = []
        self.actions = [self.add_post, self.update_post, self.delete_post, self.go_to_previous_page, self.go_to_next_page]
        self.page_index = 1
        self.posts_per_page = 15
        

    @staticmethod 
    def print_actions(): 
        print('---------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        # print('4. 저장하기')
        print('4. 이전 페이지로')
        print('5. 다음 페이지로')
        print('---------------------------------------')

    def print_post_list(self):
        if self.posts == []:
            print("작성된 판매게시글이 없습니다.")
            print("회원님이 한 번 작성해보시는 것이 어떨까요?")
            return

        not_deleted_posts = (post for post in self.posts if post.post_deleted == 'N')
        self.posts = list(not_deleted_posts)
        self.posts.sort(reverse=True)
        paged_posts = self.posts[self.posts_per_page*(self.page_index-1):self.posts_per_page*self.page_index]
        for post in paged_posts: # [FIX] 포맷 한글일 때 padding 제대로 출력안됨. 들쑥날쑥
            print('{:^8} | {:<60} | {:^6} | {}'.format(post.post_no, post.post_title, post.post_register, post.post_inserted_time))

        page_length = self.get_page_length()
        print('Page: {}'.format(str(self.page_index) + '/' + str(page_length)))

    def get_user_action(self):
        try:
            user_action_no = int(input('> '))
        except:
            print('잘못된 입력입니다.')
            input()    
            return  
        if user_action_no >0 and user_action_no <= len(self.actions):
            self.actions[user_action_no - 1]()
            return  
        print('잘못된 입력입니다.')

    def save_posts(func):
        def wrapper(self):
            func(self)
            save_data = open ('중고나라 데이터.csv', 'w', encoding='utf8', newline='')
            posts_write = csv.writer(save_data)
            for post in self.posts:
                posts_write.writerow(post.save_to_file())
            save_data.close()
            #input('저장이 완료되었습니다')
        return wrapper

    @save_posts
    def add_post(self):
        # if self.posts == []:
        #     post_no = 1
        # if self.posts != []:
        #     post_no = self.posts[0].post_no + 1
        post_title = input('내용> ')
        #post_inserted_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.posts.append(Post(post_title, self.signed_in_user_id))
    
    @save_posts
    def update_post(self):
        targets = self.get_target_post_no('삭제')
        if targets == None: # 입력값 검증 에러 처리 
            return
        target_post_no, target_post_index = targets
        if self.posts[target_post_index].check_authority(self.signed_in_user_id) == False:
            input('{} 님은 해당 글에 대한 권한이 없습니다'.format(self.signed_in_user_id))
            return
        updated_post_title = input('수정할 내용을 입력해주세요 >')
        self.posts[target_post_index].update_post_title(updated_post_title) 
        print(str(target_post_no) +'번 글이 수정되었습니다')
    
    @save_posts
    def delete_post(self):
        targets = self.get_target_post_no('삭제')
        if targets == None: # 입력값 검증 에러 처리 
            return
        target_post_no, target_post_index = targets
        if self.posts[target_post_index].check_authority(self.signed_in_user_id) == False:
            input('{} 님은 해당 글에 대한 권한이 없습니다'.format(self.signed_in_user_id))
            return
        self.posts[target_post_index].logical_delete()    
        # del(self.posts[target_post_index])
        print(str(target_post_no) +'번 글이 삭제되었습니다')
    
    def get_target_post_no(self, action):
        try:
            target_post_no = int(input('몇 번 글을 {}할까요? '.format(action)))
        except:
            input('잘못된 입력입니다')
            return     
        try:
            target_post_index = [index for index, post in enumerate(self.posts) if post.post_no == target_post_no][0] #?
            return [target_post_no,target_post_index]
        except:
            input('잘못된 입력입니다')
            return
    
    def load_posts(self):
        with open (POST_DATA_PATH, 'r', encoding='utf8') as load_data:
            posts_read = csv.reader(load_data)
            #print(posts_read)
            posts_read = [Post.load_from_file(*post) for post in posts_read]
            self.posts = list(posts_read)

    def go_to_next_page(self):
        page_length = self.get_page_length()
        page_index_to_go = self.page_index + 1
        if page_index_to_go > page_length:
            input("가장 끝 페이지입니다.")
            return
        self.page_index = page_index_to_go

    def go_to_previous_page(self):
        page_index_to_go = self.page_index - 1
        if page_index_to_go < 1:
            input("가장 앞 페이지입니다.")
            return
        self.page_index = page_index_to_go
    
    def get_page_length(self):
        return len(self.posts)//(self.posts_per_page) + 1