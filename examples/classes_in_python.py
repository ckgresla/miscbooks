# You never really master it ya know, but you can get better at it! --> NAMESPACES
# Referencing- https://docs.python.org/2/tutorial/classes.html


# Simple Class
class NoviceWizard:
    """ The most Trivial of Classes as an example """
    i = 12345

    def funky(self):
        return "you just called a function bro"

instance = NoviceWizard()

print(instance.i)
print(instance.funky())

"""
Notes on Above:
    * No need for 'self.' syntax in the vars @ the init portion of class (automatically became attributes nicely)
        * adding in vars to a class like this makes them 'class variables' --> these will be SHARED BY ALL INSTANCES OF THE CLASS & changing the value of one parameter does so for all others, if we want to have some data associated with JUST that class, include it in the '__init__' function instead (associated with just the one instance so can change w/o altering all the rest of the datastructs)
    * Functions defined as part of a class are referred to as 'Methods' ('funky' is a method of the 'NoviceWizard' class)

"""


# Simple Class w Values Passed in on Initialization of an Instance
class InitializedWizard:
    def __init__(self, name, is_good):
        self.name = name
        self.is_good = is_good
        return

n = "Rufis Maxiumus NonSensicus"
evil = True

instance = InitializedWizard(n, evil) #give it vars w the init

print(instance.name, instance.is_good)

"""
Notes on Above:
    * here we give the class the expected variables on initializing an instance of it 
    * pass 'self' to the '__init__()' function
"""


# The DATACLASS- https://docs.python.org/3/library/dataclasses.html
from dataclasses import dataclass

@dataclass
class WizardWand:
    """ Dataclasses are cool, type strongly and the boilerplate works itself out """
    name: str
    core_type: str #one of [pheonix, dragonheart, dumbledorebrow]
    length: int #in CM since those wizards like the metric system

tasteful_wand = WizardWand("Malfoy's Wand", "dumbledorebrow", 34) #all the init and stuff gets handled! 
print(tasteful_wand)

