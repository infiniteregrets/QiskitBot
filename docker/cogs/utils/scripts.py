LIB_IMPORT="""
from qiskit import QuantumCircuit
from qiskit import execute, Aer
from qiskit.visualization import *"""

CIRCUIT_SCRIPT="""
circuit = build_state()
circuit.measure_all()
figure = circuit.draw('mpl')
output = figure.savefig('circuit.png')"""

PLOT_SCRIPT="""
backend = Aer.get_backend("qasm_simulator")
job = execute(circuit,backend=backend, shots =1000)
counts = job.result().get_counts()
plot_histogram(counts).savefig('plot.png', dpi=100, quality=90)"""

ASCII_CIRCUIT_SCRIPT="""
circuit = build_state()
print(circuit)
"""