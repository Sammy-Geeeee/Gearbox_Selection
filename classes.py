# This will include classes for motor and gearbox items


import re


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
    
    def printData(self):
        print(f'{self.brand} {self.series} {self.frame} {self.poles}')
        print(f'{self.power}kW, {self.speed}rpm')
        print(f'{self.shaft}mm shaft, {self.weight}kg')


class Gearbox:
    def __init__(self, serie_size, ratio):
        self.brand = 'Bonfig'
        self.serie_size = serie_size
        self.ratio = ratio
    
    def printData(self):
        print(f'{self.brand} {self.serie_size}_ {self.ratio}:1')


class GearedMotor:
    def __init__(self, gearbox, motor):
        self.gearbox = gearbox
        self.motor = motor

        # Gearbox and Motor info from objects
        self.motor_power = motor.power
        self.motor_speed = motor.speed
        self.motor_frame = motor.frame
        self.motor_brand = motor.brand
        self.motor_series = motor.series
        self.motor_poles = motor.poles
        self.gearbox_brand = gearbox.brand
        self.gearbox_serie_size = gearbox.serie_size
        self.gearbox_ratio = gearbox.ratio
        self.gearbox_frame = f"P{re.search(r'[0-9]+', self.motor_frame).group()}"

        # Something else needs to go here...
    
    def printData(self):
        print(f'{self.gearbox_brand} {self.gearbox_serie_size}_ {self.gearbox_ratio}:1 {self.gearbox_frame} B_')
        print(f'{self.motor_brand} {self.motor_series} {self.motor_frame} {self.motor_poles} B_ ({self.motor_power}kW, {self.motor_poles}P)')




