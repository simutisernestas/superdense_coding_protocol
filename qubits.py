import random
import time
import numpy as np

random.seed(int(time.time()))


class QubitPair:
    def __init__(self):
        zero = np.array([[1.0],
                         [0.0]])
        # initial |00> state
        self.state = np.kron(zero, zero)

    def hgate(self):
        # Hadamard operation on first qubit
        hadamard = 1. / np.sqrt(2) * np.array([[1, 1],
                                               [1, -1]])

        # 4x4 hadamard for first qubit
        hadamard = np.kron(hadamard, np.eye(2))

        self.state = np.dot(hadamard, self.state)

    def cnot(self):
        # Controlled NOT
        zero = np.array([[1.0],
                         [0.0]])
        one = np.array([[0.0],
                        [1.0]])

        P0 = np.dot(zero, zero.T)
        P1 = np.dot(one, one.T)
        X = np.array([[0, 1],
                      [1, 0]])

        CNOT = np.kron(P0, np.eye(2)) + np.kron(P1, X)

        self.state = np.dot(CNOT, self.state)

        return self

    def xgate(self):
        # NOT gate on first qubit
        X = np.array([[0, 1],
                      [1, 0]])

        self.state = np.dot(np.kron(X, np.eye(2)), self.state)

    def zgate(self):
        # Z gate on first qubit
        Z = np.array([[1, 0],
                      [0, -1]])

        self.state = np.dot(np.kron(Z, np.eye(2)), self.state)

    def measure(self):
        '''Measure the two-qubit in the computational basis'''

        randomchoice = random.random()
        probs = self.state ** 2
        zerozeroprob = np.ravel(probs[0])
        zerooneprob = np.ravel(probs[1])
        onezeroprob = np.ravel(probs[2])

        if randomchoice < zerozeroprob:
            final_state = [[1.0],
                           [0.0],
                           [0.0],
                           [0.0]]
            return (0, 0)
        elif randomchoice < zerooneprob:
            final_state = [[0.0],
                           [1.0],
                           [0.0],
                           [0.0]]
            return (0, 1)
        elif randomchoice < onezeroprob:
            final_state = [[0.0],
                           [0.0],
                           [1.0],
                           [0.0]]
            return (1, 0)
        else:
            final_state = [[0.0],
                           [0.0],
                           [0.0],
                           [1.0]]
            return (1, 1)


if __name__ == "__main__":
    # Test applying all methods
    a = QubitPair()
    a.hgate()
    print(a.state)
    a.cnot()
    print(a.state)
    a.xgate()
    print(a.state)
    a.zgate()
    print(a.state)
    res = a.measure()
    print(res)
