import os
import numpy as np
import re
from get_input import Indata
#from equilibrium_calculator import Equilibrium
from tc_python import *



def main():
    path = '/home/salmasi/Documents/workdir/8-LM-7_B'
    poly3Path = '/home/salmasi/Documents/databases/1.POLY3'
    thermodynamicDatabase, kineticDatabase = 'TCFE8', 'MOBFE4'
    databases = [thermodynamicDatabase,kineticDatabase]
    equilibriumConditions = {'N':1, 'P':1e5, 'T':1723.15, 'X':[0,1,2,3]}
    rawData = Indata(path)
    rawData.get_files()
    phaseNames = [rawData.phaseNames,rawData.phaseNames[1]]
    #equilibrium_results = Equilibrium(databases, phaseNames, rawData.elementNames, equilibriumConditions, rawData.moleFractions)
    with TCPython() as tc:
        data_initializer = tc.select_database_and_elements(databases[0], rawData.elementNames).without_default_phases()
        thermodynamicPhases = phaseNames[0]
        thermodynamicPhases = thermodynamicPhases if isinstance(thermodynamicPhases,list) else [thermodynamicPhases]
        for phase in thermodynamicPhases:
            data_initializer.select_phase(phase)       
        
        data_initializer.select_database_and_elements(databases[1], rawData.elementNames).without_default_phases()
        kineticPhases = phaseNames[1]
        kineticPhases = kineticPhases if isinstance(kineticPhases,list) else [kineticPhases]
        for phase in kineticPhases:
            data_initializer.select_phase(phase)
        initialized_system = data_initializer.get_system()
        calculations = initialized_system.with_single_equilibrium_calculation()
        if 'T' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.temperature(), equilibriumConditions['T'])
        if 'P' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.pressure(), equilibriumConditions['P'])
        if 'N' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.system_size(), equilibriumConditions['N'])
        #print((rawData.numberOfGridPoints))       
        for gridPoint in range(rawData.numberOfGridPoints):
            if 'X' in equilibriumConditions:
                for element in equilibriumConditions['X']:                    
                    #print(rawData.elementNames[element])
                    #print(gridPoint*rawData.numberOfElements+element)
                    #print(rawData.moleFractions[gridPoint*rawData.numberOfElements+element])
                    calculations.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(rawData.elementNames[element]),rawData.moleFractions[gridPoint * rawData.numberOfElements+element] )
            print('%%%%%%%%%%%%%%%%%%')
            calc_res = calculations.calculate()
            stable_phases = calc_res.get_stable_phases()
            stable_conditions = calc_res.get_conditions()
            print(stable_phases)
            print(stable_conditions)
        a=1
        


        
        
        
        #equilibriumConditions
        # print(equilibriumConditions[1])
        
        #calc.set_condition(ThermodynamicQuantity.temperature(), tempera)
    
    a = 1
if __name__  == "__main__":
    main()
