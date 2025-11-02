import cirq
import numpy as np
from QFT import QFT

class quantum_phase_estimation:
    def __init__(self, unitary, eigenstate, num_counting_qubits=3):
        self.unitary = unitary
        self.eigenstate = eigenstate
        self.num_counting_qubits = num_counting_qubits

        self.counting_qubits = [cirq.LineQubit(i) for i in range(num_counting_qubits)]
        self.eigenstate_qubits = [cirq.LineQubit(i + num_counting_qubits) for i in range(len(eigenstate))]

        self.circuit = cirq.Circuit()

    def apply_hadamards(self):
        self.circuit.append(cirq.H.on_each(*self.counting_qubits))

    def apply_controlled_unitaries(self):
        for i in range(self.num_counting_qubits):
            exponent = 2 ** i
            controlled_unitary = cirq.ControlledGate(self.unitary**exponent)
            self.circuit.append(controlled_unitary(self.counting_qubits[i], *self.eigenstate_qubits))

    def apply_inverse_qft(self):
        qft_instance = QFT(signal_length=2**self.num_counting_qubits, validate_inverse_fourier=True, qubits=self.counting_qubits)
        qft_instance.qft_circuit()
        self.circuit += qft_instance.inv_circuit

    def measure_counting_qubits(self):
        self.circuit.append(cirq.measure(*self.counting_qubits, key='result'))

    def build_circuit(self):
        # Initialize eigenstate
        for i, bit in enumerate(self.eigenstate):
            if int(bit) == 1:
                self.circuit.append(cirq.X(self.eigenstate_qubits[i]))

        self.apply_hadamards()
        self.apply_controlled_unitaries()
        self.apply_inverse_qft()
        self.measure_counting_qubits()

    def run(self, repetitions=1000):
        self.build_circuit()
        print("Quantum Phase Estimation Circuit:")
        print(self.circuit)

        simulator = cirq.Simulator()
        result = simulator.run(self.circuit, repetitions=repetitions)
        histogram = result.histogram(key='result')

        formatted_result = {}
        for k in histogram.keys():
            binary_key = format(k, f'0{self.num_counting_qubits}b')
            formatted_result[binary_key] = histogram[k]

        print("Measurement results:")
        for outcome, count in formatted_result.items():
            print(f"{outcome}: {count}")
        return formatted_result
    
if __name__ == "__main__":
    # Example usage with a simple unitary (Z gate) and eigenstate |1>
    unitary = cirq.Z
    eigenstate = '1'
    qpe = quantum_phase_estimation(unitary, eigenstate, num_counting_qubits=3)
    qpe.run(repetitions=1000)