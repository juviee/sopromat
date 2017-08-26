import numpy as np
import scipy.integrate as intgr
import matplotlib.pyplot as plt

heaviside = lambda x: 0.5 * (np.sign(x) + 1)
gap_function = lambda a, l: lambda x: heaviside(x-a) * heaviside(a + l - x)

normal_concetrated_force_gen = lambda N, x0 = 0: lambda x: (-1) * N * heaviside(x - x0)

disturbed_force_gen = lambda f, l, x0 = 0: lambda x: f(x - x0) * gap_function(x0, l)(x)
normal_disturbed_force_gen = lambda f: lambda x:(-1) * intgr.quad(f, 0, x)[0] #use with "disturbed_force_gen function"
overall_disturbed_force = lambda f, l: intgr.quad(lambda x: intgr, 0, l)[0] #use with original d.force function

enlongation_gen = lambda N, E, A: lambda x: intgr.quad(lambda x: N(x)/E(x)/A(x), 0, x)[0]
tense_gen = lambda N, A: lambda x: N(x)/A(x)
#_gen functions used to produce final functions 

#use if defined allowed enlongation
reaction_force_left= lambda w_max, length, E, A: (-1) * w_max * intgr.quad(lambda x: w_max*E*A(x)/x)[0]

def function_addition(a, b):
    return lambda x: a(x) + b(x)

def width_function_gen(A, L):
    #a_f = list()
    a_f = list([lambda x: A[0]*gap_function(0, L[0])(x)])
    a_f_gen = lambda j: lambda x: a_f[j-1](x) + A[j]*gap_function(L[j-1], L[j] - L[j - 1])(x)
    for i in range(1, len(A)):
        a_f.append(a_f_gen(i))
    return a_f[len(A) - 1]
        

def diagram(f, l,r, name = '', d = -1):
    if d == -1:
        d = 1000
    x = np.arange(l, r, abs(float(l - r))/d)
    y = map(f, x)
    ymx = max(y)
    ymn = min(y)
    #Настроим сетку
    plt.rc('text', usetex=False)
    plt.plot(x, y, color='green')
    plt.axhline(xmax = r)
    plt.axvline(ymax = ymx)
    plt.grid()
    plt.axis([l, r, ymn, ymx*1.5],'tight')
    #Создадим название графика
    plt.title(name)
    plt.show()
def diag_list(f, l, r, d = -1):
    if d == -1:
        d = 1000
    x_ar = np.arange(l, r, abs(float(l - r))/d)
    y_ar = map(lambda a: map(a, x_ar), f)
    
    for i in range(len(y_ar)):
        y_t = y_ar[i]
        ymx = max(y_t)
        ymn = min(y_t)
        d = ymx - ymn
        plt.axhline(xmax = r, color = 'black')
        plt.axvline(ymax = ymx, color = 'black')
        plt.grid()
        plt.subplot(len(y_ar), 1, i+1)
        plt.plot(x_ar, y_t)
        plt.axis([l, r, ymn - d*0.01, ymx + d*0.1])
    
    plt.show()
    
def arr_red(iterble):
    cpr = list(iterble)
    for i in range(len(iterble)):
        iterble[i] = reduce(lambda a, b: a + b, cpr[:i + 1])

if __name__=='__main__':
    L_arr  = [1, 1, 2]
    A_arr = [2, 1, 1]
    E = 1
    F_con_arr = [-4, -3, 2]
    F_dist_arr = [lambda x: -3, lambda x: 0, lambda x: 1]

    l_dist_arr = list(L_arr) #создадим список длин участков для создания ф. распр. сил

    arr_red(L_arr)#преобразуем длинны в координаты

    n_conc = lambda x: map(lambda a, b: normal_concetrated_force_gen(a, b)(x), F_con_arr, L_arr)

    f_ddist = lambda x: map(lambda a, b, c: disturbed_force_gen(a, b, c)(x), F_dist_arr, l_dist_arr, L_arr)
    f_dist = lambda x: reduce(lambda a, b: a + b, f_ddist(x))

    n_f_x = lambda x: reduce(lambda a, b: a + b, n_conc(x))
    n_d_x = normal_disturbed_force_gen(f_dist)

    N_x = lambda x: n_f_x(x) + n_d_x(x)

    R_S = N_x(L_arr[-1]+1)
    R_l = normal_concetrated_force_gen(R_S, 0)
    n_z = lambda x: N_x(x) + R_l(x)

    a_f = width_function_gen(A_arr, L_arr)
    e_f = lambda x: E

    w_f = enlongation_gen(n_z, e_f, a_f) 
    ten_f = tense_gen(n_z, a_f)

    #print(w_f(3))
    diag_list([a_f, n_z, ten_f], 0, 3, 100)
