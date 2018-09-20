# -*- Encoding: UTF-8 -*-
from turtle import*
import NACA_produce as naca


def is_data(string):
    list1 = string.split(' ')
    list2 = []
    for i in range(len(list1)):
        if list1[i] != '':
            list2.append(list1[i])
    for i in range(len(list2)):
        try:
            list2[i] = float(list2[i])
        except:
            return False
    return True


def convert(string):
    list1 = string.split(' ')
    list2 = []
    for i in range(len(list1)):
        if list1[i] != '':
            list2.append(list1[i])
    if list2 != []:
        return [float(list2[0]), float(list2[1])]
    else: return None

length = 500

#name = input("input NACA airfoil file name, including .txt : ") #used while testing
#name = "naca4412.txt"
'''
print('loading '+name+' ...')
f = open(name,mode='r')
s = f.read()
final = []
line_list = s.split('\n')
for line in line_list:
    if is_data(line) and convert(line) != None:
        final.append(convert(line))
        #print(convert(line))
    #else:
        #print(line)
print('file loaded, total point: %d'%len(final))
'''
name = str(input('input NACA serial number:\n>>> '))
serial = int(name)
angle = int(input('input angle:\n>>> '))
final = naca.main(serial, angle)
print('total points: %d' % len(final))

orig_x, orig_y = -length/2, 0
color("#FD8008", "#FECC66")

#draw the airfoil
speed(0)
penup()
goto(int(final[0][0]*length)-length/2,
     int(final[0][1]*length))
pendown()
begin_fill()
for point in final:
    goto(int(point[0]*length)-length/2, int(point[1]*length))
end_fill()

#draw axis
speed(0)
color("#000000", "#000000")
penup()
goto(-length/2, length/2)
pendown()
goto(-length/2, -length/2)
penup()
goto(-length*5/8, 0)
pendown()
goto(length*5/8, 0)

#draw grid
color("#888888", "#000000")
penup()
goto(orig_x, orig_y)
setheading(270)
for i in range(10):
    goto(orig_x+length*(i+1)/10, length/2)
    pendown()
    forward(length)
    penup()
setheading(0)
for i in range(5):
    goto(-length*5/8, length*(i+1)/10)
    pendown()
    forward(length*10/8)
    penup()
for i in range(5):
    goto(-length*5/8,-length*(i+1)/10)
    pendown()
    forward(length*10/8)
    penup()
goto(0,length/2)
write('NACA '+name+', angle='+str(angle)+'°', True, align="center", font=("PT Mono", 30, "normal"))
done()