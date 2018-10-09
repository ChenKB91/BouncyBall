# -*- coding: UTF-8 -*-
#This is a modified beta version, which removes visualization
#Only a graph window left.
''' 
  A_____A
 /  = . =\   < Developed by CKB >
/     w   \
current version: 1.2

update log:
ver 1.0 - initial release
ver 1.1 - fix weird acceleration
ver 1.2 - fix "ball stuck in wall" problem

ver 2.0 -  MOAR BALLS

'''
from visual import *
from visual.graph import *
from Collision import *

########important variables##########
r = 0.05 #radius of ball
N = 50


'''initialization starts'''
#scene = display(width=800, height=800,background=(0.0,0.0,0),center = vector(0,0)
#                ,autoscale = False)
gd = gdisplay(x=600,y=0,width=600,height=600,xtitle='t',
              foreground=color.black,background=color.white)
f1 = gcurve(color=color.blue)

wall = [[0,3],[10,3],[15,1],[22,1],[22,-1],[15,-1],[10,-3],[0,-3]]  #L shape
#wall = [[2,2],[2,-2],[-2,-2],[-2,2],[2,2]]   #square
#wall = [[1,1],[1,0],[-1,-1],[-1,0],[1,2],[1,3]]
#wall = [[780,0],[1150,-140],[1180,-130],[1170,-90],[970,0],[780,0]]
'''
wall = [[0,60],[300,60],[850,240],[900,250],[940,220],[950,170],[940,130],[900,100],[730,60],[1170,40],
        [1400,60],
        [1400,0],[1070,0],[1200,-60],[1230,-90],[1240,-130],[1230,-170],[1180,-190],[1130,-180],[610,0],[300,20],
        [0,0],[0,60]]
#'''
#container = curve(pos=wall)  #!vis


random.seed(1)
##define v (array)
v = random.uniform(30,40,[N,3])
for i in range(len(v)):
    v[i][1] = random.random(size = None)*10 - 5
    v[i][2] = 0
for i in range(len(wall)):
    wall[i] = vector(wall[i])

##define pos_arr (array)
#pos_arr = random.uniform(-3,3,(N,3))
    pos_arr = zeros((N,3))
    
for i in range(len(pos_arr)):
    pos_arr[i][2] = 0
    pos_arr[i][1] = random.random(size = None)*6 - 3
    pos_arr[i][0] = random.random(size = None)*10

#ball = [sphere(radius = r,make_trail=False,       #!vis
#               color=color.yellow, visible = False) for i in range(N)]#!vis

#ball[0].color = color.red  #!vis
#ball[0].make_trail = True  #!vis
#for i in range(N):  #!vis
#    ball[i].pos = vector(pos_arr[i])  #!vis

#main code
t = 0
dt =0.001
dts = 0
'''initialization ends'''
###functions###


def add_ball(pos,vel):
    '''
    pos,v should be list with 3 variables
    '''
#    global ball #!vis
    global pos_arr, v, N
#    ball.append(sphere(radius=r,make_trail=False,color=color.yellow, visible = False)) #!vis
    pos_arr = append(pos_arr,[pos], axis = 0)
    v = append(v,[vel], axis = 0)
    N += 1
    print('NOW N = %d'%N)

def del_ball(index):
    global ball
    global pos_arr, v, N
    print('del ball %d' % index)
    
#    ball[index].visible = False    #!vis
#    del ball[index]                #!vis
    pos_arr = delete(pos_arr, index, 0)
    v = delete(v, index, 0)
    N -= 1
    
    
while N<100 :
    rate(500)
    t+=dt
    dts += 1
    '''
    if dts%10 == 0:
        rd = random.uniform(9,11)
        rdv= random.uniform(-1,1)
        rd2 =random.uniform(-3,3)
        summon_ball((0,rd2,0),(rd,rdv,0))
    #'''
    #average vel
    tmp = 0
    for i in range(len(v)):
        ab = abs(vector(v[i]))
        tmp += ab
    avg = tmp/len(v)
    f1.plot(pos = (t,avg))

    
    
    for j in range(N):
        for k in range(2):
            pos_arr[j][k] += v[j][k]*dt
#        ball[j].pos = vector(pos_arr[j]) #!vis
        
        #'''  ball hit detection
        r_array = pos_arr-pos_arr[:,newaxis]            # all pairs of atom-to-atom vectors
        rmag = sum(square(r_array),-1)                      # atom-to-atom distance squared
        hit = nonzero((rmag < 4*r**2) - identity(N))
        hitlist = zip(hit[0], hit[1])     
        for p,q in hitlist:
            if sum((pos_arr[p]-pos_arr[q])*(v[p]-v[q])) < 0 :       # check if approaching
                v[p], v[q] = vcollision(pos_arr[p], pos_arr[q], v[p], v[q])
                #print('ball hit')
        #'''
                
        for i in range(len(wall)-1):
            w = wall[i]-wall[i+1]
            f = vector(-w[1],w[0]) #法向量
            if checkhit(wall[i],wall[i+1],pos_arr[j],r) and dot([v[j][0],v[j][1],0],f)<0:
                #print("hit: wall %d and %d"%(i,i+1))
                v[j] = reflect(w,v[j])
                

    if dts% 10 == 0 :
        #print('add ball')
        add_ball(pos = [0,random.random(size = None)*6 - 3,0],
                 vel = [random.random(size = None)*10 +30,random.random(size = None)*10 -5,0])
    
    m = 0  ##trying to delete a ball without problem
    while True:
        m += 1
        if m == N:
            break
        if pos_arr[m][0] > 21 or pos_arr[m][0] < 0 or abs(pos_arr[m][1]) > 3:
            #print('prev N = %d' % N)
            del_ball(m)  #delete ball out of range
            #print('after N = %d' % N)
        
        
