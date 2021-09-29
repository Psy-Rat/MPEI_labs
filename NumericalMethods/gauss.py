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
        matrix[i] = div_string(matrix[i], matrix[i][i])
        if i < len(matrix):
            for j in range(i+1, len(matrix)):
                matrix[j] = sum_string(matrix[j],mult_string(matrix[i],-matrix[j][i]))
    return matrix

def n_gauss(matrix):
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






a = [[3,6,9],[12,6,3]]
b = [[0,3,3,12],[1,0,4,31],[4,3,0,12]]
a = n_gauss(a)
b = n_gauss(b)
print(b)
print(a)