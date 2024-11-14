# import random

# print(random.randint(1, 10))

import calculator as calc
from random import randint, choice as select_random_element
from utilities.templates import Person
from termcolor import cprint
from decouple import config

print(randint(1, 10))
print(select_random_element(["Apple", "Banana", "Orange"]))

print(calc.addition(8, 9))

friend = Person('Jim', 44)
print(friend)

cprint("Hello, World!", "green", "on_red")

print(config('SECRET_KEY'))
commented = config('COMMENTED', default=0, cast=int)
print(commented * 2)
