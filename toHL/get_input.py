import numpy as np
import os

class Indata:
    
    moleFractions = 0;
    timeList = 0;
    elementNames = 0;
    phaseNames = 0;
    numberOfElements = 0;
    numberOfPhases = 0;
    numberOfGridPoints = 0;


    def __init__(self, path):
        self.path = path

    def get_files(self):
        fname = ''.join(self.path + '/MOLE_FRACTIONS.TXT')
        with open(fname, 'r') as f:
            self.moleFractions = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(self.path + '/TIME.TXT')
        with open(fname, 'r') as f:
            self.timeList = np.array([float(line) for line in f])
        f.close()
        fname = ''.join(self.path + '/ELEMENT_NAMES.TXT')
        with open(fname, 'r') as f:
            self.elementNames = f.read().split()
        f.close()	
        fname = ''.join(self.path + '/PHASE_NAMES.TXT')
        with open(fname, 'r') as f:
            self.phaseNames = f.read().split()
        f.close()
        self.numberOfElements = np.size(self.elementNames)
        self.numberOfPhases = np.size(self.phaseNames)
        self.numberOfGridPoints = round(np.size(self.moleFractions)/self.numberOfElements/np.size(self.timeList))