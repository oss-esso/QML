import cirq
import numpy as np

def oracle(input_qubits, target_qubits, circuit):
    """Implements the oracle for Simon's algorithm.

    Args:
        input_qubits: List of cirq.Qid, the input qubits.
        target_qubits: List of cirq.Qid, the target qubits.
        circuit: cirq.Circuit, the circuit implementing the function f.
        """
    
    #Oracle for 110
    circuit.append(cirq.CNOT(input_qubits[2], target_qubits[1]))
    circuit.append(cirq.X(target_qubits[0]))
    circuit.append(cirq.CNOT(input_qubits[2], target_qubits[0]))
    circuit.append(cirq.CCNOT(input_qubits[0],input_qubits[1], target_qubits[0]))
    circuit.append(cirq.X(input_qubits[0]))
    circuit.append(cirq.X(input_qubits[1]))
    circuit.append(cirq.CCNOT(input_qubits[0],input_qubits[1], target_qubits[0]))
    circuit.append(cirq.X(input_qubits[0]))
    circuit.append(cirq.X(input_qubits[1]))
    circuit.append(cirq.X(input_qubits[0]))
    return circuit

def simons_algorithm_circuit(num_qubits=3, copies=1000):
    """Constructs the circuit for Simon's algorithm.

    Args:
        num_qubits: int, number of qubits in the input register.
        copies: int, number of measurement repetitions.
        """
    # Define qubits
    input_qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    target_qubits = [cirq.LineQubit(i + num_qubits) for i in range(num_qubits)]
    
    # Create circuit
    circuit = cirq.Circuit()
    
    # Apply Hadamard to input qubits
    circuit.append(cirq.H.on_each(*input_qubits))
    
    # Apply oracle
    oracle(input_qubits, target_qubits, circuit)
    
    # Apply Hadamard to input qubits again
    circuit.append(cirq.H.on_each(*input_qubits))
    
    # Measure input qubits
    circuit.append(cirq.measure(*input_qubits, key='result'))
    
    return circuit, input_qubits, target_qubits


def run_simons_algorithm(circuit, copies=1000):
    """Runs the Simon's algorithm circuit and returns measurement results.

    Args:
        circuit: cirq.Circuit, the circuit to be executed.
        copies: int, number of measurement repetitions.
        """
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=copies)
    return result.histogram(key='result')

if __name__ == "__main__":
    num_qubits = 3
    copies = 1000
    
    circuit, input_qubits, target_qubits = simons_algorithm_circuit(num_qubits, copies)
    print("Circuit:")
    print(circuit)
    
    results = run_simons_algorithm(circuit, copies)
    print("\nMeasurement results:")
    for outcome, count in results.items():
        print(f"{outcome:0{num_qubits}b}: {count}")

        