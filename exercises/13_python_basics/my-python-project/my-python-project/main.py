print("output")

calculation_to_units = 24
name_of_unit = "hours"

def days_to_units(num_of_days, unit = "hours"):
    if unit == "hours":
        return f"{num_of_days} days are {num_of_days * 24} {unit}"
    elif unit == "minutes":
        return f"{num_of_days} days are {num_of_days * 24 * 60} {unit}"
    else:
        return "unsupported unit"


def validate_and_execute(days_and_unit_dict):
    try:

        num_of_days = int(days_and_unit_dict["days"])
        unit = days_and_unit_dict.get("unit")
        if num_of_days > 0:
            calculated_value = days_to_units(num_of_days, unit)
            print(calculated_value)
        elif num_of_days == 0:
            print("You entered a 0, please enter a valid number")
        else:
            print("You entered a negative number, no conversion for you")

    except ValueError:
        print("Your input is not a number. Don't ruin my program")


user_input = ""
while user_input != "exit":
    user_input = input("Enter a number of days and conversion unit:\n")
    days_and_unit = user_input.split(":")
    if len(days_and_unit) != 2:
        print("You entered the input in the wrong format. Stick to the x:unit format")
    else:
        days_and_unit_dictionary = {"days": days_and_unit[0], "unit": days_and_unit[1]}
        validate_and_execute(days_and_unit_dictionary)
