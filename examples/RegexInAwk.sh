# A minimum example of using regex to search for something with awk

datafile="some/path/of/interest/file.txt"


awk '
	/1234/ { n_matches = n_matches + 1 }
	END    { print n_matches }
' $datafile 

# you should really use this to pipe the filtered input into something else, say in a new file?

