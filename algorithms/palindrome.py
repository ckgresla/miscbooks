
def palindrome(string):

	string_len = len(string)
	
	for i in range(0, string_len//2):
		if string[i] != string[string_len-1-i]:
			print("False")
			return False
	
	print("True")
	return True


string = "oyyo"
string = "wowz"
palindrome(string)

