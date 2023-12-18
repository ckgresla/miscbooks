# You wanna run commands from inside a python script AND parse results? 
# some benevolent wizard on stackoverflow has us covered- https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output

import subprocess
output = subprocess.getoutput("ls -l")
print(output) #equivalent to running the command @ the cli 

# maybe you wanna get an array of the lines and do something with specific ones...
outlines = output.split("\n")
for line in outlines:
    if ".txt" in line:
        print(line, "--> gotta text file!")
