from time import gmtime, strftime

class Post() :
    index = 1
    def __init__(self, context, user_name):
        self.index = Post.index
        self.removed = False
        self.context = context
        self.time = strftime("%Y-%m-%d %H:%M", gmtime())
        self.user_name = user_name
        Post.index += 1

    def show(self):
        if self.removed == False:
            print('{:^8} | {:60.60} | {} | {}'.format(self.index, self.context, self.user_name, self.time))
