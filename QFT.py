import cirq
import numpy as np
import fire
from elapsedtimer import ElapsedTimer

class QFT:
    def __init__(self, signal_length=16, basis_to_transform='', validate_inverse_fourier=False, qubits=None):
        self.signal_length = signal_length
        self.basis_to_transform = basis_to_transform
        self.validate_inverse_fourier = validate_inverse_fourier

        if qubits is None:
            self.num_qubits = int(np.log2(signal_length))
            self.qubits = [cirq.LineQubit(i) for i in range(self.num_qubits)]
        else:
            self.qubits = qubits
            self.num_qubits = len(qubits)

        self.qubit_index = 0
        self.input_circuit = cirq.Circuit()

        self.circuit = cirq.Circuit()
        if validate_inverse_fourier:
            self.inverse_circuit = cirq.Circuit()
        
        for k, q_s in enumerate(basis_to_transform):
            if int(q_s) == 1:
                self.input_circuit.append(cirq.X(self.qubits[k]))


    def qft_circuit_iter(self):
        if self.qubit_index > 0:
        # Apply the rotations on the prior qubits
        # conditioned on the current qubit
            for j in range(self.qubit_index):
                diff = self.qubit_index - j + 1
                rotation_to_apply = -2.0 / (2.0 ** diff)
                self.circuit.append(cirq.CZ(self.qubits[
                self.qubit_index],
                self.qubits[j]) ** rotation_to_apply)
        # Apply the Hadamard Transform
        # on current qubit
        self.circuit.append(cirq.H(self.qubits[
        self.qubit_index]))
        # set up the processing for next qubit
        self.qubit_index += 1

    def qft_circuit(self):
        while self.qubit_index < self.num_qubits:
            self.qft_circuit_iter()
            print(f"QFT step {self.qubit_index-1} complete")
            print(self.circuit)

        self.swap_qubits()
        print('Circuit after swaps')
        print(self.circuit)
        self.inv_circuit = cirq.inverse(self.circuit.copy())

    def swap_qubits(self):
        # Swap the states of pair of qubits whose indices sum to n
        for i in range(self.num_qubits // 2):
            self.circuit.append(cirq.SWAP(self.qubits[i], self.qubits[self.num_qubits - i - 1]))

    def simulate_circuit(self):
        sim = cirq.Simulator()
        result = sim.simulate(self.circuit)
        return result