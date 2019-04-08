import concurrent.futures
from pylab import *
from tc_python import *
from get_input import Indata
import time

def do_step(param):
    with TCPython() as tc:
        #tc.set_cache_folder(os.path.basename(__file__) + "_cache")
        init = tc.select_database_and_elements(param['databases'], param['elementNames']).without_default_phases()
        for phase in param['phaseNames']:
            init.select_phase(phase)       
        system = init.get_system()
        print(system.get_phases_in_system())
        calculations = system.with_single_equilibrium_calculation()
        calculations.set_condition(ThermodynamicQuantity.temperature(), param['T'])
        calculations.set_condition(ThermodynamicQuantity.pressure(), param['P'])
        calculations.set_condition(ThermodynamicQuantity.system_size(), param['N'])   
        for n, element in enumerate(param['conditionsElementNames']):                    
            calculations.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element),param['compositions'][n] )
        r = calculations.calculate().get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase('liquid'))
    return r

def do_step_non_functional(param):
    calculations = param['data']
    for n, element in enumerate(param['conditionsElementNames']):                    
        calculations.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element),param['compositions'][n] )
    r = calculations.calculate().get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase('liquid'))
    return r


if __name__ == "__main__":
    path = '/home/salmasi/Documents/workdir/8-LM-7_B'
    poly3Path = '/home/salmasi/Documents/databases/1.POLY3'
    thermodynamicDatabase, kineticDatabase = 'TCFE8', 'MOBFE4'
    databases = [thermodynamicDatabase,kineticDatabase]
    equilibriumConditions = {'N':1, 'P':1e5, 'T':1723.15}
    conditionsElementIndex = [0,1,2,3]
    conditionsElementNames = ['C','Co','Ti','N']
    rawData = Indata(path)
    rawData.get_files()    
    phaseNames = [rawData.phaseNames,rawData.phaseNames[1]]
    databases ='TCFE8'
    phaseNames = rawData.phaseNames
    keys = ['databases','elementNames','phaseNames','N','P','T','compositions','conditionsElementNames','data']
    
    parameter={}
    parameters=[]
    for gridPoint in range(rawData.numberOfGridPoints):
        for key in keys:
            if key == 'databases':
                parameter[key] = databases
            if key == 'elementNames':
                parameter[key] = rawData.elementNames
            if key == 'phaseNames':
                parameter[key] = phaseNames
            if key == 'conditionsElementNames':
                parameter[key] = conditionsElementNames
            if key == 'compositions':
                gridComposition = rawData.moleFractions[gridPoint* rawData.numberOfElements:(gridPoint+1)* rawData.numberOfElements-1]
                parameter[key] = gridComposition[conditionsElementIndex]
            if key in equilibriumConditions:
                parameter[key] = equilibriumConditions[key]
        parameters.append(dict(parameter))

    ''' single tread 1 '''
    start = time.time()    
    for gridPoint in range(rawData.numberOfGridPoints):            
        print(gridPoint)
        out1 = do_step(parameters[gridPoint])
        print(out1)
    end = time.time()
    print('timelog single tread 1 ',end-start)
    ''' parallel 1'''
    start = time.time()    
    results = []
    processes = 8
    with concurrent.futures.ProcessPoolExecutor(processes) as executor:
        for out1 in executor.map(do_step, parameters):
            results.append(out1)
    print(results)
    end = time.time()
    print('timelog parallel 1',end-start)


    ''' single tread 1'''
    parameter2={}
    parameters2=[]
    start = time.time()    
    with TCPython() as tc:
        #tc.set_cache_folder(os.path.basename(__file__) + "_cache")
        init = tc.select_database_and_elements(databases, rawData.elementNames).without_default_phases()
        for phase in phaseNames:
            init.select_phase(phase)       
        system = init.get_system()
        calculations = system.with_single_equilibrium_calculation()
        calculations.set_condition(ThermodynamicQuantity.temperature(), equilibriumConditions['T'])
        calculations.set_condition(ThermodynamicQuantity.pressure(), equilibriumConditions['P'])
        calculations.set_condition(ThermodynamicQuantity.system_size(), equilibriumConditions['N'])   

        for gridPoint in range(rawData.numberOfGridPoints):
            for key in keys:
                if key == 'conditionsElementNames':
                    parameter2[key] = conditionsElementNames
                if key == 'compositions':
                    gridComposition = rawData.moleFractions[gridPoint* rawData.numberOfElements:(gridPoint+1)* rawData.numberOfElements-1]
                    parameter2[key] = gridComposition[conditionsElementIndex]
                if key in equilibriumConditions:
                    parameter2[key] = equilibriumConditions[key]
                if key == 'data':
                    parameter2[key] = calculations
            parameters2.append(dict(parameter2))
        
        for gridPoint in range(rawData.numberOfGridPoints):            
            out2 = do_step_non_functional(parameters2[gridPoint])
            print(out2)
        end = time.time()
        print('timelog single tread 2 ',end-start)

        
        ''' parallel 2'''
        start = time.time()    
        results = []
        processes = 8
        with concurrent.futures.ProcessPoolExecutor(processes) as executor:
            for out2 in executor.map(do_step_non_functional, parameters2):
                results.append(out2)
        print(results)
        end = time.time()
        print('timelog parallel 2',end-start)
    