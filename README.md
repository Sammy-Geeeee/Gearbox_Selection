# Geared_Motor_Selector
Program to select gearbox and motor combinations based on simple mechanical input info.

This program is my attempt at seeing how much manual catalogue specification checking I could automate.

Finding the specs for motor and gearbox combinations is a fairly simple task when done by hand, but is fairly time consuming task when done multiple times a day, or with a constantly changing requirement set.
This program can do most of the number crunching for me, allowing me to quickly establish whether a certain setup will be a viable solution to the given problem.

Use of this program will be simple enough for anyone familiar with motor and gearbox specifications.
The inputs are a handful of basic specs, output speeds and torques, safety factors, as well as motors, and gearbox types and sizes.
Once this is all entered, the program will generate a list of geared motor combinations and their specifications.
Those that fit within the given conditions will be output onto the screen, giving a quick but comprehensive look at what would achieve the requested outputs.

The program works by going through spreadsheets of data that I put together, and pulling specs from them.
The data was manually keyed and copied from the catalogued specifications sheets, and so is accurate from the manufacturer.

There is also a check function, allowing users to input an existing gearbox and motor and have the specs for that combination provided.
As well as a data validation function within the code (Not in the GUI), that will ensure all of the spreadsheet data has been given in an appripriate format.
