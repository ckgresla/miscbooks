# Imports
import os
import sys
import shutil

# Dir set to folder of Script
directory = os.path.dirname(os.path.realpath(sys.argv[1])) #get the directory of your script (pass 0) else pass alt file path (1)

# Algorithm
for subdir, dirs, files in os.walk(directory):
 for filename in files:
  if filename.find('.webp') > 0: #Extension to change (.xlsx in first iter)
   subdirectoryPath = os.path.relpath(subdir, directory) #get the path to your subdirectory
   filePath = os.path.join(subdirectoryPath, filename) #get the path to your file
   newFilePath = filePath.replace(".webp",".jpg") #create the new name (extension to change to)
   os.rename(filePath, newFilePath) #rename file
