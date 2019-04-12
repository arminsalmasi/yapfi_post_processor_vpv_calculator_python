from get_input import Indata
from equilibrium_calculator import Equilibrium
import time
import concurrent.futures

def main():
    path = '/home/salmasi/Documents/workdir/8-LM-7_B'
    rawData = Indata(path)
    rawData.get_files()
    phaseNames = {'thermodynamics':rawData.phaseNames[0:], 'kinetics':rawData.phaseNames[0]}
    conditions = { \
        'databases':['TCFE8','', 'MOBFE4', ''], \
        'elementNames':rawData.elementNames, \
        'phaseNames':phaseNames, \
        'N':1,'P':1e5,'T':1723.15, \
        'compositions':rawData.moleFractions, \
        'ementalConditions':[['C','Co','Ti','N'],[0,1,2,3],['X','X','X','X'],[],[]] }    #ementalConditions':[[elname],[index],[variables X W Ac ACP],[activity value],[reference phase]] \  '''
    

    equilibriumCalculator_parallel = Equilibrium(conditions)
    equilibriumCalculator_parallel.do_parallel_calculator()

    equilibriumCalculator_mono = Equilibrium(conditions)
    r = equilibriumCalculator_mono.do_calculate()   


    #conditionsParallel = []
    #for gridPoint in range(rawData.numberOfGridPoints):
    #    compositions = rawData.moleFractions[gridPoint*rawData.numberOfElements:(gridPoint+1)*rawData.numberOfElements]
    #    conditionsParallel.append({ \
    #    'databases':['TCFE8','', 'MOBFE4', ''], \
    #    'elementNames':rawData.elementNames, \
    #    'phaseNames':phaseNames, \
    #    'N':1,'P':1e5,'T':1723.15, \
    #    'compositions':compositions, \
    #    'ementalConditions':[['C','Co','Ti','N'],[0,1,2,3],['X','X','X','X'],[],[]] })
    #calculator = Equilibrium(conditionsParallel)
    #results = calculator.do_parallle_calculator()



if __name__  == "__main__":
    main() 







""" 


import os
import numpy as np
import re
from get_input import Indata
#from equilibrium_calculator import Equilibrium
from tc_python import *
import matplotlib.pyplot as plt



def main():
    path = '/home/salmasi/Documents/workdir/8-LM-7_B'
    poly3Path = '/home/salmasi/Documents/databases/1.POLY3'
    thermodynamicDatabase, kineticDatabase = 'TCFE8', 'MOBFE4'
    databases = [thermodynamicDatabase,kineticDatabase]
    equilibriumConditions = {'N':1, 'P':1e5, 'T':1723.15, 'X':[0,1,2,3]}
    rawData = Indata(path)
    rawData.get_files()
    phaseNames = [rawData.phaseNames,rawData.phaseNames[1]]
    


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
        print(initialized_system.get_phases_in_system())
        
        calculations = initialized_system.with_single_equilibrium_calculation()
        if 'T' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.temperature(), equilibriumConditions['T'])
        if 'P' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.pressure(), equilibriumConditions['P'])
        if 'N' in equilibriumConditions:
            calculations.set_condition(ThermodynamicQuantity.system_size(), equilibriumConditions['N'])   
        for gridPoint in range(rawData.numberOfGridPoints):
            if 'X' in equilibriumConditions:
                for element in equilibriumConditions['X']:                    
                    calculations.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(rawData.elementNames[element]),rawData.moleFractions[gridPoint * rawData.numberOfElements+element])
            calc_res = calculations.calculate()
            stable_phases = (calc_res.get_stable_phases())
            stable_conditions = (calc_res.get_conditions())
            
           # for element in element_names:
           #         #calc_mf.append(calc_res.get_value_of('x({})'.format(element)))
           #         mf_out.append(calc_res.get_value_of('x({})'.format(element)))
           #         #wf.append(calc_res.get_value_of('w({})'.format(element)))
           #         wf_out.append(calc_res.get_value_of('w({})'.format(element)))
           #     for phase in stable_phases:
           #         vpv_out.append(calc_res.get_value_of('vpv({})'.format(phase)))
           #         npm_out.append(calc_res.get_value_of('npm({})'.format(phase)))
           #     for binary in binary_list:
           #         x_ph_out.append(calc_res.get_value_of('x({},{})'.format(binary[0], binary[1])))
           #     for binary in binary_list:
           #         try:
           #             y_ph_out.append(calc_res.get_value_of('y({},{})'.format(binary[0], binary[1])))
           #         except Exception as error:
           #             print('y({},{})=error'.format(binary[0], binary[1]))
           #             y_ph_out.append(-1)
    
    for element in range(rawData.numberOfElements):
        plt.plot(rawData.moleFractions[element::rawData.numberOfElements])
        plt.ylabel('some numbers')
    plt.show()


    a = 1        


    #equilibrium_results = Equilibrium(databases, phaseNames, rawData.elementNames, equilibriumConditions, rawData.moleFractions)


        
        
    

if __name__  == "__main__":
    main() """
