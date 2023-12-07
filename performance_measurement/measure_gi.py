from graphs import create_graph, print_graph, print_result_latex
from qubo_functions import create_qubo_gi
from dimod import BinaryQuadraticModel
import time
from dwave.system import DWaveSampler, EmbeddingComposite, LeapHybridSampler
from dwave.samplers import SimulatedAnnealingSampler
from api_token import token
from check_result import check_result_gi

num_reads_sel = [2000]
#sizes = [5,7,10,15,20]
sizes = [10]
solvers = ['local simulator', 'cloud hybrid solver', 'quantum solver']
#solvers = ['cloud hybrid solver']
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
            G1,G2 = create_graph(gtype, size, directed=False, permutation=True)
            if G1!=None:
                Q = create_qubo_gi(G1,G2)
                bqm = BinaryQuadraticModel(Q, 'BINARY')
                for solver in solvers:
                    result = {}
                    result['gtype'] = gtype
                    result['vertices'] = len(G1.nodes)
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
                    result['performance'] = check_result_gi(sampleset, -len(G1.edges))
                    result_table.append(result)

print(result_table)
print_result_latex(result_table)




