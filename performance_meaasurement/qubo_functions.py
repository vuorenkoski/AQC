import numpy as np

def create_qubo_apsp(G):
    vertices = len(G.nodes)
    E = [] 
    for e in G.edges(data=True):
        E.append((e[0],e[1],e[2]['weight']))

    p = 1
    for e in E:
        p += e[2]

    edges = len(E)
    Q = np.zeros((2*vertices + edges, 2*vertices + edges))

    # Constraints 1 and 2
    for i in range(vertices):
        for j in range(vertices):
            if i!=j:
                Q[i,j] += p
                Q[vertices+i,j+vertices] += p
        
    # Constraint 3
    for i in range(vertices):
        Q[i,i+vertices] += p

    # Constraint 4
    for v in range(vertices):
        for i,e in enumerate(E):
            if e[0]==v:
                Q[v,vertices*2+i] -= p
            if e[1]==v:
                Q[v,vertices*2+i] += p

    # Constraint 5
    for v in range(vertices):
        for i,e in enumerate(E):
            if e[1]==v:
                Q[vertices+v,vertices*2+i] -= p
            if e[0]==v:
                Q[vertices+v,vertices*2+i] += p

    # Constraint 6 and 7
    for i,ei in enumerate(E):
        for j,ej in enumerate(E):
            if ei[0]==ej[0] or ei[1]==ej[1]:
                Q[vertices*2+i,vertices*2+j] += p
            if ei[1]==ej[0] or ei[0]==ej[1]:
                Q[vertices*2+i,vertices*2+j] -= p/2

    # Constraint 8 
    for i in range(edges):
        Q[vertices*2+i,vertices*2+i] += E[i][2]

    # Quadratic coefficients in lower triangle to upper triangle
    for i in range(vertices): 
        for j in range(i):
            Q[j,i] += Q[i,j]
            Q[i,j] = 0
            
    return Q

def create_qubo_cd(G, communities):
    vertices = len(G.nodes)
    Q = np.zeros((vertices*communities, vertices*communities))
    p = 0
    for e in G.edges:
        p += G[e[0]][e[1]]['weight']

    # Helper datastructure to containt k
    k = np.zeros(vertices)
    for e in G.edges:
        k[e[0]] += G[e[0]][e[1]]['weight']
        k[e[1]] += G[e[0]][e[1]]['weight']

    # Constraint 1
    for v in range(vertices): 
        for c1 in range(communities): 
            for c2 in range(communities):
                if  c1!=c2:
                    Q[v*communities+c1,v*communities+c2] += p
                
    # Constraint 2
    for c in range(communities):
        for v1 in range(vertices): 
            for v2 in range(v1+1,vertices): 
                Q[v1*communities+c, v2*communities+c] += k[v1]*k[v2] / (2*p)
                
    for e in G.edges:
        for c in range(communities):
            Q[e[0]*communities+c, e[1]*communities+c] -= G[e[0]][e[1]]['weight']
            
    return Q

def create_qubo_gi(G1, G2):
    vertices = len(G1.nodes)
    E1 = [] 
    for e in G1.edges(data=True):
        E1.append((e[0],e[1]))
    E2 = [] 
    for e in G2.edges(data=True):
        E2.append((e[0],e[1]))
    p = len(E1)
    Q = np.zeros((vertices*vertices, vertices*vertices))
    
    # Constraint 1: penalty if several mappings from same source
    for i in range(vertices): 
        for j in range(vertices): 
            for k in range(j+1,vertices): 
                Q[i*vertices+j,i*vertices+k]=p 

    # Constaint 2: penalty if several mappings to same target
    for i in range(vertices): 
        for j in range(vertices): 
            for k in range(j+1,vertices): 
                Q[i+vertices*j,i+vertices*k]=p 
                
    # Constraint 3: -1 for each succesfully mapped edge: (x1,y1) -> (x2,y2) 
    #    two possible mappings: (x1->x2, y1->y2) or (x1->y2,y1->x2)
    for e1 in E1: 
        for e2 in E2: 
            Q[e1[0]*vertices+e2[0], e1[1]*vertices+e2[1]] -= 1
            Q[e1[0]*vertices+e2[1], e1[1]*vertices+e2[0]] -= 1
            
    # All quadratic coefficients in lower triangle to upper triangle
    for i in range(vertices): 
        for j in range(i):
            Q[j,i] += Q[i,j]
            Q[i,j] = 0
    return Q