# -*- coding: UTF-8 -*-
from visual import *
'''
WIP
known issues:
遇到凹四邊形會爆掉 -solved v0.2
weird bouncing acceleration
#'''

########important variables##########
r = 0.05

#####functions#####
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def reflect(w,v):   #ball hit wall
    f = vector(-w[1],w[0],0) #法向量
    unit_f=f/abs(f) #法向量的單位向量
    re = v + abs(dot(v,f)/abs(f))*unit_f*2
    if abs(re) == abs(v):
        return v
    else:
        print("back hit")
        return reflect(-w,v)
def vcollision(a1p, a2p, a1v,a2v): #ball hit ball
    v1prime = a1v - (a1p - a2p)  * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p)  * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

def checkhit(w1,w2,b):
    wx1,wy1 = w1[0],w1[1]
    wx2,wy2 = w2[0],w2[1]
    bx ,by  =  b[0], b[1]
    area = 0.5*abs(wx1*wy2+wx2*by+bx*wy1-wy1*wx2-wy2*bx-by*wx1)
    wall = sqrt((wx1-wx2)**2+(wy1-wy2)**2)
    
    if (2*area/wall)<=r or ( dist(bx,by,wx1,wy1)<=r or dist(bx,by,wx2,wy2)<=r ):
        return True
    else: return False
    
#initialize!
scene = display(width=800, height=800,background=(0.0,0.0,0))
wall = [[1,1],[1,-1],[-1,-1],[-1,0],[0,0],[0,1],[1,1]]
container = curve(pos=wall) 

v    = vector(10,10)
for i in range(len(wall)):
    wall[i] = vector(wall[i])

ball = sphere(pos = vector(0,-0.1,0),radius = r)
#testing area    
print(reflect(wall[1]-wall[0],v))
#print(checkhit(wall[0],wall[1],v))

#main code
t = 0
dt =0.001
while True:
    rate(100)
    t+=dt
    ball.pos += v*dt
    for i in range(len(wall)-1):
        if checkhit(wall[i],wall[i+1],ball.pos) == True:
            print("hit: wall %d and %d"%(i,i+1))
            v = reflect(wall[i]-wall[i+1],v)
            print("speed %d"%abs(v))
