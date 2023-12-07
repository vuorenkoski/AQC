from graphs import create_graph, print_graph, print_result_latex
from qubo_functions import create_qubo_apsp
from dimod import BinaryQuadraticModel
import time
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler
from dwave.samplers import SimulatedAnnealingSampler
from api_token import token
from check_result import check_result_apsp

num_reads_sel = [2000]
sizes = [5,7,10,15]
solvers = ['local simulator', 'quantum solver']
graph_types = ['path graph', 'star graph', 'cycle graph', 'complete graph', 'tree graph', 'single cycle graph', 
               'multiple cycle graph', 'bipartite graph', 'regular graph', 'wheel graph', 'friendship graph',
               'random graph']

machine = DWaveSampler(solver={'chip_id': 'Advantage_system4.1'}, token=token)
print('Chip:', machine.properties['chip_id'])
print('Qubits:', machine.properties['num_qubits'])

result_table = []
for num_reads in num_reads_sel:
    for size in sizes:
        for gtype in graph_types:
            print(gtype)
            G = create_graph(gtype, size, weight=True)
            if G!=None:
                Q = create_qubo_apsp(G)
                labels = {}
                for i in range(size):
                    labels[i]='s'+str(i)
                    labels[size+i]='t'+str(i)   
                for i,e in enumerate(G.edges):
                    labels[size*2+i] = str(e[0]) + '-' + str(e[1])

                bqm = BinaryQuadraticModel(Q, 'BINARY').relabel_variables(labels, inplace=False)
                for solver in solvers:
                    result = {}
                    result['gtype'] = gtype
                    result['vertices'] = len(G.nodes)
                    result['logical_qubits'] = Q.shape[0]  
                    result['couplers'] = len(bqm.quadratic)
                    if solver=='local simulator':
                        result['solver'] = 'Simulator'
                        result['physical_qubits'] = 'n/a'
                        ts = time.time()
                        sampleset = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads).aggregate()
                        result['time'] = int((time.time()-ts)*1000)
                        result['samples'] = str(num_reads)
                    elif solver=='cloud hybrid solver':
                        try:
                            sampleset = LeapHybridSampler(token=token).sample(bqm).aggregate()
                        except Exception as err:
                            continue 
                        result['physical_qubits'] = 'n/a'
                        result['time'] = int(sampleset.info['run_time'] / 1000)
                        result['solver'] = 'Hybrid'
                        result['samples'] = 'n/a'
                    elif solver=='quantum solver':
                        try:
                            sampleset = EmbeddingComposite(machine).sample(bqm, num_reads=num_reads, return_embedding=True).aggregate()
                        except Exception as err:
                            continue 
                        result['solver'] = 'Quantum'
                        result['time'] = int(sampleset.info['timing']['qpu_access_time'] / 1000)
                        result['physical_qubits'] = str(sum(len(x) for x in sampleset.info['embedding_context']['embedding'].values()))
                        result['chainb'] = sampleset.first.chain_break_fraction
                        result['samples'] = num_reads
                    result['energy'] = int(sampleset.first.energy)
                    result['performance'] = str(check_result_apsp(G, sampleset)) + ' \\%'
                    result_table.append(result)

print(result_table)
print_result_latex(result_table)




