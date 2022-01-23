# This will include classes for motor and gearbox items


import re


def interpolation(out_low, out_high, in_low, in_high, in_final):  # Function to interpolate data from the sheets
    out_final = out_low + ((out_high-out_low)/(in_high-in_low))*(in_final-in_low)
    return out_final


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
        data0 = f'{self.brand} {self.series} {self.frame} {self.poles}'
        data1 = f'{self.power}kW, {self.speed}rpm'
        data2 = f'{self.shaft}mm shaft, {self.weight}kg'
        return [data0, data1, data2]


class Gearbox:
    def __init__(self, serie_size, ratio, shaft, p8data, p6data, p4data, p2data):
        self.brand = 'Bonfig'
        self.serie_size = serie_size
        self.ratio = ratio
        self.shaft = shaft
        self.p8data = p8data
        self.p6data = p6data
        self.p4data = p4data
        self.p2data = p2data
    
    def printData(self):
        data0 = f'{self.brand} {self.serie_size}_ {self.ratio}:1'
        data1 = f'{self.p8data}    {self.p6data}    {self.p4data}    {self.p2data}'
        return [data0, data1]


class GearedMotor:
    def __init__(self, gearbox, motor):
        # To import the gearbox and motor objects directly
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
        self.gearbox_shaft = gearbox.shaft
        self.gearbox_frame = f"P{re.search(r'[0-9]+', self.motor_frame).group()}"

        # Now to calculate all the stats that are part of these being together
        if 500 > self.motor_speed or self.motor_speed > 3000:
            print(f'{self.motor_speed}    Invalid motor speed')
        elif 500 <= self.motor_speed <= 900:
            motor_low = 500
            motor_high = 900
            low_data = self.gearbox.p8data
            high_data = self.gearbox.p6data
        elif 900 < self.motor_speed <= 1400:
            motor_low = 900
            motor_high = 1400
            low_data = self.gearbox.p6data
            high_data = self.gearbox.p4data
        elif 1400 < self.motor_speed <= 2800:
            motor_low = 1400
            motor_high = 2800
            low_data = self.gearbox.p4data
            high_data = self.gearbox.p2data
        
        elif 2800 < self.motor_speed <= 3000:
            motor_low = 2800 * 0.9999
            motor_high = 2800 * 1.0001
            low_data = self.gearbox.p4data
            high_data = self.gearbox.p2data

        # Getting all the data from each gearbox
        spd_low = low_data[0]
        trq_low = low_data[1]
        pwr_low = low_data[2]
        eff_low = low_data[3]
        spd_high = high_data[0]
        trq_high = high_data[1]
        pwr_high = high_data[2]
        eff_high = high_data[3]

        # Finding the actual values from interpolation, for gearbox data only
        gbox_out_spd = interpolation(spd_low, spd_high, motor_low, motor_high, self.motor_speed)
        gbox_out_trq = interpolation(trq_low, trq_high, motor_low, motor_high, self.motor_speed)
        gbox_out_pwr = interpolation(pwr_low, pwr_high, motor_low, motor_high, self.motor_speed)
        gbox_out_eff = interpolation(eff_low, eff_high, motor_low, motor_high, self.motor_speed)

        # Now to make the actual ratings for each geared motor combo
        self.gm_spd = gbox_out_spd
        self.gm_trq = gbox_out_trq * (self.motor_power / gbox_out_pwr)
        self.gm_safety = gbox_out_pwr / self.motor_power


    def printData(self):
        data0 = f'{self.gearbox_brand} {self.gearbox_serie_size}_ {self.gearbox_ratio}:1 {self.gearbox_frame} B_'
        data1 = f'{self.motor_brand} {self.motor_series} {self.motor_frame} {self.motor_poles} B_  ({self.motor_power}kW, {self.motor_poles}P)'

        if self.gearbox_shaft[1] != 'None':
            data2 = f'{self.gm_spd:.2f}rpm,  {self.gm_trq:.2f}Nm,  {self.gm_safety:.2f} S.F,  {self.gearbox_shaft[0]}mm or {self.gearbox_shaft[1]}mm output'
        else:
            data2 = f'{self.gm_spd:.2f}rpm,  {self.gm_trq:.2f}Nm,  {self.gm_safety:.2f} S.F,  {self.gearbox_shaft[0]}mm output'
        
        return [data0, data1, data2]
