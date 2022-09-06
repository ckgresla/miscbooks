# Renamer -- Split on Separator and Rename all files in dir accordingly (as a portion of the split file name)
import os 


curr_dir = os.listdir()


for file in curr_dir:
	portions = file.split("?")
	print(portions[0]) #presumably the portion of the original file we want (substring after splitting)
	
	# Renaming Operation, in-place w os
	os.rename(i, t[0])


