from functools import reduce

A =[[1,1,1,1,0,0,1,0,0,1],
    [0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,1,0,0,0],
    [1,1,0,1,1,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,1],
    [0,1,0,0,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [1,0,0,1,0,0,0,1,1,1],
    [0,0,0,0,0,0,0,0,0,0]]

def long_ships_body(a_row, pos, length = 0):
    if pos == -1 and length > 1:
        return [length]
    elif pos==-1 and length <=1:
        return []
    elif a_row[pos] == 0 and length > 1:
        return [length] + long_ships_body(a_row, pos-1)
    elif a_row[pos] == 1:
        return long_ships_body(a_row, pos - 1, length + a_row[pos])
    else:
        return long_ships_body(a_row, pos - 1)

def clear_longs_body(a_row, pos, length = 0):
    if pos == -1 and length != 1:
        return [0]
    elif pos==-1 and length ==1:
        return [1]
    elif a_row[pos] == 0 and length != 1:
        return clear_longs_body(a_row, pos-1) + [0]
    elif a_row[pos] == 0 and length == 1:
        return clear_longs_body(a_row, pos - 1) + [1]
    elif a_row[pos] == 1:
        return clear_longs_body(a_row, pos - 1, length + a_row[pos]) + [0]
    else:
        return clear_longs_body(a_row, pos - 1) + [0]

col = lambda x,i: list(map(lambda mat: mat[i], x))
transp = lambda m: list(map(lambda col_i: col(m, col_i), range(len(m[0]))))
clear_longs_row = lambda a_row: clear_longs_body(a_row, len(a_row) - 1)[:-1]
clear_longs_all_rows = lambda a_matr: list(map(lambda a_row: clear_longs_row(a_row), a_matr))
clear_longs_matr = lambda a_matr: transp(clear_longs_all_rows(transp(clear_longs_all_rows(a_matr))))
get_small_ship_count = lambda a_matr: reduce(lambda x,y: x + y,
    list(map(lambda a_row: reduce(lambda x,y: x + y, a_row), clear_longs_matr(a_matr))))
get_long_ship_list_row = lambda a_matr: reduce(lambda x,y: x + y,
    list(map(lambda i: long_ships_body(a_matr[i], len(a_matr[0])-1), range(len(a_matr)))))
get_long_ship_list = lambda a_matr: get_long_ship_list_row(a_matr) + get_long_ship_list_row(transp(a_matr))
get_long_ship_count = lambda a_matr: list(map( lambda i: (str(i) + "-палубные", get_long_ship_list(a_matr).count(i)), range(2, len(a_matr) + 1)))
get_all_ships_count = lambda a_matr: [('1-палубные', get_small_ship_count(a_matr) )] + get_long_ship_count(a_matr)

print(get_all_ships_count(A))