# -*- coding: UTF-8 -*-
'''
  A_____A
 /  = . =  - Developed by CKB, do not steal plz
/     w   \

'''
from visual import *
from visual.graph import *
from Collision import *

# Do the bloody importing
import sys

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
print(sys.path)
from util import NACA_produce as naca

# variables
r = 0.1  # radius of ball
#N = 50


# visual stuff
scene = display(x=0, y=0, width=600, height=600, background=(0, 0, 0), center=vector(11, 0)  # !vis
                , autoscale=False,)  # !vis
gd = gdisplay(x=600, y=0, width=300, height=300, xtitle='t', title='Force',
              foreground=color.white, background=color.black, xmax=1,xmin=-1,ymax=1,ymin=-1)
gd2 = gdisplay(x=600, y=300, width=300, height=300, xtitle='t',
               title='Ball N', foreground=color.black, background=color.white)

f1 = gdots(color=color.green, gdisplay=gd)
f2 = gcurve(color=color.blue, gdisplay=gd)
f3 = gcurve(color=color.cyan, gdisplay=gd2)

random.seed(1)


# main code
t = 0
dt = 0.001
dts = 0

# initialization ends


class Container():


    def __init__(self, parts, limit_udlr):
        global r
        self.parts = parts  # list sections of container

        self.limit_udlr = limit_udlr

        # balls
        self.N = 1  # initial number of ball
        # mass of ball (just a random number, i dot car)
        self.ball_mass = 0.001

        self.v = random.uniform(-30, 30, [self.N, 3])  # velocity of balls
        for i in range(len(self.v)):
            #self.v[i][0] = 0
            # self.v[i][1] = 0 #random.random(size = None)*10 - 5
            self.v[i][2] = 0

        #pos_arr = random.uniform(-3,3,(N,3))
        self.pos_arr = zeros((self.N, 3))  # pos of ball

        for i in range(len(self.pos_arr)):
            self.pos_arr[i][2] = 0
            self.pos_arr[i][1] = random.random(size=None) * 6 - 3
            self.pos_arr[i][0] = random.random(size=None) * 6 - 3

        self.ball = [sphere(radius=r, make_trail=False,  # !vis
                            color=color.yellow) for i in range(self.N)]  # !vis

        self.ball[0].color = color.red  # !vis
        # self.ball[0].make_trail = True  #!vis
        for i in range(self.N):  # !vis
            self.ball[i].pos = vector(self.pos_arr[i])  # !vis

    def OnUpdate(self):
        '''
        The main update function.
        '''
        for j in range(self.N):
            for k in range(2):
                # update ball position array
                self.pos_arr[j][k] += self.v[j][k] * dt

            # update visual ball position #!vis
            self.ball[j].pos = vector(self.pos_arr[j])
            #'''  ball hit detection

            # all pairs of atom-to-atom vectors
            r_array = self.pos_arr - self.pos_arr[:, newaxis]
            # atom-to-atom distance squared
            rmag = sum(square(r_array), -1)
            hit = nonzero((rmag < 4 * r**2) - identity(self.N))
            hitlist = zip(hit[0], hit[1])
            for p, q in hitlist:
                # check if approaching
                if sum((self.pos_arr[p] - self.pos_arr[q]) * (self.v[p] - self.v[q])) < 0:
                    self.v[p], self.v[q] = vcollision(
                        self.pos_arr[p], self.pos_arr[q], self.v[p], self.v[q])
                    #print('ball hit')
            #'''

            for part in self.parts:  # detect collision between wall & balls
                wall = part.wall_list
                for i in range(len(wall) - 1):
                    w = wall[i] - wall[i + 1]
                    f = vector(-w[1], w[0])  # 法向量

                    if checkhit(wall[i], wall[i + 1], self.pos_arr[j], r) and dot([self.v[j][0] - part.v[0], self.v[j][1] - part.v[1], 0], f) <= 0:

                        # to calculate force (roughly)
                        dp = self.ball_mass * \
                            (self.v[j] - reflect(w, self.v[j], part.v))
                        part.stored_momentum += dp
                        self.v[j] = reflect(w, self.v[j], part.v)

        for part in self.parts:  # Wrong indent makes it violent....
            part.update_pos(dt)  # update wall position

    def add_ball(self, pos, vel):
        '''
        pos,v should be list with 3 variables
        '''
        self.ball.append(sphere(radius=r, make_trail=False,
                                color=color.yellow))  # !vis
        self.pos_arr = append(self.pos_arr, [pos], axis=0)
        self.v = append(self.v, [vel], axis=0)
        self.N += 1
        #print('NOW N = %d'%self.N)

    def del_ball(self, index):
        #print('del ball %d' % index)

        self.ball[index].visible = False  # !vis
        del self.ball[index]  # !vis
        self.pos_arr = delete(self.pos_arr, index, 0)
        self.v = delete(self.v, index, 0)
        self.N -= 1

    def get_force(self, index, passed_time):
        return self.parts[index].get_force(passed_time)


foil = naca.shiftscale(naca.main(int('0020'), 10), shift=(10, 0), scale=5)

pipe2 = [[0, 3], [5, 3], [8, 2], [22, 2], [
    22, -2], [8, -2], [5, -3], [0, -3]]  # pipe

flow = Container(parts=[Wall(pipe2, v=vector(0, 0, 0)), Wall(
    foil, v=vector(0, 0, 0))], limit_udlr=(5, -5, 0, 20))

u_limit = flow.limit_udlr[0]
d_limit = flow.limit_udlr[1]
l_limit = flow.limit_udlr[2]
r_limit = flow.limit_udlr[3]

indicator = arrow(pos=vector(10, 0, 0), r=0.1, color=color.red, shaftwidth=0.1)
indicator_norm = arrow(pos=vector(10, 0, 0), r=0.1,
                       color=color.green, shaftwidth=0.1)

get_force_dts = 80
while True:
    rate(1/dt)
    t += dt
    dts += 1

    # average vel

    tmp, tmp2 = 0, 0
    avg, avg2 = 0, 0
    n1, n2 = 0, 0

    if dts % get_force_dts == 0:
        force_vec = flow.parts[1].get_force(get_force_dts*dt)
        indicator.axis = force_vec
        indicator_norm.axis = norm(force_vec)
        f1.plot(pos = (indicator_norm.axis[0],indicator_norm.axis[1]))

    flow.OnUpdate()

    if dts % 15 == 0:
        # pass
        #print('add ball')
        flow.add_ball(pos=[0, random.random(size=None) * 6 - 3, 0], vel=[
                      random.random(size=None) * 10 + 30, random.random(size=None) * 10 - 5, 0])
        #flow.add_ball(pos = [0,random.random(size = None)*6 - 3,0],vel = [50,0,0])

    # if dts % get_force_dts == 0:
        #f = abs(flow.get_force(0,get_force_dts*dt))
        #f1.plot(pos = (t,f))

    m = -1  # trying to delete a ball without problem
    while True:
        m += 1
        if m == flow.N:
            break

        if flow.pos_arr[m][0] > r_limit or flow.pos_arr[m][0] < l_limit or flow.pos_arr[m][1] > u_limit or flow.pos_arr[m][1] < d_limit:
            #print('prev N = %d' % N)
            flow.del_ball(m)  # delete ball out of range
            #print('after N = %d' % N)
            m -= 1

    f3.plot(pos=(t, flow.N))
