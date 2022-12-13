# Chad Way of importing based on verbose file paths

package_path = "DocStore-Local" #without the .py extension
DocStore = __import__(package_path)

DocStore.function_of_interest() #is imported nicely!

