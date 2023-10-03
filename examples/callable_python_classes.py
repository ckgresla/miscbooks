# to make a class callable, we just include the logic inside of the __call__ method --> this then lets us call the class to execute the logic 


class Car:
    def __init__(self, hp):
        self.horsepower = hp

    def __call__(self):
        print("vroom " * self.horsepower ) 
        return

mustang = Car(hp=200)

mustang()
