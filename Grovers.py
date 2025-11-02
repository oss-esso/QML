import cirq
import numpy as np

def oracle(input_qubits, target_qubit, circuit, secret_element='01'):
    """Creates an oracle for Simon's algorithm.

    Args:
        input_qubits: List of cirq.Qid, the input qubits.
        output_qubit: cirq.Qid, the output qubit.
        secret_element: str, the element that defines the oracle behavior.
    """
    print(f"Creating oracle for secret element: {secret_element}")
    for i, bit in enumerate(secret_element):
        if int(bit) == 0:
            circuit.append(cirq.X(input_qubits[i]))

    circuit.append(cirq.TOFFOLI(*input_qubits, target_qubit))
    for i, bit in enumerate(secret_element):
        if int(bit) == 0:
            circuit.append(cirq.X(input_qubits[i]))

    return circuit


def grovers_algorithm(num_qubits=2, copies=1000):
    input_qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    output_qubit = cirq.LineQubit(num_qubits)
    circuit = cirq.Circuit()

    # Create the oracle
    

    # Add Grover's diffusion operator
    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append([cirq.X(output_qubit), cirq.H(output_qubit)])
    circuit =oracle(input_qubits, output_qubit, circuit)
    circuit.append(cirq.H.on_each(*input_qubits))
    circuit.append(cirq.X.on_each(*input_qubits))

    circuit.append(cirq.H.on(input_qubits[1]))
    circuit.append(cirq.CNOT(input_qubits[0], input_qubits[1]))

    circuit.append(cirq.H.on(input_qubits[1]))
    circuit.append(cirq.X.on_each(*input_qubits))
    circuit.append(cirq.H.on_each(*input_qubits))
    
    # Measure the result.
    circuit.append(cirq.measure(*input_qubits, key='Z'))
    print("Grover's algorithm follows")
    print(circuit)
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=copies)
    out = result.histogram(key='Z')
    out_result = {}
    for k in out.keys():
        new_key = "{0:b}".format(k)
        if len(new_key) < num_qubits:
            new_key = (num_qubits - len(new_key))*'0'+ new_key
    out_result[new_key] = out[k]
    print(out_result)
if __name__ =='__main__':
    grovers_algorithm(2)