### ### ### ### ### ### ###
### Расчеты непосредственно ###
### ### ### ### ### ### ###
###   N1   ###
### ### ###
import numpy as np
import scipy.integrate as intgr
import matplotlib.pyplot as plt
import amen as am
A_arr = [1, 2, 1]
N_arr = [-4, -3, 2]
L_arr  = [1, 1, 1]
E = 1

arr_red(L_arr) #преобразуем длинны участков в координаты смены участков

length = L_arr[-1]
#Cоздадим массив с нормальными силами, возникающими от внешних концетрических

forces = lambda x: map(lambda a, b: normal_concetrated_force_gen(a, b)(x), N_arr, L_arr)

#Найдем функцию N(z) - функцию нормальных усилий, возникающей 
#в участке стержня на расстоянии x от начала стержня
N_x = lambda x: reduce( lambda a, b: a + b, forces(x)) #от внешних сил
R_S = N_x(L_arr[-1]+1)
R_l = normal_concetrated_force_gen(R_S, 0)
N_z = lambda x: N_x(x) + R_l(x) #С учетом р. опоры - N(z)
a_f = width_function_gen(A_arr, L_arr) #функция толщины
e_f = lambda x: E #функция коэффициента Е
w_f = enlongation_gen(N_z, e_f, a_f) #функция удлинения w_f
ten_f = tense_gen(N_z, a_f) #функция нормальных напряжений

#построение графика
diag_list([a_f, N_z, ten_f, w_f], 0, 3, 1000) 