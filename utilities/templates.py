class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def __str__(self):
        return f'Name: {self.__name}, Age: {self.__age}'

print(__name__)
if __name__ == '__main__':
    person = Person('Alex', 26)
    print(person)
