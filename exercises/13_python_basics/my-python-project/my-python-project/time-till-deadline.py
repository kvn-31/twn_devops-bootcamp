from datetime import datetime

user_input = input("Enter your goal with a deadline separated by colon\ngoal:dd.mm.yyyy\n")
input_list = user_input.split(":")

goal = input_list[0]
deadline = input_list[1]

deadline_date = datetime.strptime(deadline, "%d.%m.%Y")

today_date = datetime.today()
time_till = deadline_date - today_date

hours_till = int(time_till.total_seconds() / 60 / 60)
print(f"Time remaining for your goal {goal} is {hours_till} hours.")
