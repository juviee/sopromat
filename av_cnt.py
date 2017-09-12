#! /usr/bin/env python3
# -*- coding:utf-8 -*-

#стат. обработка результатов: 
from scipy.stats import t
import locale
import sys
def answ(data, trusted_probability):
    '''Функция берет массив данных, полученных в результате 
    вычисления, например интеграла по гистерезису, доверительную 
    вероятность, в результате чего возращает среднее значение и 
    допустимое отклонение по этой вероятности согласно распределению
    Cтьюдента (<X> +/- k(Prob, N) * \sigma)'''
   
    average = 0
    N = 0
    standard_variance = 0
    k = 0
    dispersion = 0
    
    N = len(data)
    for x in data: average += x/N
    for x in data: standard_variance += (average-x)**2
    k = abs(t.ppf((1-trusted_probability)/2, N))
    #t.ppf - обратная функция от стандартного 
    #распределения Стьюдента(интегрального)
    dispersion = standard_variance*k
    ans = [average, dispersion]
    return ans

if __name__=='__main__':
    '''Программа берет на вход название файла, доверителную вероятность.
    Файл вывода из программы hysterezis.py, доверительная 
    вероятность опциональна, по умолчанию Prob = 0.9'''
    data=list()
    with open(sys.argv[1], 'r', encoding='utf-8') as fi:
        fi.__next__()
        data = [locale.atof(num) for num in fi]
    try:
        Prob = locale.atof(sys.argv[2])
    except IndexError:
        Prob = 0.9
    result = answ(data, Prob)

    with open(sys.argv[1], 'a', encoding = 'utf-8') as fi:
        fi.write('W = {0[0]:.6}\N{PLUS-MINUS SIGN}{0[1]:.6}\n'.format(result))
        fi.write('При доверительной вероятности P = {0}'.format(Prob))
