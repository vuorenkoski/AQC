from graphs import create_graph

sizes = [5,7,10,15,20,30,40]
graph_types = ['path graph', 'star graph', 'cycle graph', 'complete graph', 'tree graph', 'single cycle graph', 
               'multiple cycle graph', 'bipartite graph', 'wheel graph', 'random graph', 'community graph']

for g in graph_types:
    print(g, end='')
    for i in sizes:
        print(' & '+str(len(create_graph(g,i).edges())), end='')
    print(' \\\\')