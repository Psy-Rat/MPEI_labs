import math
import numpy as np
import matplotlib.pyplot  as plt

Australia=[[],[]]
Australia[0] = [1950,1960,1970,1980,1990,2000,2013,2015,2007]
Australia[1] = [8.2,10.0,13.0,14.7,17,19.5,23.8,25.0,21.0]
def div_string(i_str, diver):
    n_str = []
    for x in i_str:
         n_str.append(x/diver)
    return n_str
def mult_string(i_str, multiplier):
    n_str = []
    for x in i_str:
         n_str.append(x*multiplier)
    return n_str
def sum_string(i_str, j_str):
    n_str = []
    for x,y in zip(i_str, j_str):
        n_str.append(x + y)
    return n_str
def gauss(matrix):
    answer = []
    for i in range(len(matrix)):
        for x in range(i, len(matrix)):
            if matrix[x][i] != 0.0:
                buf = matrix[i]
                matrix[i] = matrix[x]
                matrix[x] = buf
                break
        matrix[i] = div_string(matrix[i],matrix[i][i])
        for j in range(len(matrix)):
            if j is i:
                continue
            matrix[j] = sum_string(matrix[j], mult_string(matrix[i], -matrix[j][i]))
    for i in range(len(matrix)):
        answer.append(matrix[i][-1] / matrix[i][i])
    return answer
def lagr_fun(knotes, x):
    r_sum = 0.0
    for i in range(len(knotes[0])):
        r_mul = 1.0
        for j in range(len(knotes[1])):
            if j is i:
                continue
            else:
                T_kn = knotes[0][i]
                T_kn2 = knotes[0][j]
                T_kn3 = knotes[0][j]
                t_d = knotes[0][i] - knotes[0][j]
                s_d = x - knotes[0][j]
                r_mul *= (x - knotes[0][j])/(knotes[0][i] - knotes[0][j])
        r_sum+=r_mul * knotes[1][i]
    return  r_sum
def min_squares(knotes, power):
    ExpSis = []
    ExpDia = []
    ExpAns = []
    power+=1
    for i in range(power*2-1):
        Sum = 0
        for x in (knotes[0]):
            Sum += x**i
        ExpDia.append(round(Sum, 7))
    for i in range(power):
        Sum = 0
        for x,y in zip(knotes[0],knotes[1]):
            Sum+=y*(x**i)
        ExpAns.append(Sum)
    for i in range(power):
        ExpSis.append(ExpDia[i:i+power])
        ExpSis[i].append(ExpAns[i])
    return gauss(ExpSis)
def solve_polynomial(pol,x):
    Ans = 0
    for i in range(len(pol)):
        Ans += pol[i]*(x**i)
    return Ans

'''Функции, полученные с помощью МНК'''
fun_2SQ = min_squares([Australia[0][1:-1], Australia[1][1:-1]], 2)
fun_1SQ = min_squares([Australia[0][1:-1], Australia[1][1:-1]], 1)
"""Графики Лагранжа"""
t = np.arange(Australia[0][0], Australia[0][-2] + 1, 1)
L = []
F1 = []
F2 = []
for i in t:
    L.append(lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], i))
    F1.append(solve_polynomial(fun_1SQ, i))
    F2.append(solve_polynomial(fun_2SQ, i))

plt.figure(1)
plt.plot(t,L, "b-", label = "lagrange polynomial")
plt.plot(t,F1, "g-", label = "least squares: 1")
plt.plot(t,F2, "r-", label = "least squares: 2")

plt.title('Australia population')
plt.xlabel('Years')
plt.ylabel('Population (millions)')
plt.grid(True)
plt.scatter(Australia[0][1:-1],Australia[1][1:-1])
plt.scatter([Australia[0][0],Australia[0][-1]], [Australia[1][0],Australia[1][-1]],s=20, marker= 'x')
plt.legend()
plt.show()

print("Результаты, полученные с помощью глобальной интерполяции:\n",
      "1950:",lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], 1950),"\n",
      "2016:",lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], 2016),"\n",
      "2007:",lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], 2007),"\n",
      "Разница в промежуточном значении:",math.fabs(lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], 2007) - Australia[1][-1]),"\n",
      "Разница в экстраполируемом значении(1950):",math.fabs(lagr_fun([Australia[0][1:-1], Australia[1][1:-1]], 2007) - Australia[1][0]),"\n"
      )
print("Результаты, полученные с помощью МНК 1-го порядка:\n",
      "1950:",solve_polynomial(fun_1SQ, 1950),"\n",
      "2016:",solve_polynomial(fun_1SQ, 2016),"\n",
      "2007:",solve_polynomial(fun_1SQ, 2007),"\n",
      "Разница в промежуточном значении:",math.fabs(solve_polynomial(fun_1SQ, 2007) - Australia[1][-1]),"\n",
      "Разница в экстраполируемом значении:",math.fabs(solve_polynomial(fun_1SQ, 1950) - Australia[1][0]),"\n"
      )
print("Результаты, полученные с помощью МНК 2-го порядка:\n",
      "1950:",solve_polynomial(fun_2SQ, 1950),"\n",
      "2016:",solve_polynomial(fun_2SQ, 2016),"\n",
      "2007:",solve_polynomial(fun_2SQ, 2007),"\n",
      "Разница в промежуточном значении:",math.fabs(solve_polynomial(fun_2SQ, 2007) - Australia[1][-1]),"\n",
      "Разница в экстраполируемом значении:",math.fabs(solve_polynomial(fun_2SQ, 1950) - Australia[1][0]),"\n"
      )