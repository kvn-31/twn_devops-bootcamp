class User:
    def __init__(self, name, password, job_title, email):
        self.name = name
        self.password = password
        self.job_title = job_title
        self.email = email


    def change_password(self, password):
        self.password = password
        print("Password changed successfully")

    def change_job_title(self, job_title):
        self.job_title = job_title
        print("Job title changed successfully")

    def print_user_info(self):
        print (f"Name: {self.name}, Job Title: {self.job_title}, Email: {self.email}")

