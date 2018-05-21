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
    q = p.copy()
    direction = ""
    if abs(U[0]) > 0.0:
        direction = "V"
        U = U[0]

    elif abs(U[1]) > 0.0:
        direction ="H"
        U = U[1]
    if direction == "H":
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                s = pMove * p[i,((j-U) % p.shape[1])]
                s = s + pNoMove * p[i,j]
                q[i,j] = s


    if direction == "V":
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                s = pMove * p[((i-U) % p.shape[0]),j]
                s = s + pNoMove * p[i,j]
                q[i,j] = s
    return q





colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 0.5


def localize(colors, measurements, motions, sensor_right, p_move):

    pHit = sensor_right
    pMiss = 1.0 - sensor_right


    world_size = len(colors[0]) * len(colors)
    init_p = 1.0/world_size

    p = np.full((len(colors[0]),len(colors)),init_p)


    pMove = p_move
    pNoMove = 1- pMove

    for i in range(0,len(motions)):
        p = move(p,motions[i],pMove=pMove,pNoMove=pNoMove)
        p = sense(p, measurements[i], colors, pMiss=pMiss, pHit=pHit)

    return p

p = localize(colors, measurements, motions, sensor_right, p_move)

print(p)
