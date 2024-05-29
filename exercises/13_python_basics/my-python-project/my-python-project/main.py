print("output")

calculation_to_units = 24
name_of_unit = "hours"


def days_to_units(num_of_days):
    return f"{num_of_days} days are {num_of_days * calculation_to_units} {name_of_unit}"


def validate_and_execute(user_input):
    try:
        user_input = int(user_input)
        if user_input > 0:
            calculated_value = days_to_units(user_input)
            print(calculated_value)
        elif user_input == 0:
            print("You entered a 0, please enter a valid number")
        else:
            print("You entered a negative number, no conversion for you")

    except ValueError:
        print("Your input is not a number. Don't ruin my program")


user_input = input("Enter a number of days:\n")
validate_and_execute(user_input)
