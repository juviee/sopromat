### ### ### ### ### ### ###
### Расчеты непосредственно ###
### ### ### ### ### ### ###
###   N2   ###
### ### ###
import numpy as np
import scipy.integrate as intgr
import matplotlib.pyplot as plt
import amen as am

L_arr  = [1, 1, 2]
A_arr = [2, 1, 1]

F_con_arr = [-4, -3, 2]
F_dist_arr = [lambda x: -3, lambda x: 0, lambda x: 1]

l_dist_arr = list(L_arr) #создадим список длин участков для создания ф. распр. сил

arr_red(L_arr)#преобразуем длинны в координаты

n_conc = lambda x: map(lambda a, b: normal_concetrated_force_gen(a, b)(x), F_con_arr, L_arr)

f_dist = lambda x: map(lambda a, b, c: disturbed_force_gen(a, b, c)(x), F_dist_arr, l_dist_arr, L_arr)
n_dist = map(lambda x:normal_disturbed_force_gen(x), f_dist)

n_f_x = lambda x: reduce(lambda a, b: a + b, f_dist(x))
n_d_x = lambda x: reduce(lambda a, b: a + b, n_dist(x))

N_x = lambda x: n_f_x(x) + n_d_x(x)

R_S = N_x(L_arr[-1]+1)
R_l = normal_concetrated_force_gen(R_S, 0)
n_z = lambda x: N_x(x) + R_l(x)

a_f = width_function_gen(A_arr, L_arr)
e_f = lambda x: E

w_f = enlongation_gen(n_z, e_f, a_f) 
ten_f = tense_gen(n_z, a_f)

