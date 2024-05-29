from helper import validate_and_execute, user_input_message

user_input = ""
while user_input != "exit":
    user_input = input(user_input_message)
    days_and_unit = user_input.split(":")
    if len(days_and_unit) != 2:
        print("You entered the input in the wrong format. Stick to the x:unit format")
    else:
        days_and_unit_dictionary = {"days": days_and_unit[0], "unit": days_and_unit[1]}
        validate_and_execute(days_and_unit_dictionary)
