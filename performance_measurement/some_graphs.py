import numpy as np
import matplotlib.pyplot as plt


# phys qubits vs performance in all pairs shortest path (quantum solver)
data1 = np.array([[24,100],[24,100],[25,100],[47,100],[24,100],[27,100],[32,100],[58,100],
[36,100],[45,100],[38,100],[41,100],[39,100],[124,80],[37,100],[43,100],
[53,100],[56,100],[68,97],[77,96],[67,93],[82,100],[66,86],[392,0],
[71,100],[78,95],[83,96],[112,87],[123,70],[251,8],[149,40],[163,78],
[138,15],[127,20],[145,35],[171,4],[233,15],[260,1],
[134,15],[166,57],[134,13],[153,67],[140,41],[160,14],[205,30],[263,0]])
data1 = data1.T

plt.figure(figsize=(12,6))
plt.scatter(data1[0],data1[1])
plt.xlabel('Physical qubits')
plt.ylabel('Performance (%)')
plt.show()

data2 = np.array([[59,0], [63,0], [70,0], [87,0], [66,0], [66,0], [72,0], [71,0], 
[89,0], [67,0], [225,1], [216,0], [225,0], [321,0], [210,0], [207,0], 
[257,0], [276,0], [279,0], [280,0], [831,5], [817,1], [904,5], [1414,0], 
[859,5], [799,5], [1035,6], [997,7], [1092,7], [1046,8] 

])
