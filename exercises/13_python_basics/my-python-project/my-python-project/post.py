class Post:
    def __init__(self, message, author):
        self.message = message
        self.author = author

    def print_post_info(self):
        print(f"Message: {self.message}, Author: {self.author}")
