from user import User
from post import Post

john = User("John", "1234", "Developer", "john@john.at")
john.print_user_info()
john.change_job_title("Senior Developer")
john.print_user_info()

new_post = Post("Hello World", "John")
new_post.print_post_info()
