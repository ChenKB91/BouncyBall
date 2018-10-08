# -*- coding: UTF-8 -*-
from visual import*
'''
----
    To achieve great things, two things are needed;
    a plan, and not quite enough time.  -- Leonard Bernstein
----
    To write good code, two things are required;
    a nice looking editor, and a good amount of coffee.  -- CKB
----
Algorithm:
1. initialize:
    class wall: generate 1 piece of wall, capable of moving
                also good for calculating pressure and force etc.

2. on update:
    delete balls which are out of range
    add N balls according to flow rate

    get balls bounced off by the wall
    get balls bounced by one another
    change their speed
    update position of the ball according to speed

    calculate force by (momentum changed)/(time passed)
'''


class Wall():  # A piece of wall, makes up class Container

    def __init__(self, wall_list, v):
        self.wall_list = vectorfy(wall_list)
        self.visual = curve(pos=wall_list)
        self.v = vector(v)
        self.stored_momentum = vector((0, 0, 0))

    def update_pos(self, dt):
        for point in self.wall_list:
            point[0] += self.v[0] * dt
            point[1] += self.v[1] * dt
        self.visual.pos = self.wall_list

    def get_force(self, passed_time):
        re = self.stored_momentum / passed_time
        self.stored_momentum = vector((0, 0, 0))
        return re


def dist(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def reflect(w, v, w_v):  # ball hit wall
    '''
    w,v must be list/array/vector with 2 numbers
    '''
    w, v, w_v = vector(w), vector(v), vector(w_v)
    v = v - w_v  # 相對速度
    f = vector(-w[1], w[0], 0)  # 法向量
    unit_f = f / abs(f)  # 法向量的單位向量
    re = v + abs(dot(v, f) / abs(f)) * unit_f * 2

    if abs(abs(re) - abs(v)) <= 0.00001 * abs(v):  # small number to fix floating point stuff
        if dot(v, f) < 0:
            return re + w_v
        else:
            #print('!!!wrong side!!!')
            return v
    else:
        #print("back hit")
        w = -w
        f = vector(-w[1], w[0], 0)  # 法向量
        unit_f = f / abs(f)  # 法向量的單位向量
        if dot(v, f) < 0:
            re = v + abs(dot(v, f) / abs(f)) * unit_f * 2
            return re + w_v
        else:
            #print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
            return v


def checkhit(w1, w2, b, r):
    wx1, wy1 = w1[0], w1[1]
    wx2, wy2 = w2[0], w2[1]
    bx, by = b[0], b[1]
    area = 0.5 * abs(wx1 * wy2 + wx2 * by + bx * wy1 -
                     wy1 * wx2 - wy2 * bx - by * wx1)
    wall = sqrt((wx1 - wx2)**2 + (wy1 - wy2)**2)
    # (2*area/wall)<=r : distance to wall <= radius
    # (dist(bx,by,wx1,wy1)<=r or dist(bx,by,wx2,wy2)<=r) : hit edge
    # and not(dist(bx,by,wx1,wy1)>wall or dist(bx,by,wx2,wy2)>wall) : make
    # sure hit in the middle, not outside
    if ((2 * area / wall) <= r or (dist(bx, by, wx1, wy1) <= r or dist(bx, by, wx2, wy2) <= r)) and not(dist(bx, by, wx1, wy1) > wall or dist(bx, by, wx2, wy2) > wall):
        return True
    else:
        return False


def vcollision(a1p, a2p, a1v, a2v):  # ball hit ball
    v1prime = a1v - (a1p - a2p) * sum((a1v - a2v) *
                                      (a1p - a2p)) / sum((a1p - a2p)**2)
    v2prime = a2v - (a2p - a1p) * sum((a2v - a1v) *
                                      (a2p - a1p)) / sum((a2p - a1p)**2)
    return v1prime, v2prime


def vectorfy(points):
    for i in range(len(points)):
        points[i] = vector(points[i])
    return points
