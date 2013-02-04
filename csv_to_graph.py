# Time: 7 hrs, 45 min
import os
import csv
import pylab
import tempfile
from Tkinter import *

# Goal: automatically process multiple CSV files into scatterplots
# Outline: For each csv file in a folder, process into scatterplot, save in
# another folder

def read(filename):
    '''
    filename - string of the path of a csv file
    Output - (list of x values, list of y values, date)
    Opens file and extracts x_values, y_values, and date
    '''
    f = open(filename)
    linelist = f.readlines()
    
    x_data = []
    y_data = []
    # in case there is no date, or wrong formatting
    name = filename
    # for each line in linelist, convert to a list of ascii numbers,
    # remove blankspace, newline, etc. characters
    # then turn that list back to a string
    for line in linelist:
        converted_line = []
        for l in line:
            converted_line.append(ord(l))
        converted_line = filter(lambda a: a!=0 and a != 13 and a !=10, converted_line)
        new_line = []
        for j in converted_line:
            new_line.append(chr(j))
        # convert new_line to a string
        string_line = ''.join(new_line)
        # convert string to list
        line_data=string_line.split(',')
        # removes blank lines
        if line_data == []:
            continue
        try:
            x_data.append(float(line_data[0]))
            y_data.append(float(line_data[1]))
        except:
            # checks exceptions if they are date, and if they are, make that
            # name
            if line_data[0] == 'Date:':
                name = line_data[1]
    return (x_data, y_data, name)

# Now, take the tuples we processed before, and graph it
def graph(data_tuple, name, output):
    '''
    data_tuple - a tuple of (x values, y values, name), obtained from read(filename)
    name - filename of saved scatterplot
    output - output folder
    Uses pylab to make a scatterplot with blue diamonds for data points
    with a blue line connecting them
    Saves scatterplot to folder in png format
    '''
    pylab.figure()
    pylab.plot(data_tuple[0], data_tuple[1], 'b.-')
    pylab.suptitle(data_tuple[2])
    pylab.xlabel('Wavelength in nm')
    pylab.ylabel('Absorption')
    out_path = output+'/'+name
    pylab.savefig(out_path)
    return
    

def mult(in_file, out_file):
    '''
    in_file - string of path to folder containg only CSV files
    out_file - string of path to folder to save png graphs
    Processes all .csv files in one folder and saves them as png graphs in
    out_file
    '''
    for path, dirs, files, in os.walk(in_file):
        for f in files:
            filepath = path+'/'+f
            data = read(filepath)
            # create name of png by truncating last 4 characters of filename
            name = f[:-4]
            graph(data, name, out_file)

# GUI
# Asks for string of in_file and out_file
class ProcessCSV:
    '''
    GUI for software. Produces a popup box with a label, two entry boxes and
    a button which submits filepaths to mult.
    '''
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        Label(master, text='This software will process .csv files into scatterplots.\n\
Please ensure that the input file contains only .csv files \n and that you have spelled \
the names of the file paths correctly.').pack()
        self.entry1 = Entry(master, width = 50)
        self.entry1.pack()
        self.entry1.insert(0, 'Type input folder here.')
        self.entry2 = Entry(master, width = 50)
        self.entry2.pack()
        self.entry2.insert(0, 'Type output folder here.')
        self.button = Button(master, text='Submit', command=self.process)
        self.button.pack()

    def process(self):
        in_file = self.entry1.get()
        out_file = self.entry2.get()
        mult(in_file, out_file)

if __name__ == '__main__' :
    root = Tk()
    p = ProcessCSV(root)
    root.mainloop()
