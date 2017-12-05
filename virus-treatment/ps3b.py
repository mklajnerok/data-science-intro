# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
import numpy

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.birthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.birthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        tempProb = random.random()
        if tempProb <= self.clearProb:
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        
        tempProb = random.random()
        if tempProb <= self.birthProb * (1 - popDensity):
            offspring = SimpleVirus(self.birthProb, self.clearProb)
            return offspring
         
        else:
            raise NoChildException
        
#TESTING
#random.seed(0)
#virus1 = SimpleVirus(1.0, 1.0)
#print(virus1.getClearProb())
#print(virus1.getMaxBirthProb())
#print (virus1.doesClear())
#popDensity = 0.7
#print(virus1.reproduce(popDensity))


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.
        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        livingVir = []
        for vir in self.viruses:
            if vir.doesClear() == False:
                livingVir.append(vir)
        
        popDensity = len(livingVir)/self.getMaxPop()
        
        newVir = []
        for vir in livingVir:
            try:
                newVir.append(vir.reproduce(popDensity))
            except NoChildException:
                continue
        self.viruses = livingVir + newVir
        
        return self.getTotalPop()
        
# TESTING
#random.seed(0)
#vir1 = SimpleVirus(0.3, 0.2)
#vir2 = SimpleVirus(0.3, 0.9)
#vir3 = SimpleVirus(0.9, 0.3)
#human1 = Patient([vir1, vir2, vir3], 5)
#print(human1.getMaxPop())
#print(human1.getTotalPop())
#print(human1.getViruses())
#print(human1.update())


def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    
    virusesList = []
    for i in range(numViruses):
        virusesList.append(SimpleVirus(maxBirthProb, clearProb))
       
    popSize = [0]*300
    
    for trial in range(numTrials):
        human1 = Patient(virusesList, maxPop)
        for step in range(300):
            popSize[step] += (human1.update())

    for i in range(len(popSize)):
        popSize[i] = popSize[i]/numTrials
   
    pylab.plot(popSize, label = 'human1')
    pylab.title('Average Population Size over time')
    pylab.xlabel('number od time steps')
    pylab.ylabel('average population')
    pylab.legend(loc = 'best')
    pylab.show()
           

#TESTING
#numViruses = 100
#maxPop = 1000
#maxBirthProb = 0.1
#clearProb = 0.05
#numTrials = 50
#print(simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials))


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistance = resistances
        self.mutProb = mutProb

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistance

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in ResistantVirus.getResistances(self).keys():
            if ResistantVirus.getResistances(self)[drug]:
                return True
            else:
                return False
        else:
            self.resistance[drug] = False
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        #spr czy się rozmnaża
        #dojdzie do tego jeli jest odporny na wszystkie leki z listy activeDrugs
        resTest = 0
        if activeDrugs == []:
            resTest = 1
        else:
            for drug in activeDrugs:
                if ResistantVirus.isResistantTo(self,drug):
                    resTest = 1
                else:
                    resTest = 0
         
        #dodatkowo prawd rozmnożenia wynosi self.maxBirthProb * (1 - popDensity)
        tempProb = random.random()
        #print (tempProb)
        if tempProb <= self.getMaxBirthProb() * (1-popDensity) and resTest == 1:
            newRes = self.resistance.copy()    
            #dla kazdego leku na liscie odpornosci wirusa, czyl dla klucza
            for drug in self.resistance:
                tempProb2 = random.random()
            # istnije prawd 1-mutProb ze nie bedzie zmiany
            #istnieje prawd mutProb ze nastapi zmiana odpornosci
                if self.mutProb >= tempProb2:
                    newRes[drug] = not ResistantVirus.getResistances(self)[drug]
                    #print(newRes)
                else:
                    newRes[drug] = ResistantVirus.getResistances(self)[drug]
            #jełi się rozmnaża to tworzy instancje klasy z takimi samymi 3 parametr
            #print(newRes)
            offspring = ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), newRes, self.mutProb)
            return offspring
         
        else:
            raise NoChildException   

# TESTING
#random.seed(0)
#vir4 = ResistantVirus(0.3, 0.2, {'aaa': True, 'bbb':False}, 0.5)
#vir4 = ResistantVirus(1.0, 0.0, {}, 0.0)
#vir4 = ResistantVirus(0.0, 1.0, {"drug1":True, "drug2":False}, 0.0)
#vir4 = ResistantVirus(1.0, 0.0, 
#                      {'drug1':True, 'drug2': True, 'drug3': True, 
#                      'drug4': True, 'drug5': True, 'drug6': True}, 0.5)
#print(vir4.getMutProb())
#print(vir4.getResistances())
#popDensity = 0
#activeDrugs = []
#print(vir4.reproduce(popDensity, activeDrugs))
#print(vir4.doesClear())
#print(vir4.isResistantTo('drug3'))



class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs# he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.drugList = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug in self.drugList:
            return
        else:
            self.drugList.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.drugList


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistPop = 0
        for virus in self.viruses:
            isResist = True
            for drug in drugResist:
                if virus.isResistantTo(drug) == False:
                    isResist = False
                    break
            if isResist == True:
                resistPop += 1
        return resistPop


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        livingVir = []
        for vir in self.viruses:
            if vir.doesClear() == False:
                livingVir.append(vir)
        
        popDensity = len(livingVir)/self.getMaxPop()
        
        newVir = []
        for vir in livingVir:
            try:
                newVir.append(vir.reproduce(popDensity,self.getPrescriptions()))
            except NoChildException:
                continue
        self.viruses = livingVir + newVir
        
        return self.getTotalPop()        

#TESTING
#virus = ResistantVirus(1.0, 0.0, {}, 0.0)
#patient = TreatedPatient([virus], 100)
#print(patient.update())

#virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
#virus2 = ResistantVirus(1.0, 0.0, {"drug1": False, "drug2": True}, 0.0)
#virus3 = ResistantVirus(1.0, 0.0, {"drug1": True, "drug2": True}, 0.0)
#patient = TreatedPatient([virus1, virus2, virus3], 100)

#print(patient.getResistPop(['drug1']))
#2
#print(patient.getResistPop(['drug2']))
#2
#print(patient.getResistPop(['drug1','drug2']))
#1
#print(patient.getResistPop(['drug3']))
#0
#print(patient.getResistPop(['drug1', 'drug3']))
#0
#print(patient.getResistPop(['drug1','drug2', 'drug3']))
#0


def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    virusesList = []
    for i in range(numViruses):
        virusesList.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)) 
   
    popSize = [0]*300
    virSize = [0]*300
    
    for trial in range(numTrials):
        human1 = TreatedPatient(virusesList, maxPop)
        for step in range(150):
            popSize[step] += human1.update()
            virSize[step] += human1.getResistPop(['guttagonol'])
        human1.addPrescription('guttagonol')
        for step in range(150,300):
            popSize[step] += human1.update()
            virSize[step] += human1.getResistPop(['guttagonol'])

    for i in range(len(popSize)):
        popSize[i] = popSize[i]/numTrials
    
    for i in range(len(virSize)):
        virSize[i] = virSize[i]/numTrials

   
    pylab.plot(popSize, label = 'human1')
    pylab.plot(virSize, label = 'G-res virus')
    pylab.title('Average Population Size over time')
    pylab.xlabel('number od time steps')
    pylab.ylabel('average population')
    pylab.legend(loc = 'best')
    pylab.show()
    

#TESTING
numViruses = 100
maxPop = 1000
maxBirthProb = 0.1
clearProb = 0.05
resistances = {'guttagonol': False}
mutProb = 0.005
numTrials = 5
print(simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                      mutProb, numTrials))

#print(simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5))
#print(simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5))
#print(simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1))




