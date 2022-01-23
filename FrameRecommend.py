# This will define the FrameRecommend class, which is just the Recommend Frame in that tab


from functionRecommend import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import ttkwidgets
import openpyxl
import string
import re


class FrameRecommend(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Some base variables for sizing of various things
        pad_ext = 5
        pad_int = 2
        entry_width = 10

        # To make all the widgets within the Recommend tab
        self.label_inputs = tk.Label(self.master, text='Input Information')
        self.frame_inputs = tk.Frame(self.master)
        self.separator_in_out = ttk.Separator(self.master, orient='vertical')
        self.label_output = tk.Label(self.master, text='Output Information')
        self.frame_outputs = tk.Frame(self.master)
        # This will be all the positioning for these primary frames
        self.label_inputs.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        self.frame_inputs.grid(row=1, column=0)
        self.separator_in_out.grid(row=0, column=1, rowspan=2, padx=pad_ext, pady=pad_ext, sticky='nsew')
        self.label_output.grid(row=0, column=2, padx=pad_ext, pady=pad_ext)
        self.frame_outputs.grid(row=1, column=2)


        # Widgets in the Recommend tab input frame
        self.label_seriesize = tk.Label(self.frame_inputs, text='Applicable Series/Sizes')
        self.scroll_seriesize = tk.Scrollbar(self.frame_inputs)
        self.tree_seriesize = ttkwidgets.CheckboxTreeview(self.frame_inputs, yscrollcommand=self.scroll_seriesize.set, columns=2)  # Not sure about this column property?
        self.label_poles = tk.Label(self.frame_inputs, text='Motor Poles')
        self.scroll_poles = tk.Scrollbar(self.frame_inputs)
        self.tree_poles = ttkwidgets.CheckboxTreeview(self.frame_inputs, yscrollcommand=self.scroll_poles.set, columns=2)  # What is the columns property doing?
        self.label_spd = tk.Label(self.frame_inputs, text='Speed (rpm)')
        self.entry_spd = tk.Entry(self.frame_inputs, width=entry_width)
        self.label_spd_updown = tk.Label(self.frame_inputs, text='+/-')
        self.entry_spd_tol = tk.Entry(self.frame_inputs, width=entry_width)
        self.label_spd_perc = tk.Label(self.frame_inputs, text='%')
        self.label_trq = tk.Label(self.frame_inputs, text='Torque (Nm)')
        self.entry_trq = tk.Entry(self.frame_inputs, width=entry_width)
        self.label_trq_updown = tk.Label(self.frame_inputs, text='+/-')
        self.entry_trq_tol = tk.Entry(self.frame_inputs, width=entry_width)
        self.label_trq_perc = tk.Label(self.frame_inputs, text='%')
        self.label_safety = tk.Label(self.frame_inputs, text='Safety Factor')
        self.entry_safety = tk.Entry(self.frame_inputs, width=entry_width)
        # To position all the widgets within the grid
        self.label_seriesize.grid(row=0, column=0, columnspan=5, padx=pad_ext, pady=pad_ext)
        self.scroll_seriesize.grid(row=1, column=4, padx=pad_ext, pady=pad_ext, sticky='ns')
        self.tree_seriesize.grid(row=1, column=0, columnspan=4, padx=pad_ext, pady=pad_ext)
        self.label_poles.grid(row=2, column=0, columnspan=5, padx=pad_ext, pady=pad_ext)
        self.scroll_poles.grid(row=3, column=4, padx=pad_ext, pady=pad_ext, sticky='ns')
        self.tree_poles.grid(row=3, column=0, columnspan=4, padx=pad_ext, pady=pad_ext)
        self.label_spd.grid(row=4, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_spd.grid(row=4, column=1, padx=pad_ext, pady=pad_ext)
        self.label_spd_updown.grid(row=4, column=2, padx=pad_ext, pady=pad_ext)
        self.entry_spd_tol.grid(row=4, column=3, padx=pad_ext, pady=pad_ext)
        self.label_spd_perc.grid(row=4, column=4, padx=pad_ext, pady=pad_ext)
        self.label_trq.grid(row=5, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_trq.grid(row=5, column=1, padx=pad_ext, pady=pad_ext)
        self.label_trq_updown.grid(row=5, column=2, padx=pad_ext, pady=pad_ext)
        self.entry_trq_tol.grid(row=5, column=3, padx=pad_ext, pady=pad_ext)
        self.label_trq_perc.grid(row=5, column=4, padx=pad_ext, pady=pad_ext)
        self.label_safety.grid(row=6, column=0, padx=pad_ext, pady=pad_ext)
        self.entry_safety.grid(row=6, column=1, padx=pad_ext, pady=pad_ext)
        # To enable the scrolling of the two trees
        self.scroll_seriesize.config(command=self.tree_seriesize.yview)
        self.scroll_poles.config(command=self.tree_poles.yview)
        
        # To generate all the series and sizes in the selection tree
        series_sizes = {'VF_W':[], 'A':[], 'C':[], 'F':[]}
        for series_size in series_sizes:
            workbook = openpyxl.load_workbook(f'{series_size}_Gearboxes.xlsx')
            sheets =  workbook.worksheets
            for sheet in sheets:
                series_size_name = sheet['A2'].value
                series_size_shaft = sheet['O1'].value
                series_size_shaft_alt = sheet['P1'].value
                if series_size_shaft_alt is not None:
                    series_sizes[series_size].append(f'{series_size_name}    ({series_size_shaft}mm, {series_size_shaft_alt}mm)')
                else:
                    series_sizes[series_size].append(f'{series_size_name}    ({series_size_shaft}mm)')
        # To insert all these sizes into the tree
        for key in series_sizes:
            self.tree_seriesize.insert('', 'end', key, text=key)
            for value in series_sizes[key]:
                self.tree_seriesize.insert(key, 'end', value, text=value)
        # To Generate all the motor pole options in that selection tree
        for poles in ['2 Pole', '4 Pole', '6 Pole', '8 Pole']:
            self.tree_poles.insert('', 'end', poles, text=poles)
        

        # Widgets in the Recommend tab input frame
        self.scroll_reco = tk.Scrollbar(self.frame_outputs)
        self.list_reco = tk.Listbox(self.frame_outputs, width=130, height=30, yscrollcommand=self.scroll_reco.set)
        self.button_reco = tk.Button(self.frame_outputs, text='Generate Recommendations', command=lambda:self.postOutputs())
        # And their positioning
        self.scroll_reco.grid(row=0, column=1, padx=pad_ext, pady=pad_ext, sticky='ns')
        self.list_reco.grid(row=0, column=0, padx=pad_ext, pady=pad_ext)
        self.button_reco.grid(row=1, column=0, columnspan=2, padx=pad_ext, pady=pad_ext)
        # Configs for various things
        self.scroll_reco.config(command=self.list_reco.yview)
        self.list_reco.config(font=font.Font(size=11))
    

    def retrieveInputs(self):
        # To get all the raw data from the GUI
        self.spd = self.entry_spd.get()
        self.spd_tol = self.entry_spd_tol.get()
        self.trq = self.entry_trq.get()
        self.trq_tol = self.entry_trq_tol.get()
        self.safety = self.entry_safety.get()
        self.raw_series_sizes = self.tree_seriesize.get_checked()
        self.poles = self.tree_poles.get_checked()
        
        # To make the series size info into a useful list
        self.series_sizes = {'VF_W':[], 'A':[], 'C':[], 'F':[]}
        replacement = str.maketrans(string.punctuation, ' '*32)
        for serie_size in self.raw_series_sizes:
            no_punc = serie_size.translate(replacement)
            name = re.search(r'[A-Z]+ [A-Z]+ [0-9]+ [0-9]+|[A-Z]+ [0-9]+', no_punc).group()
            if (name[0] == 'V' or name[0] == 'W'):
                self.series_sizes['VF_W'].append(name)
            elif (name[0] == 'A'):
                self.series_sizes['A'].append(name)
            elif (name[0] == 'C'):
                self.series_sizes['C'].append(name)
            elif (name[0] == 'F'):
                self.series_sizes['F'].append(name)

        # Dictionary of all the input information
        inputs = {
        'spd': float(self.spd),
        'spd_tol': float(self.spd_tol),
        'trq': float(self.trq),
        'trq_tol': float(self.trq_tol),
        'safety': float(self.safety),
        'series_sizes': self.series_sizes,
        'poles': self.poles
        }

        return inputs


    def postOutputs(self):
        inputs = self.retrieveInputs()
        self.list_reco.delete(0, tk.END)

        gearedmotors = make_recommendations(inputs)
        for gearedmotor in gearedmotors:
            self.list_reco.insert(tk.END, gearedmotor.printData()[0])
            self.list_reco.insert(tk.END, gearedmotor.printData()[1])
            self.list_reco.insert(tk.END, gearedmotor.printData()[2])
            self.list_reco.insert(tk.END, '')
