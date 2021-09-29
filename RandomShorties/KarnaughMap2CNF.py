import math
import numpy as np
import sys


GrayCode = [[0, 0], [0, 1], [1, 1], [1, 0]]
def KarnoCoordinates(numb):
    y = [(numb//2)%2, numb%2]
    numb = (numb//2)//2
    x = [(numb//2)%2, numb%2]
    res = [x, y]
    fin = []
    for R in res:
        for i in range(len(GrayCode)):
            if (R[0]==GrayCode[i][0]) and (R[1]==GrayCode[i][1]):
                fin.append(i)
                break
    return fin
def KarnoCreate(f_code):
    result = [[0]*4 for i in range(4)]
    for i in range(len(f_code)):
        a = f_code[i]
        if f_code[i]=='1':
            T_coords = KarnoCoordinates(i)
            result[T_coords[0]][T_coords[1]] = 1
    return result
def CheckFull(T_Karno, simb):
    for x in T_Karno:
        for y in x:
            if y != simb:
                return 0
    return 1
def CheckLine(L_Karno, simb):
     for x in L_Karno:
         if x != simb:
             return 0
     return 1
def CountLine(T_Karno,simb):
    res = 0
    for i in T_Karno:
        if i==simb:
            res+=1
    return res
def KarnoClusterisation(T_Karno):
    T_buffer = [[0]*4 for i in range(4)]
    res =""
    '''HORISONTAL 8`s'''
    for i in range(len(T_Karno)):
        x = round((i+1)%4)
        buff = []
        buff.append(T_Karno[i])
        buff.append(T_Karno[x])
        if CheckFull(buff, 1)==1:
            T_buffer[i] = [1]*4
            T_buffer[x] = [1]*4
            if i==0:
                res+="!AV"
            elif i==1:
                res+="BV"
            elif i==2:
                res+="AV"
            elif i==3:
                res+="!BV"
    '''VERTICAL 8s'''
    for i in range(len(T_Karno)):
        j = round((i + 1) % 4)
        buff = [[x[i] for x in T_Karno],[x[j] for x in T_Karno]]
        if CheckFull(buff, 1)==1:
            for k in T_buffer:
                k[i] = 1
                k[j] = 1
            if i==0:
                res += "!CV"
            elif i==1:
                res += "DV"
            elif i==2:
                res += "CV"
            elif i==3:
                res += "!DV"
    '''HORISONTAL 4s'''
    for i in range(len(T_Karno)):
        if (CheckLine(T_buffer[i], 1)==0) and\
            (CheckLine(T_Karno[i], 1)==1):
            T_buffer[i] = [1] * 4
            if i==0:
                res += "(!A&!B)V"
            elif i==1:
                res += "(!A&B)V"
            elif i==2:
                res += "(A&B)V"
            elif i==3:
                res += "(A&!B)V"
    '''VERTICAL 4s'''
    for i in range(len(T_Karno)):
        buff_a = [x[i] for x in T_Karno]
        buff_b = [x[i] for x in T_buffer]
        if (CheckLine(buff_b, 1)==0) and \
            (CheckLine(buff_a, 1)==1):
            for k in T_buffer:
                k[i] = 1
            if i==0:
                res += "(!C&!D)V"
            elif i==1:
                res += "(!C&D)V"
            elif i==2:
                res += "(C&D)V"
            elif i==3:
                res += "(C&!D)V"
    '''SQUARE 4s'''
    for i in range(len(T_Karno)):
        for j in range (len(T_Karno)):

            buff = [T_Karno[i][j],T_Karno[i][(j+1)%4],
                    T_Karno[(i+1)%4][j],T_Karno[(i+1)%4][(j+1)%4]]
            if (CheckLine(buff, 1)==1) and ((T_buffer[i][j] != 1) or (T_buffer[(i+1)%4][j] != 1) or (T_buffer[i][(j+1)%4] != 1) or (T_buffer[(i+1)%4][(j+1)%4] != 1)):
                res+="(" + GiveDiz([[i,j],[i,(j+1)%4],[(i+1)%4,j],[(i+1)%4,(j+1)%4]]) + ")&"
                T_buffer[i][j] = 1
                T_buffer[(i+1)%4][j] = 1
                T_buffer[i][(j+1)%4] = 1
                T_buffer[(i+1)%4][(j+1)%4] = 1
    '''HORISONTAL 2s'''
    for i in range(len(T_Karno)):
        for j in range (len(T_Karno)):
            buff = [T_Karno[i][j],T_Karno[i][(j+1)%4]]
            if (CheckLine(buff, 1)==1) and ((T_buffer[i][j] != 1) or (T_buffer[i][(j+1)%4] != 1)):
                res+="("+GiveDiz([[i,j],[i,(j+1)%4]]) + ")&"
                T_buffer[i][j] = 1
                T_buffer[i][(j+1)%4] = 1
    '''VERTICAL 2s'''
    for i in range(len(T_Karno)):
        for j in range (len(T_Karno)):
            buff = [T_Karno[i][j],T_Karno[(i+1)%4][j]]
            if (CheckLine(buff, 1)==1) and ((T_buffer[i][j] != 1) or (T_buffer[(i+1)%4][j] != 1)):
                res+="("+GiveDiz([[i,j],[(i+1)%4,j]]) + ")&"
                T_buffer[i][j] = 1
                T_buffer[(i+1)%4][j] = 1

    return res[:-1]
def GiveDiz(T_Cooords):
    Gray_M = []
    res = ""
    for coor in T_Cooords:
        buff = []
        if coor[0]==0:
            buff.append(0)
            buff.append(0)
        if coor[0]==1:
            buff.append(0)
            buff.append(1)
        if coor[0]==2:
            buff.append(1)
            buff.append(1)
        if coor[0]==3:
            buff.append(1)
            buff.append(0)
        if coor[1]==0:
            buff.append(0)
            buff.append(0)
        if coor[1]==1:
            buff.append(0)
            buff.append(1)
        if coor[1]==2:
            buff.append(1)
            buff.append(1)
        if coor[1]==3:
            buff.append(1)
            buff.append(0)

        Gray_M.append(buff)
    for i in range(len(Gray_M[0])):
        buff = [x[i] for x in Gray_M]
        if (CheckLine(buff, 1)==1):
            if i==0:
                res += "A&"
            if i==1:
                res += "B&"
            if i==2:
                res += "C&"
            if i==3:
                res += "D&"
        if (CheckLine(buff, 0)==1):
            if i==0:
                res += "!A&"
            if i==1:
                res += "!B&"
            if i==2:
                res += "!C&"
            if i==3:
                res += "!D&"
    res = res[:-1]
    return res
def GiveKon(T_Cooords):
    Gray_M = []
    res = ""
    for coor in T_Cooords:
        buff = []
        if coor[0]==0:
            buff.append(0)
            buff.append(0)
        if coor[0]==1:
            buff.append(0)
            buff.append(1)
        if coor[0]==2:
            buff.append(1)
            buff.append(1)
        if coor[0]==3:
            buff.append(1)
            buff.append(0)
        if coor[1]==0:
            buff.append(0)
            buff.append(0)
        if coor[1]==1:
            buff.append(0)
            buff.append(1)
        if coor[1]==2:
            buff.append(1)
            buff.append(1)
        if coor[1]==3:
            buff.append(1)
            buff.append(0)
        Gray_M.append(buff)
    for i in range(len(Gray_M[0])):
        buff = [x[i] for x in Gray_M]
        if (CheckLine(buff, 1)==1):
            if i==0:
                res += "!AV"
            if i==1:
                res += "!BV"
            if i==2:
                res += "!CV"
            if i==3:
                res += "!DV"
        if (CheckLine(buff, 0)==1):
            if i==0:
                res += "AV"
            if i==1:
                res += "BV"
            if i==2:
                res += "CV"
            if i==3:
                res += "DV"
    res = res[:-1]
    return res


Test = [[1,1,0,1],
        [1,0,0,1],
        [0,0,0,0],
        [0,1,1,0]]
print(KarnoClusterisation(Test))

'''
filename = "input.txt"
function_code = ""

try:
    f = open(filename,'r')
except IOError as e:
    print ("Такого файла не существует")
    sys.exit(-4)
else:
    function_code = f.readline()
    print("Код функции: ",function_code)
    if len(function_code) != 16:
        print(
            "Извините, в данной версии программы поддерживаются только функции с 4-мя переменными. Код функции должн иметь 16 знаков.")
        sys.exit(0)
    f.close()

Karno = KarnoCreate(function_code)
print("Карта карно:")
for x in Karno:
    print(x)
KarnoClusterisation(Karno)'''