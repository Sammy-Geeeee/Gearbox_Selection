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
    def __init__(self, series_size, ratio, shaft, p8data, p6data, p4data, p2data):
        self.brand = 'Bonfig'
        self.series_size = series_size
        self.ratio = ratio
        self.shaft = shaft
        self.p8data = p8data
        self.p6data = p6data
        self.p4data = p4data
        self.p2data = p2data
    
    def printData(self):
        data0 = f'{self.brand} {self.series_size}_ {self.ratio}:1'
        data1 = f'{self.p8data}    {self.p6data}    {self.p4data}    {self.p2data}'
        return [data0, data1]


class GearedMotor:
    def __init__(self, gearbox, motor):
        # To import the gearbox and motor objects directly
        self.gearbox = gearbox
        self.motor = motor
        self.gearbox_frame = f"P{re.search(r'[0-9]+', self.motor.frame).group()}"

        # Now to calculate all the stats that are part of these being together
        if 500 <= self.motor.speed <= 900:
            motor_low = 500
            motor_high = 900
            low_data = self.gearbox.p8data
            high_data = self.gearbox.p6data
        elif 900 < self.motor.speed <= 1400:
            motor_low = 900
            motor_high = 1400
            low_data = self.gearbox.p6data
            high_data = self.gearbox.p4data
        elif 1400 < self.motor.speed <= 3000:
            # I've chosen to make this be up to 3000, even though the data is only counted up to 2800
            # The lack of data after 2800rpm means I have no real means of ensuring accuracy of these selections
            # However the only motors that are within this range are high efficiency/power 2P motors, which are not commonly used
            motor_low = 1400
            motor_high = 2800
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
        gbox_out_spd = interpolation(spd_low, spd_high, motor_low, motor_high, self.motor.speed)
        gbox_out_trq = interpolation(trq_low, trq_high, motor_low, motor_high, self.motor.speed)
        gbox_out_pwr = interpolation(pwr_low, pwr_high, motor_low, motor_high, self.motor.speed)
        gbox_out_eff = interpolation(eff_low, eff_high, motor_low, motor_high, self.motor.speed)

        # Now to make the actual ratings for each geared motor combo
        self.speed = gbox_out_spd
        self.torque = gbox_out_trq * (self.motor.power / gbox_out_pwr)
        self.safety = gbox_out_pwr / self.motor.power


    def printData(self):
        data0 = f'{self.gearbox.brand} {self.gearbox.series_size}_ {self.gearbox.ratio}:1 {self.gearbox_frame} B_'
        data1 = f'{self.motor.brand} {self.motor.series} {self.motor.frame} {self.motor.poles} B_  ({self.motor.power}kW, {self.motor.poles}P)'
        if self.gearbox.shaft[1] != 'None':
            data2 = f'{self.speed:.2f}rpm,  {self.torque:.2f}Nm,  {self.safety:.2f} S.F,  {self.gearbox.shaft[0]}mm or {self.gearbox.shaft[1]}mm output'
        else:
            data2 = f'{self.speed:.2f}rpm,  {self.torque:.2f}Nm,  {self.safety:.2f} S.F,  {self.gearbox.shaft[0]}mm output'
        
        return [data0, data1, data2]
