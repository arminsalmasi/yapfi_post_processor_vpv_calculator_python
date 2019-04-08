from tc_python import *
import itertools as itertool
import concurrent.futures
import time

class Equilibrium:
    ''' i / o '''
    eqConditions, eqState = 0, 0

    def __init__(self, eqConditions):
        self.eqConditions = eqConditions
        
    def do_calculate(self):
        phaseNames, userDatabse = [], [False,False]
        tempPhaseNames = self.eqConditions['phaseNames']
        databases = self.eqConditions['databases']
        elementNames = self.eqConditions['elementNames']
        if databases[1] == 'user':
            userDatabse[0] = True
        if databases[3] == 'user':
            userDatabse[1] = True
        for n, key in enumerate(['thermodynamics','kinetics']):
            phaseNames.append(tempPhaseNames[key] if isinstance(tempPhaseNames[key],list) else [tempPhaseNames[key]])      
        with TCPython() as tc:
            tc.set_cache_folder(os.path.basename(__file__) + "_cache")
            if not(userDatabse[0]):
                thermokinetcData = tc.select_database_and_elements(databases[0], elementNames).without_default_phases()
                for phase in phaseNames[0][:]:
                    thermokinetcData.select_phase(phase)   
                    print(phase)
            else:
                thermokinetcData = tc.select_user_database_and_elements(databases[0], elementNames).without_default_phases()
                for phase in phaseNames[0][:]:
                    thermokinetcData.select_phase(phase)      
            if not(userDatabse[1]):
                thermokinetcData.select_database_and_elements(databases[2], elementNames).without_default_phases()
                for phase in phaseNames[1][:]:
                    thermokinetcData.select_phase(phase)  
                    print(phase)
            else:
                thermokinetcData.select_user_database_and_elements(databases[2], elementNames).without_default_phases()
                for phase in phaseNames[1][:]:
                    thermokinetcData.select_phase(phase)      
            start = time.time()    
            fetched_data = thermokinetcData.get_system() 
            print(fetched_data.get_phases_in_system())
            calculation =  fetched_data.with_single_equilibrium_calculation()
            for key in self.eqConditions:
                if key == 'T':
                    calculation.set_condition(ThermodynamicQuantity.temperature(), self.eqConditions['T'])
                if key == 'P':
                    calculation.set_condition(ThermodynamicQuantity.pressure(), self.eqConditions['P'])
                if key == 'N':
                    calculation.set_condition(ThermodynamicQuantity.system_size(), self.eqConditions['N'])  
            r=[]
            for gridPoint in range(len(self.eqConditions['compositions']) // len(elementNames)):
                compositions = self.eqConditions['compositions'][gridPoint*len(elementNames):(gridPoint+1)*len(elementNames)]
                indices =  self.eqConditions['ementalConditions'][1]
                for n, element in enumerate(self.eqConditions['ementalConditions'][0]):                       
                    if self.eqConditions['ementalConditions'][2][n] == 'X':
                        calculation.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element),compositions[indices[n]])
                    if self.eqConditions['ementalConditions'][2][n] == 'W':
                        calculation.set_condition(ThermodynamicQuantity.mass_fraction_of_a_component(element),compositions[indices[n]])
                    if self.eqConditions['ementalConditions'][2][n] == 'AC':                   
                        calculation.set_condition(ThermodynamicQuantity.activity_of_component(element),self.eqConditions['ementalConditions'][3][n])
                r.append(calculation.calculate().get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase('liquid')))
                print(gridPoint)
            print(r)
        return r

        end = time.time()
        print('timelog single tread 2 ',end-start)



    def do_parallel(self):
        phaseNames, userDatabse = [], [False,False]
        tempPhaseNames = self.eqConditions['phaseNames']
        databases = self.eqConditions['databases']
        elementNames = self.eqConditions['elementNames']
        if databases[1] == 'user':
            userDatabse[0] = True
        if databases[3] == 'user':
            userDatabse[1] = True
        for n, key in enumerate(['thermodynamics','kinetics']):
            phaseNames.append(tempPhaseNames[key] if isinstance(tempPhaseNames[key],list) else [tempPhaseNames[key]])      
        with TCPython() as tc:
            tc.set_cache_folder(os.path.basename(__file__) + "_cache")
            if not(userDatabse[0]):
                thermokinetcData = tc.select_database_and_elements(databases[0], elementNames).without_default_phases()
                for phase in phaseNames[0][:]:
                    thermokinetcData.select_phase(phase)   
                    print(phase)
            else:
                thermokinetcData = tc.select_user_database_and_elements(databases[0], elementNames).without_default_phases()
                for phase in phaseNames[0][:]:
                    thermokinetcData.select_phase(phase)      
            if not(userDatabse[1]):
                thermokinetcData.select_database_and_elements(databases[2], elementNames).without_default_phases()
                for phase in phaseNames[1][:]:
                    thermokinetcData.select_phase(phase)  
                    print(phase)
            else:
                thermokinetcData.select_user_database_and_elements(databases[2], elementNames).without_default_phases()
                for phase in phaseNames[1][:]:
                    thermokinetcData.select_phase(phase)      
            fetched_data = thermokinetcData.get_system() 
            print(fetched_data.get_phases_in_system())
            calculation =  fetched_data.with_single_equilibrium_calculation()
            for key in self.eqConditions:
                if key == 'T':
                    calculation.set_condition(ThermodynamicQuantity.temperature(), self.eqConditions['T'])
                if key == 'P':
                    calculation.set_condition(ThermodynamicQuantity.pressure(), self.eqConditions['P'])
                if key == 'N':
                    calculation.set_condition(ThermodynamicQuantity.system_size(), self.eqConditions['N'])  
            indices =  self.eqConditions['ementalConditions'][1]
            for n, element in enumerate(self.eqConditions['ementalConditions'][0]):                       
                if self.eqConditions['ementalConditions'][2][n] == 'X':
                    calculation.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component(element),compositions[indices[n]])
                if self.eqConditions['ementalConditions'][2][n] == 'W':
                    calculation.set_condition(ThermodynamicQuantity.mass_fraction_of_a_component(element),compositions[indices[n]])
                if self.eqConditions['ementalConditions'][2][n] == 'AC':                   
                    calculation.set_condition(ThermodynamicQuantity.activity_of_component(element),self.eqConditions['ementalConditions'][3][n])
            r = calculation.calculate().get_value_of(ThermodynamicQuantity.mole_fraction_of_a_phase('liquid'))
        return r

    def do_parallle_calculator(self):
        start = time.time()    
        results = []
        processes = 8
        temp = self.eqConditions
        with concurrent.futures.ProcessPoolExecutor(processes) as executor:
            for out in executor.map(self.do_parallel, temp):
                results.append(out)
        end = time.time()
        print('timelog parallel 1',end-start)
        print(results)
        return results