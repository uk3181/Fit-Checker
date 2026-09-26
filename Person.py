class Person:
    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.__gender = gender

    def setName(self, name):
        self.__name = name

    def setAge(self, age):
        self.__age = age

    def setGender(self, gender):
        self.__gender = gender

    def getName(self):
        return self.__name

    def getAge(self):
        return self.__age

    def getGender(self):
        return self.__gender