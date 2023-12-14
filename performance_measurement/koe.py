from qubo_functions import create_qubo_cd
from graphs import create_graph, print_graph
from check_result import check_result_cd
from dimod import BinaryQuadraticModel
from dwave.samplers import SimulatedAnnealingSampler

size = 8
communities = 4
G = create_graph('geometric graph', size, weight=True, directed=False)
Q = create_qubo_cd(G, communities)
labels = {}
for i in range(len(G.nodes)):
    for j in range(communities):
        labels[i*communities + j]=(i,j)

bqm = BinaryQuadraticModel(Q, 'BINARY').relabel_variables(labels, inplace=False)
sampleset = SimulatedAnnealingSampler().sample(bqm, num_reads=2000).aggregate()
print(check_result_cd(G,sampleset,communities))
print_graph(G)
