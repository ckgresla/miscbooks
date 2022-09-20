# Logging in Python
# PythonDocs- https://docs.python.org/3/library/logging.html#
# g4g- https://www.geeksforgeeks.org/logging-in-python/

import logging


# Configure Logger (output files, write permissions, etc.)
logging.basicConfig(
    filename="test.log", #output filename, presumably in same dir
    format="%(asctime)s    %(name)s    %(levelname)s    %(message)s", 
    #configures the logger to write the timestamp, name of running user, level of log message and the message to the Log File (4-space sep.)
    filemode="w" #default is appending to file (overwrite existing logs with "w")
)

# Instantiate Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) #set threshold of logs, full list at- https://docs.python.org/3/library/logging.html#logging-levels


# Sample Messages -- Basically an alt way to get print statements that last
logger.debug("Example of a debugging message") #could pass in an object or relevant here
logger.info("this ought to be some information about the status of a program")
logger.warning("something might be suspect or is on track to break") #like a function return taking too long?
logger.error("yea something broke, example of an error log") #nice to include actual errors from "except Exception as E:" statements
logger.critical("some idiot hit the big red button, this is a critical log")


