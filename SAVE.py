SAVE_PATH_POST = "post.csv"
SAVE_PATH_USER = "user_info.csv"

def autosave(func):
    def wrapper(caller, *args, **kwargs):
        func(caller)
        caller.save()
    return wrapper
