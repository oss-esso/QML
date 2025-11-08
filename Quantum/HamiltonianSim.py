import cirq
import numpy as np

class HamiltonianSimulation(cirq.Eigengate, cirq.SingleQubitGate):
    def __init__(self, _H_, t, exponent=1.0):
        self._H_ = _H_
        self.t = t
        self.exponent = exponent
        eigenvalues, eigenvectors = np.linalg.eigh(self._H_)
        self.eigen_components = []
        for _lambda_, vec in zip(eigenvalues, eigenvectors.T):
            theta = -_lambda_ * t / np.pi
            _proj_ = np.outer(vec, vec.conj())
            self.eigen_components.append((theta, _proj_))

    def _with_exponent(self, exponent):
        return HamiltonianSimulation(self._H_, self.t,exponent)
    def _eigen_components(self):
        return self.eigen_components