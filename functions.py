# This will be all the functions and classes for the gearbox selection program


import openpyxl


# Gearbox workbook function
def applicable_series(input):  # takes the input type(s) and will output a list of series workbook names
    series = []  # Empty list to store all the applicable workbooks in
    if input['type'] == 'VF W':
        workbook = openpyxl.load_workbook('VF_W_Gearboxes.xlsx')
        series.append(workbook)
    else:
        print('Invalid Workbook has been selected. Try again')

    return series  # This will return a list of workbook objects
# TODO - Need to somehow make this work the same way as the gates program
# Todo - Let you choose multiple input tick boxes and then return all the appropriate ones


# Gearbox series and size narrowing function
def applicable_sizes(input, all_series):  # Takes the input data and a list of workbook objects, outputs a list of applicable sheet objects
    size_options = set()  # Blank set for all the good series

    for series in all_series:
        sizes_list = series.sheetnames  # make a list of all the sheetnames

        for size in sizes_list:
            sheet = series[size]  # To set this worksheet

            # To define all the values to check for
            max_trq = float(sheet['B1'].value)
            shft_std = float(sheet['O1'].value)
            tol_trq = float(input['tol_trq']/100)
            try:  # This will make the alternate shaft size equal to the standard one
                shft_alt = float(sheet['P1'].value)
            except TypeError:
                shft_alt = float(sheet['O1'].value)

            # These conditions will exclude all the gearboxes and series that won't work
            if sheet['B4'].value is not None:  # To exclude the empty worksheets
                if input['out_trq']*(1-tol_trq) <= max_trq:  # To make sure the geaerbox can handle the torque
                    if input['shft_min'] <= shft_std <= input['shft_max']:  # To make sure the shaft size will work
                        if input['shft_min'] <= shft_alt <= input['shft_max']:  # To check if an alternate shaft size will work
                            size_options.add(sheet)  # To add each acceptable size to the list

        return size_options  # This will return a list of sheet objects that are applicable


# Torque table information
def gearbox_data(input, sheets):  # Takes the input data and the list of sheet objects, outputs a list of cells that the selected speeds are found in
    tol = input['tol_spd']/100
    spd_lwr = input['out_spd'] * (1 - tol)
    spd_upr = input['out_spd'] * (1 + tol)

    gbx_sheet_cells = []
    for sheet in sheets:  # To iterate through each sheet
        for c in [6, 10, 14]:  # To iterate through each speed column  # TODO - I've removed column 2 here, not sure what to actually do with this data (500rpm)
            for r in range(4, sheet.max_row+1):  # To iterate through each ratio row
                data_spd = float(sheet.cell(column=c, row=r).value)  # These will save each of the catalogue speed and torque data
                data_trq = float(sheet.cell(column=c+1, row=r).value)

                if spd_lwr <= data_spd <= spd_upr:  # These will make sure the speeds and torques are applicable
                    if input['out_trq']*(1-tol) <= data_trq:
                        if data_trq <= 3*input['out_trq']:
                            gbx_sheet_cells.append((sheet, sheet.cell(column=c, row=r)))

    return gbx_sheet_cells


# Finds all the data needed to specify the motor that will be used
def motor_data(input, gbox_sheets_cells):  # Input is all user input, and the gearbox sheets and cells, output is motor sheets and cells
    mtr_workbook = openpyxl.load_workbook('Motors.xlsx')

    mtr_sheet_cells = []
    for option in gbox_sheets_cells:
        gbox_sheet = option[0]
        cell_col, cell_row = option[1].column, option[1].row

        mtr_poles = gbox_sheet.cell(column=cell_col, row=2).value[0:6]
        mtr_sheet = mtr_workbook[mtr_poles]

        tol = input['tol_trq']/100
        pwr_req = ((input['out_trq'] * input['out_spd']) / (9550 * option[1].offset(0, 3).value/100)) * (1 - tol)

        for r in range(3, mtr_sheet.max_row+1):
            mtr_pwr = mtr_sheet.cell(column=1, row=r).value

            if mtr_pwr is not None:  # To exclude the empty sheets
                if mtr_pwr >= pwr_req:
                    mtr_sheet_cells.append((mtr_sheet, mtr_sheet.cell(column=2, row=r)))
                    break  # This means it will only ever choose the lower applicable value, all we really need

    return mtr_sheet_cells


# This will do the final gearbox selection and specification work
def final_selection(gbox_info, motor_info):  # Inputs are the input data and the chosen speed cells, outputs are??
    all_selections = []
    for gbox, motor in zip(gbox_info, motor_info):
        gbx_sheet = gbox[0]  # This will define the gearbox sheet and speed cell
        gbx_spd_cell = gbox[1]
        gbox_r, gbox_c = gbx_spd_cell.row, gbx_spd_cell.column
        mtr_sheet = motor[0]  # This will define the motor sheet and speed cell
        mtr_spd_cell = motor[1]

        series = gbx_sheet['A2'].value
        ratio = float(gbx_sheet.cell(row=gbox_r, column=1).value)
        power = float(mtr_spd_cell.offset(0, -1).value)
        poles = mtr_sheet['A1'].value
        eff = gbx_spd_cell.offset(0, 3).value / 100

        mtr_spd = int(mtr_spd_cell.value)
        out_spd = mtr_spd / ratio
        out_trq = (power/out_spd) * 9550 * eff

        trq_cat = gbx_spd_cell.offset(0, 1).value
        sf = trq_cat / out_trq
        shafts = (gbx_sheet['O1'].value, gbx_sheet['P1'].value)
        if shafts[1] is None:
            shaft_txt = f'{shafts[0]}mm output'
        else:
            shaft_txt = f'{shafts[0]}mm or {shafts[1]}mm output'

        base_info = f'{series}_ {ratio:.0f}:1 + {power}kW {poles} ({mtr_spd}rpm)'
        ratings = f'{out_spd:.1f}rpm, {out_trq:.1f}Nm, {sf:.1f} SF, {shaft_txt}'
        warnings = f''

        if sf < 1.25:
            warnings = f'Warning - This selection has a low safety factor, {sf:.1f}'

        all_selections.append((base_info, ratings, warnings))

    return all_selections


# This function will let you put in just the inputs up front and then it will give you everything you need out
def entire_function(inputs):
    series = applicable_series(inputs)
    sizes = applicable_sizes(inputs, series)
    gearboxes = gearbox_data(inputs, sizes)
    motors = motor_data(inputs, gearboxes)
    choices = final_selection(gearboxes, motors)
    return choices
