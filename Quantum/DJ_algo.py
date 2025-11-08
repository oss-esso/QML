import cirq
import numpy as np

def oracle(data_reg, y_reg, circuit, is_balanced=True):
    """
    :param data_reg: Qubits representing the data register
    :param y_reg: Qubit representing the output register
    :param circuit: cirq Circuit to which the oracle will be added
    :param is_balanced: Boolean indicating if the function is balanced or constant
    :return: None (the circuit is modified in place)
    """
    if is_balanced:
        for qubit in data_reg:
            circuit.append(cirq.CNOT(qubit, y_reg))
    return circuit

def deutsch_jozsa(domain_size: int, func_type_to_simulate: str = 'balanced', copies:int = 1000):
    """
    :param domain_size: Number of qubits in the data register
    :param func_type_to_simulate: 'balanced' or 'constant' to indicate the type of function
    :param copies: Number of times to run the circuit for statistics
    :return: None (prints the results)
    """
    if func_type_to_simulate not in ['balanced', 'constant']:
        raise ValueError("func_type_to_simulate must be 'balanced' or 'constant'")

    is_balanced = func_type_to_simulate == 'balanced'

    # Define qubits
    num_qubits = int(np.ceil(np.log2(domain_size)))

    data_reg = [cirq.LineQubit(i) for i in range(num_qubits)]
    y_reg = cirq.LineQubit(num_qubits)

    # Create circuit
    circuit = cirq.Circuit()

    # Initialize y_reg to |1>
    circuit.append(cirq.H(qubit) for qubit in data_reg)


    circuit.append(cirq.X(y_reg))
    circuit.append(cirq.H(y_reg))
    

    # Add oracle
    circuit = oracle(data_reg, y_reg, circuit, is_balanced)

    # Apply Hadamard to data register again
    circuit.append(cirq.H(qubit) for qubit in data_reg)

    # Measure data register
    circuit.append(cirq.measure(*data_reg, key='z'))

    print("Circuit:")
    print(circuit)

    # Simulate the circuit
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=copies)
    
    # Analyze results
    print(result.histogram(key='z'))
    



if __name__ == '__main__':
    print("Execute Deutsch Jozsa for a Balanced Function of Domain size 4")
    deutsch_jozsa(domain_size=4, func_type_to_simulate='balanced', copies=1000)
    print("Execute Deutsch Jozsa for a Constant Function of Domain size 4")
    deutsch_jozsa(domain_size=4, func_type_to_simulate='constant', copies=1000)



