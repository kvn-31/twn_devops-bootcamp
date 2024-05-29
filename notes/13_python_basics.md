# Python Basics

- simple syntax
- large ecosystem
- flexible
  - web development
  - data science
  - machine learning
  - ai
  - web scraping
  - automation

## Python as DevOps Engineer
- more automation, less manual work
- automation scripts for teams
- system health checks, ci/cd, monitoring tasks, backup tasks, cleanup, etc.

## Syntax and Basics
### Data Types
- String
  - single or double quotes
- Integer
- Float
- Boolean

`type(value)` returns the type of the value


### String concatenation
```python
first_name = "John"
last_name = "Doe"
full_name = first_name + " " + last_name
print(full_name)
```

```python
print("20 days are " + str(20) + " weeks")
print(f"20 days are {20*24} hours") #using f for format
```

### Variables
- python is dynamically typed
- naming convention: snake_case
- python has reserved keywords (e.g. `and`, `as`, `for`, `while`, `def`, `class`, etc.)
```python
to_seconds = 24 * 60 * 60
print(f"20 days are {20 * to_seconds} seconds")
```

### Functions
```python 
def days_to_units(num_of_days):
    print(f"{num_of_days} days are {20 * 24} hours")
    print("All good!")


days_to_units(6)
```

### Scope
- global scope
  - outside of functions
- local scope
  - inside of functions

### User Input
```python
user_input = input("Enter a number of days:\n")
```

Validate user input
```python
user_input = input("Enter a number of days:\n")
if user_input.isdigit():
    user_input = int(user_input)
else:
    print("You entered an invalid input. No calculation done")
    exit()
```
### Type Casting
```python
user_input_number = int(user_input)
```

### Try-Ecept
```python
try:
    user_input_number = int(user_input)
except ValueError:
    print("You entered an invalid input. No calculation done")
```
