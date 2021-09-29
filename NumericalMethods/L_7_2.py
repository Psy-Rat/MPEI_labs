import numpy as np
import matplotlib.pyplot  as plt

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
def choose_some_knotes(t, s, power):
    res =[[],[]]
    step = len(t)//(power - 1)
    for i in range(power -  1):
        res[0].append(t[i*step])
        res[1].append((s[i*step]))
    res[0].append(t[-1])
    res[1].append(s[-1])
    return res

power = 10
smoothness = 2000

t = np.linspace(-2, 2, smoothness)
t_part1 = t[:len(t)//2]
t_part2 = t[len(t)//2:]
s = np.sin(np.abs(t))

knotes = choose_some_knotes(t,s,power)
knotes_part1 = choose_some_knotes(t_part1, s[:len(s)//2], power)
knotes_part2 = choose_some_knotes(t_part2, s[len(s)//2:], power)

interpolated_s = []
particly_int_s1 = []
particly_int_s2 = []

for curr_p in t_part1:
    particly_int_s1.append(lagr_fun(knotes_part1, curr_p))
for curr_p in t_part2:
    particly_int_s2.append(lagr_fun(knotes_part2, curr_p))
for curr_p in t:
    interpolated_s.append(lagr_fun(knotes,curr_p))


error = np.max(np.abs(s-interpolated_s))
error_part = max(np.max(np.abs(s[:len(s)//2] - particly_int_s1)),
                 np.max(np.abs(s[len(s)//2:] - particly_int_s2)))

print("Ошибка при интерполировании функции по всему отрезку:", error)
print("Ошибка при интерполировании функции по частям:", error_part)
plt.figure(1)
plt.title("Source function graphics")
plt.plot(t,s)
plt.grid()
plt.scatter(knotes[0], knotes[1])

plt.figure(2)
plt.title("Interpolated function graphics")
plt.plot(t,interpolated_s)
plt.grid()
plt.scatter(knotes[0], knotes[1])

plt.figure(3)
plt.title("Partially interpolated function graphics")
plt.plot(t_part1,particly_int_s1, "r-")
plt.plot(t_part2,particly_int_s2, "r-")
plt.grid()
plt.scatter(knotes[0], knotes[1])
plt.show()