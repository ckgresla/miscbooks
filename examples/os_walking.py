# Usage for the os.walk command, view the contents of a dir and subdirs programmatically
import os 


dir_of_interest = "data"

for d, sd, files in os.walk(dir_of_interest):
    print(d)       #directory
    print(sd)      #sub-directory
    print(files)   #files in sub-directory
    for f in files:
        print(f"{d}/{f}") #full path to file (relative)


