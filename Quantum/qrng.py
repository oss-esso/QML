import cirq
import numpy as np

def random_number_generator(low=0, high=2**10, m=10):
    """
    :param low: lower bound of numbers to be generated
    :param high: Upper bound of numbers to be generated
    :param number m : Number of random numbers to output
    :return: string of random numbers
    """

    qubits_required = int(np.ceil(np.log2(high-low)))
    print(f"Number of qubits required: {qubits_required}")

    Q_reg = [cirq.LineQubit(i) for i in range(qubits_required)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(Q_reg[c]) for c in range(qubits_required))
    circuit.append(cirq.measure(*Q_reg, key='z'))
    print("Circuit:")
    print(circuit)

    sim = cirq.Simulator()

    num_gen = 0
    output = []
    while num_gen < m:
        result = sim.run(circuit, repetitions=1)
        rand_number = result.data['z'][0] + low
        if rand_number < high:
            output.append(rand_number)
            num_gen += 1
    return output


if __name__ == "__main__":
    output = random_number_generator()
    print(output)
    print(f'Mean of generated numbers: {np.mean(output)}')