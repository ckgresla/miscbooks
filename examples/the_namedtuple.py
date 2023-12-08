"""
sample usage of the stdlib's module
* kinda like a convenient and functional dataclass

see the docs- https://docs.python.org/3/library/collections.html#collections.namedtuple
"""

from collections import namedtuple

WizBook = namedtuple("WizBook", ['spells', 'potions', 'is_evil']) 
        # 1st arg is the 'typename' --> what the type of the object is
        # 2nd arg is a list of 'field_names' --> each field becomes an attribute of instantiated typenames 
        #                                        (think instance.field for field in field_names)

evilbook = WizBook(
    spells=["avado-cadavro", "cuda-out-of-memory", "instant-trip"],
    potions=["oj", "room temp milk"],
    is_evil=True
)

print(evilbook)
print("orange juice (oj) is an evil potion? --> ", "oj" in evilbook.potions, end="\n\n") #great to see that empirically validated


holybook = WizBook(["praying"], ["holy-water"], False) #one could also just do the args thing
print(f"are religious texts EVIL? --> ", holybook.is_evil, end="\n\n") #also good to know


# we can also convert this convenient data structure to a dictionary
evildict = evilbook._asdict() 
print("dictionary of evil: ")
print(evildict)



