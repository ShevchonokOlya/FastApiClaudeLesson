class Car:
    def __init__(self, name):
        self.name = name
        self._speed = 0
        self.__pin = "1234"

    def press_gas(self):
        self._speed += 10

    def __str__(self):
        return f"{self.name}: {self._speed} km/h"


class ElectricCar(Car):
    def __init__(self, name, battery):
        super().__init__(name)
        self.battery = battery

    def press_gas(self):
        self._speed += 20


# cars = [Car("Old car"), ElectricCar("Electric car", 80)]
# for car in cars:
#     car.press_gas()
#     print(car)
#
# print(cars[0]._speed)
# print(cars[0]._Car__pin)

class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"{self.title}, {self.pages} pages"

class EBook(Book):
    def __init__(self, title, pages,size_mb):
        super().__init__(title, pages)
        self.size_mb = size_mb

    def __str__(self):
        return super().__str__() + f", {self.size_mb} MB"

for book in [Book("Dune", 500), EBook("The Hobbit", 300, 5)]:
    print(book)