class Car:
    weight = 100


car1 = Car()
car2 = Car()

Car.weight = 300

car2.weight = 300
print(car1.weight)
print(car2.weight) 