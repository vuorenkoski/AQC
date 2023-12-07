from networkx.classes.function import path_weight
from networkx import has_path, all_shortest_paths

def xy_from_label(e):
    x = 0
    y = 0
    i = len(e)-1
    d = 1
    while e[i]!='-':
        y += d*int(e[i])
        d *= 10 
        i -= 1
    d = 1
    i -= 1
    while i>=0:
        x += d*int(e[i])
        d *= 10
        i -= 1 
    return (x,y)

def path_from_sample(sample,G):
    vertices = len(G.nodes)
    s = 0
    t = 0
    w = 0
    for v in range(vertices):
        if sample['s'+str(v)]==1:
            s = v
        if sample['t'+str(v)]==1:
            t = v
    if s==t:
        return (None,None,None)
    i = s
    path = [i]
    while i!=t:
        xx = i
        for p in sample:
            if p[0]!='s' and p[0]!='t' and sample[p]==1:
                x,y = xy_from_label(p)
                if x==i:
                    path.append(y)
                    w += G[x][y]['weight']
                    i = y
                    break
        if xx==i:
            return (None,None,None)
    return (str(s)+'-'+str(t),path,w)

def result_paths(sampleset, G):
    res = {}
    for s in sampleset.filter(lambda s: s.energy<0):
        st, path, w = path_from_sample(s,G)
        if st!=None and st not in res:
            res[st]=(path,w)
    return res

def check_result_apsp(G,sampleset):
    ok = 0
    s = 0
    res = result_paths(sampleset, G)
    for i in G.nodes:
        for j in G.nodes:
            if i!=j and has_path(G,i,j):
                s += 1
                sp = [p for p in all_shortest_paths(G,i,j,weight='weight')]
                w1 = path_weight(G,sp[0],'weight')
                if str(i)+'-'+str(j) in res.keys():  # Does result have path between s-t
                    path,w2 = res[str(i)+'-'+str(j)]
                    if (path in sp) and w1==w2:      # Is path among correct paths and are weights same
                        ok += 1
    print(ok,'/',s)
    return str(int(100*ok/s))

def check_result_gi(sampleset, e):
    return str(int(sampleset.first.energy)-e)
