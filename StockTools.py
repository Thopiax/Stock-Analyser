#!/usr/bin/env

def readFile(sep=",",file="log.txt"): #Name of the file, Seperator of data, Boolean to see if file is a .config
    
    global valor_list
    global read
    
    valor_list = []
    read = ''
    data_file = True

    with open(file,'r') as data:
        
        try:
            read = data.readlines()[-1]
        except IndexError:
            data_file = False
            return data_file

        valor_list = read.split(sep)

def writeFile(text, log="log.txt", form = 'a',end = ','):

        with open(log,form) as data:
            data.write(text + end)

def setVariacao(start,end):
	var = ((start - end) / end)* 100.
	return var