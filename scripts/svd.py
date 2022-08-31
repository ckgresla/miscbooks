# DaVinci generated.....

import numpy as np

def SVD(A):
    #Compute the SVD of a matrix A
    #Input:
    #A - mxn matrix
    #Output:
    #U - mxm unitary matrix
    #S - mxn diagonal matrix
    #Vh - nxn unitary matrix
    
    #Compute the SVD using the numpy function
    U,S,Vh = np.linalg.svd(A)
    
    #Print the results
    print("U:")
    print(U)
    print("S:")
    print(S)
    print("Vh:")
    print(Vh)

A = np.array([[1,2,3],[4,5,6]])

SVD(A)
