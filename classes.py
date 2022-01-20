# This will include classes for motor and gearbox items


# Imports go here


class Motor:
    def __init__(self, power, speed, frame, shaft, weight, brand, series, poles):
        self.power = power
        self.speed = speed
        self.frame = frame
        self.shaft = shaft
        self.weight = weight
        self.brand = brand
        self.series = series
        self.poles = poles
    
    def print_data(self):
        print(f'{self.brand} {self.series} {self.frame} {self.poles}')
        print(f'{self.power}kW, {self.speed}rpm')
        print(f'{self.shaft}mm shaft, {self.weight}kg')





