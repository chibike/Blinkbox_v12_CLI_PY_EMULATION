import os

def fileParseCsvData(filename):
    try:
        with open(filename, 'r') as file:
            f = file.read()
            file.close()
            p = f.split(',')
            return p
    except TypeError:
        return ["Error"]

def processListDirCmd( options, currentDir ):
    if options == '':
        runListDir( curentDir )
    

def runListDir( curentDir ):
    pass
