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
- Lists []
- Dictionaries {}
- Tuples ()

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

### Lists & Loops
- while
```pyton
user_input = ""
while user_input!= "exit"
    user_input = input("Enter a number of days:\n")
    validate_and_execute(user_input)
```
- for
```python
for i in range(1, 10):
    print(i)
```

- Lists
```python
my_list = ["January", "February", "March"]
my_list[0] = "December" # changes the first element
my_list.pop() # removes the last element
my_list.append("April") # adds an element at the end
```

### Sets
- Set items are unordered, unchangeable, and do not allow duplicate values.
- access elements via loop
- items cannot be changed, but can be added or removed
```python
my_set = {"apple", "banana", "cherry"}
my_set.add("lemon")    # add an element
my_set.remove("banana")    # remove an element
```

### Dictionaries
- key-value pairs
```python
my_dict = {
    "name": "John",
    "age": 36
}
print(my_dict["name"])
my_dict["age"] = 40 # change value
my_dict["city"] = "New York" # add new key-value pair

```
## Comments
```python
# This is a comment
# Multiline below
"""
This is a comment
written in
more than just one line
"""
```

## Modules
- a .py file to logically organize code
- a module contains related code (f.e. a feature)
- use `import` to include a module
```python
import mymodule as mm # with optional alias
mm.greeting("seas")
```
- alternatively only import specific function
```python
from mymodule import greeting
greeting("seas")
```
- built-in modules
  - datetime, math, os, sys, random, json, etc.
```python
import datetime
x = datetime.datetime.now()
```
