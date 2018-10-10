#from visual import*
from math import*

foil_origin = (0.25, 0.0)

def main(serial, rot_angle, z):
    # NACA-(A1,A2,A34)
    #serial = input("NACA WHAT?")
    #rot_angle = input("AOA?")
    global foil_origin

    dX = 0.01

    rot_angle = -radians(rot_angle)

    A1 = float(serial / 1000)
    A2 = float((serial / 100) % 10)
    A34 = float(serial % 100)

    T = A34 / 100
    X = 1.0
    C = 1.0
    M = A1 / 100

    P = A2 / 10
    O = foil_origin

    dX_finest = 0.0125
    dX_fine = 0.025
    dX_medium = 0.05
    dX_rough = 0.1

    if 0 < X < P * C:

        Yc = M * X / (P**2) * (2 * P - X / C)
        Tan_theta = (2 * M * (C * P - X)) / ((P**2) * C)

        Cos_theta = ((((P**2) * C)**2) /
                     (((2 * M * (C * P - X))**2) + (((P**2) * C)**2)))**0.5

        Sin_theta = (((2 * M * (C * P - X))**2) /
                     (((2 * M * (C * P - X))**2) + (((P**2) * C)**2)))**0.5

    else:

        Yc = M * (C - X) / ((1 - P)**2) * (1 + (X / C) - 2 * P)

        Tan_theta = (2 * M * (C * P - X)) / (((1 - P)**2) * C)

        Cos_theta = (((((1 - P)**2) * C)**2) /
                     (((2 * M * (C * P - X))**2) + ((((1 - P)**2) * C)**2)))**0.5

        Sin_theta = (((2 * M * (C * P - X))**2) /
                     (((2 * M * (C * P - X))**2) + ((((1 - P)**2) * C)**2)))**0.5

    # theta=(2*M*(C*P-X))/((P**2)*C)

    # Cos_theta=((((P**2)*C)**2)/(((2*M*(C*P-X))**2)+(((P**2)*C)**2)))**(1.0/2)

    # Sin_theta=(((2*M*(C*P-X))**2)/(((2*M*(C*P-X))**2)+(((P**2)*C)**2)))**(1.0/2)

    S1 = 0.2969 * ((X / C)**(0.5))
    S2 = (-0.126) * (X / C)
    S3 = (-0.3516) * (X / C)**2
    S4 = (0.2843) * (X / C)**3
    S5 = ((-0.1015) * ((X / C)**4))
    Yt = 5 * T * C * (S1 + S2 + S3 + S4 + S5)

    X_U = X - Yt * Sin_theta

    Y_U = Yc + Yt * Cos_theta

    X_L = X + Yt * Sin_theta

    Y_L = Yc - Yt * Cos_theta

    # Yt=5*T*C*(((0.2969)*((X/C)**(1/2)))+(-0.126)*(X/C)+((-0.3516)*((X/C)**2))+((0.2843)*((X/C)**3))+((-0.1015)*((X/C)**4)))

    t = 0

    final = []

    while (X > 0):  # DO UPPER PART
        if X <= 0.026:
            dX = dX_finest
        elif X <= 0.1:
            dX = dX_fine
        elif X <= 0.3:
            dX = dX_medium
        else:
            dX = dX_rough
        S1 = 0.2969 * ((X / C)**(0.5))
        S2 = (-0.126) * (X / C)
        S3 = (-0.3516) * (X / C)**2
        S4 = (0.2843) * (X / C)**3
        S5 = ((-0.1015) * ((X / C)**4))
        Yt = 5 * T * C * (S1 + S2 + S3 + S4 + S5)

        if 0 <= X < P * C:
            Yc = M * X / (P**2) * (2 * P - X / C)
            Tan_theta = (2 * M * (C * P - X)) / ((P**2) * C)

            Cos_theta = ((((P**2) * C)**2) / (((2 * M * (C * P - X))
                                               ** 2) + (((P**2) * C)**2)))**(1.0 / 2)

            Sin_theta = (((2 * M * (C * P - X))**2) /
                         (((2 * M * (C * P - X))**2) + (((P**2) * C)**2)))**(1.0 / 2)
        else:
            Yc = M * (C - X) / ((1 - P)**2) * (1 + (X / C) - 2 * P)
            Tan_theta = (2 * M * (C * P - X)) / (((1 - P)**2) * C)

            Cos_theta = (((((1 - P)**2) * C)**2) / (((2 * M * (C * P - X))
                                                     ** 2) + ((((1 - P)**2) * C)**2)))**(1.0 / 2)

            Sin_theta = (((2 * M * (C * P - X))**2) / (((2 * M *
                                                         (C * P - X))**2) + ((((1 - P)**2) * C)**2)))**(1.0 / 2)

        X_U = X - Yt * Sin_theta
        Y_U = Yc + Yt * Cos_theta

        X_L = X + Yt * Sin_theta
        Y_L = Yc - Yt * Cos_theta

        coor = [X_U, -Y_U]
        coor = rotate(angle=rot_angle, O=O, P=coor)
        final.append( (round(coor[0], 5), round(coor[1], 5), z) )
        # print(round(coor[0],3),round(coor[1],3))
        # print(round(X_L,3),round(Y_L,5))
        # print(round(X,3),round(Yt,5))
        
        
        X -= dX

    X = 0
    while (X < C - 2*dX):  # DO LOWER PART

        X += dX

        if X < 0.025:
            dX = dX_finest
        elif X < 0.1:
            dX = dX_fine
        elif X < 0.3:
            dX = dX_medium
        else:
            dX = dX_rough
        S1 = 0.2969 * ((X / C)**(0.5))
        S2 = (-0.126) * (X / C)
        S3 = (-0.3516) * (X / C)**2
        S4 = (0.2843) * (X / C)**3
        S5 = ((-0.1015) * ((X / C)**4))
        Yt = 5 * T * C * (S1 + S2 + S3 + S4 + S5)

        if 0 <= X < P * C:

            Yc = M * X / (P**2) * (2 * P - X / C)
            Tan_theta = (2 * M * (C * P - X)) / ((P**2) * C)

            Cos_theta = ((((P**2) * C)**2) / (((2 * M * (C * P - X))
                                               ** 2) + (((P**2) * C)**2)))**(1.0 / 2)

            Sin_theta = (((2 * M * (C * P - X))**2) /
                         (((2 * M * (C * P - X))**2) + (((P**2) * C)**2)))**(1.0 / 2)

        else:

            Yc = M * (C - X) / ((1 - P)**2) * (1 + (X / C) - 2 * P)

            Tan_theta = (2 * M * (C * P - X)) / (((1 - P)**2) * C)

            Cos_theta = (((((1 - P)**2) * C)**2) / (((2 * M * (C * P - X))
                                                     ** 2) + ((((1 - P)**2) * C)**2)))**(1.0 / 2)

            Sin_theta = (((2 * M * (C * P - X))**2) / (((2 * M *
                                                         (C * P - X))**2) + ((((1 - P)**2) * C)**2)))**(1.0 / 2)

        X_U = X - Yt * Sin_theta
        Y_U = Yc + Yt * Cos_theta
        X_L = X + Yt * Sin_theta
        Y_L = Yc - Yt * Cos_theta

        coor = [X_L, -Y_L]
        coor = rotate(angle=rot_angle, O=O, P=coor)
        final.append((round(coor[0], 5), round(coor[1], 5), z))
        # print(round(coor[0],3),round(coor[1],3))
        # print(round(X_U,3),round(Y_U,5))
        # print(round(X_L,3),round(Y_L,5))
        # print(round(X,3),round(Yt,5))

    # print(final)
    return final

def rotate(angle, O, P):
    x, y = P[0] - O[0], P[1] - O[1]
    x2 = cos(angle) * x - sin(angle) * y + O[0]
    y2 = sin(angle) * x - cos(angle) * y + O[1]

    return [x2, y2]


def shiftscale(points, shift, scale):
    global foil_origin
    O = foil_origin
    tmp = list(points)
    for p in tmp:
        p[0] -= O[0]
        p[1] -= O[1]
        p[0] *= scale
        p[1] *= scale
        p[0] += shift[0]
        p[1] += shift[1]
    return tmp


def gen_faces_pillar(poly):
    top = tuple(range(poly))
    bottom = tuple(range(poly, 2*poly))
    re = [top]
    for i in range(poly):
        ap = (i,i+1,i+1+poly,i+poly) if i != poly - 1 else (i,0,poly,poly+i)
        re.append(ap)
    re.append(bottom)
    return re

def gen_verts_pillar(serial, height):
    serial = int(serial)
    points = main(serial,0,0) + main(serial, 0, height)

    return points

if __name__ == '__main__':
    serial = int('0010')
    height = 10
    poly = len(main(10,0,0))
    verts = gen_verts_pillar(serial,height)
    faces = gen_faces_pillar(poly)
    print(verts)
    print(faces)
