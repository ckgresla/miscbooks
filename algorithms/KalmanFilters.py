#!/usr/bin/env python

"""
Useful Resources:
Blog Post- https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/#mathybits
Paper w Below Implementation- https://arxiv.org/pdf/1204.0375.pdf
"""

# Kalman Filters in Python
import numpy as np


# The Filter as a Class (prediction and update steps as methods)
class KalmanFilter:
    def __init__(self, *args, **kwargs):
        return

    def predict(self, X, P, A, Q, B, U):
        X = np.dot(A, X) + np.dot(B, U)
        P = np.dot(A, np.dot(P, A.T)) + Q
        return (X, P)

    def update(self, X, P, Y, H, R):
        IM = np.dot(H, X)
        IS = R + np.dot(H, np.dot(P, H.T))
        K = np.dot(P, np.dot(H.T, np.linalg.inv(IS)))
        X = X = np.dot(K, (Y-IM))
        P = P - np.dot(K, np.dot(IS, K.T))
        LH = self.gauss_pdf(Y, IM, IS)
        return (X, P, K, IM, IS, LH)

    def gauss_pdf(self, X, M, S):
        if M.shape[1] == 1:
            DX = X - np.tile(M, X.shape[1])
            E = 0.5 * np.sum(DX * (np.dot(np.linalg.inv(S), DX)))
            E = E + 0.5 * M.shape[0] * np.log(2 * pi) + 0.5 * np.log(np.linalg.det(S))
            P = np.exp(-E)

        elif X.shape[1] == 1:
            DX = np.tile(X, M.shape[1]) - M
            E = 0.5 * np.sum(DX * (np.dot(np.linalg.inv(S), DX)), axis=0)
            E = E + 0.5 * M.shape[0] * np.log(2 * pi) + 0.5 * np.log(np.linalg.det(S))
            P = np.exp(-E)

        else:
            DX = X - M
            E = 0.5 * np.dot(DX.T, np.dot(np.linalg.inv(S), DX))
            E = E + 0.5 * M.shape[0] * np.log(2 * pi) + 0.5 * np.log(np.linalg.det(S))
            P = np.exp(-E)

        return (P, E)



# Driver Code + Program Parameters

#time step of mobile movement
dt = 0.1

pi = 3.14

# Initialization of state matrices
X = np.array([[0.0], [0.0], [0.1], [0.1]])
P = np.diag((0.01, 0.01, 0.01, 0.01))
A = np.array([[1, 0, dt , 0], [0, 1, 0, dt], [0, 0, 1, 0], [0, 0, 0,1]])
Q = np.eye(X.shape[0])
B = np.eye(X.shape[0])
U = np.zeros((X.shape[0],1))

# Measurement matrices
Y = np.array([[X[0,0] + abs(np.random.rand(1)[0])], [X[1,0] + abs(np.random.rand(1)[0])]])
H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
R = np.eye(Y.shape[0])

# Number of iterations in Kalman Filter
N_iter = 50


# Applying the Kalman Filter
km = KalmanFilter()
for i in np.arange(0, N_iter):
     (X, P) = km.predict(X, P, A, Q, B, U)
     (X, P, K, IM, IS, LH) = km.update(X, P, Y, H, R)
     Y = np.array([[X[0,0] + abs(0.1 * np.random.rand(1)[0])],[X[1, 0] + abs(0.1 * np.random.rand(1)[0])]]) 
     print(f"@ Timestep {i} -- X: {X}, Y: {Y}")



