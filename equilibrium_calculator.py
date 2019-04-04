from tc_python import *
import itertools as itertool

class Equilibrium:

    ''' input '''
    databases = 0 
    phaseNames = 0
    elementNames = 0
    equilibriumConditions = 0 
    fractions = 0
    ''' output '''
    moleFractions = 0
    moleFractionsInPhases = 0
    numberOfMoles = 0
    numberOfMolesInPhases = 0 
    uFractions = 0 
    ufractionsInPhases = 0
    volumeFractions = 0
    volumeFractionFromUFractions = 0
    phaseFractions = 0 
    mobilities = 0
    chemicalPotentials = 0 
    yFractions = 0 

    ''' databases = (thermodybnamics; kinetics)
        phaseNames = (thermodybnamics; kinetics)
        elementNames = (names; substitutional index(0,1))
        equilibriumConditions = 
            Dictionary (N,P,T,X,W,N,Ac,
            [a list of elements with the specific condition = value from fractions]
            if condition =AC then value:real) 
    '''
    def __init__(self, databases, phaseNames, elementNames, equilibriumConditions, fractions):
        self.databases =  databases
        self.phaseNames = phaseNames
        self.elementNames = elementNames
        self.equilibriumConditions = equilibriumConditions
        self.fractions = fractions
#
#
    #def calculate_equilibrium(self):
    #    with TCPython() as tc:
    #        initial_system = tc.select_database_and_elements(self.databases[0], self.elementNames).without_default_phases()
    #        for phase in self.phaseNames[0][:]:
    #            initial_system.select_phase(phase)       
    #        initial_system.select_database_and_elements(self.databases[1], self.elementNames).without_default_phases()
    #        for phase in self.phaseNames[1][:]:
    #            initial_system.select_phase(phase)
    #        system = initial_system.get_system()
    #        calc = system.with_single_equilibrium_calculation()
    #        
    #        calc.set_condition(ThermodynamicQuantity.temperature(), tempera)
    #        calc.set_condition(ThermodynamicQuantity.pressure(), press)
    #        for gp in range(ngd):
    #            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" + " grid point= ", str(gp))
    #            cnt = 1
    #            for element in element_names[0:-1]:
    #                calc.set_condition(ThermodynamicQuantity.mole_fraction_of_a_component((element)), mf_in[cnt][gp])
    #                cnt += 1
    #            calc_res = calc.calculate()
    #            stable_phases = calc_res.get_stable_phases()
    #            binary_list = list(itertool.product(stable_phases, element_names))
    #            for element in element_names:
    #                #calc_mf.append(calc_res.get_value_of('x({})'.format(element)))
    #                mf_out.append(calc_res.get_value_of('x({})'.format(element)))
    #                #wf.append(calc_res.get_value_of('w({})'.format(element)))
    #                wf_out.append(calc_res.get_value_of('w({})'.format(element)))
    #            for phase in stable_phases:
    #                vpv_out.append(calc_res.get_value_of('vpv({})'.format(phase)))
    #                npm_out.append(calc_res.get_value_of('npm({})'.format(phase)))
    #            for binary in binary_list:
    #                x_ph_out.append(calc_res.get_value_of('x({},{})'.format(binary[0], binary[1])))
    #            for binary in binary_list:
    #                try:
    #                    y_ph_out.append(calc_res.get_value_of('y({},{})'.format(binary[0], binary[1])))
    #                except Exception as error:
    #                    print('y({},{})=error'.format(binary[0], binary[1]))
    #                    y_ph_out.append(-1)
    #    return mf_out, wf_out, vpv_out, npm_out, y_ph_out, x_ph_out
##