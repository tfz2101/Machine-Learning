import numpy as np
import pandas as pd




def sense(p, Z, world, pMiss, pHit):
    q=np.full((p.shape[0],p.shape[1]),1.0)
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            hit = (Z == world[i][j])
            q[i,j] = float(p[i,j] * (hit * pHit + (1-hit) * pMiss))
    s = np.sum(q, axis=None)

    for i in range(len(q)):
        for j in range(len(q[0])):
            q[i,j] = q[i,j] / s
    return q

def move(p, U, pMove, pNoMove):
    q = np.full((p.shape[0], p.shape[1]), 1.0)
    direction = ""
    if abs(U[0]) <= 0.0:
        direction = "V"
        U = U[0]
    elif abs(U[1]) <= 0.0:
        direction ="H"
        U = U[1]
    if direction == "H":
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                s = pMove * p[i,((j-U) % p.shape[1])]
                print('1st s',s)
                s = s + pNoMove * p[i,j]
                q[i,j] = s


    if direction == "V":
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                s = pMove * p[((i-U) % p.shape[0]),j]
                print('1st s', s)
                s = s + pNoMove * p[i,j]
                q[i,j] = s
    return q

def localize(colors,measurements,motions,sensor_right,p_move):
        pass



colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 0.8
p_move = 1.0


pHit = sensor_right
pMiss = 1.0 - sensor_right


world_size = len(colors[0]) * len(colors)
init_p = 1.0/world_size

p = np.full((len(colors[0]),len(colors)),init_p)

p1 = sense(p,measurements[0],colors, pMiss, pHit)

'''
for k in range(0, len(measurements)):
    p = sense(p, measurements[k],colors,pMiss,pHit)
    print(np.array(p))

'''

pMove = p_move
pNoMove = 1- p_move
for i in range(0,len(motions)):
    p = sense(p, measurements[i], colors, pMiss, pHit)
    p = move(p,motions[i],pMove,pNoMove)
    print(p)
