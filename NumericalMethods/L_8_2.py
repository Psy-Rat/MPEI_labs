import math
import numpy as np
import matplotlib.pyplot  as plt
'''Лямбда-функции вычисления заданной функции,
    интеграла заданной функции вычесленного аналитически,
    длины шага'''
func = lambda x: math.exp(x)*math.sin(x)
func_I = lambda x: math.exp(x) * (math.sin(x) - math.cos(x)) / 2
h = lambda a,b,n: (b-a)/(2**n)

A = 0
B = 3
N = 10
EPS = 10**-6

''' Различнные вычисления интегралов'''
def Integral_sq(a,b,adding):
    Sum = 0
    padding = adding / 2
    i=0
    while i < b :
        Sum += func(i + padding)*adding
        i+=adding
    return Sum
def Integral_y(a,b,adding):
    Ih1 = Integral_sq(a,b,adding)
    Ih2 = Integral_sq(a,b,adding/2)
    R = (Ih2 - Ih1) / 3
    return Ih2 + R
def Integral_analytical(a,b):
    return func_I(b) - func_I(a)

print("Аналитически вычесленное интеграла:",
      "\nI:",Integral_analytical(A,B))
print("Значение интеграла, полученное с помощью метода центральных прямоугольников: ",
      "\nI:",Integral_sq(A, B, h(A, B, 5)),"h:",h(A, B, 5))
print("Метод центральных прямоугольников с шагом, равным половине предыдущего: ",
      "\nI:",Integral_sq(A, B, h(A, B, 5)/2),"h:",h(A, B, 5)/2)
print("Уточнённый интеграл по методу Рунге:",
      "\nI:",Integral_y(A, B, h(A, B, 5)))

R1 = []
R2 = []
R3 = []
t = np.arange(0,N,1)
for n in range(N):
    I = Integral_analytical(A, B)
    R1.append(math.fabs(I - Integral_sq(A, B, h(A, B, n))))
    R2.append(math.fabs(I - Integral_sq(A, B, 1/2*h(A, B, n))))
    R3.append(math.fabs(I - Integral_y(A, B, h(A, B, n))))
plt.plot(t,R1,"bo-", label ="R1")
plt.plot(t,R2,"go-", label ="R2")
plt.plot(t,R3,"r^-", label ="R3")
plt.legend()
plt.grid(True)
plt.show()