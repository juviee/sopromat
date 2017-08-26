#! /usr/bin/env python3
# -*- coding:utf-8 -*-
#Анализ опыта n2
import sys
import csv
import locale as lc
def sympson_integration(x, y):
#интгрирование методом Симпсона
    base = lambda h, y: (y[0]+4*y[1]+y[2])*h/6
    i = 2
    S = 0
    while i<len(x):
        a = (y[i-2], y[i-1], y[i])
        h = x[i] - x[i-2]
        S += base(h, a)
        i+=2
#Поскольку количество полученных измерений во время опыта
#может не совпадать с условием N%2==1, то требуется дополнительная
#проверка и, при нарушении условие, минимизировать погрешность
#сложив последнее измерение к общему интегралу через метод
#трапеций
    if (i-2+1) > len(x):
        S+=(x[-1]-x[-2])*(y[-2]+y[-1])/2
    return S

if __name__=='__main__':
    energy = list()
    lc.setlocale(lc.LC_NUMERIC, "ru_RU.utf8")
    cycle_length = -1.0
    with open(sys.argv[1], encoding='cp1251', newline='') as f_in:
        table = csv.reader(f_in, delimiter=';')
        table.__next__()
        rr = table.__next__()
        cycle = int(rr[3])
        length_buf = -1.0
        x_buf = list([lc.atof(rr[6])/1000])
        flag = 1
        y_buf = list([lc.atof(rr[7])])
        for row in table:
            if ((int(row[3])-cycle==1) or 
                    ((lc.atof(row[1])>cycle_length*1.1)
                    and(cycle_length>0))
            ):
#Последние два условия были введены поскольку последний цикл во всех
#Отличается по продолжительноости и диапазону нагрузок
#Что свидетельствует об ошибке прерывания логирования в софте
#И вызывает ошибку в последнем интеграле
                cycle = int(row[3])
                work = sympson_integration(x_buf, y_buf)
                energy.append(work)
                x_buf = list()
                y_buf = list()
                x_buf.append(lc.atof(row[6])/1000)
                y_buf.append(lc.atof(row[7]))
                
                if cycle_length<0:
                    cycle_length = length_buf
                elif lc.atof(row[1])>(cycle_length*1.1):
#Допустимая погрешность, поскольку могут быть отклонения от
#Скорости колебания
                    flag = 0
                    break
            elif int(row[3])-cycle==0:
                x_buf.append(lc.atof(row[6])/1000)
#Работа считается в Н*м, перемещения же даны в миллиметрах
                y_buf.append(lc.atof(row[7]))
                length_buf = lc.atof(row[1])
            else:
                raise ValueError('error in number of cycle')
        if flag == 1:
            work = sympson_integration(x_buf, y_buf)
            energy.append(work)

    output_file = ''

    frequency = round(1/cycle_length)
    try:
        output_file = sys.argv[2]
    except IndexError:
        output_file = "output.txt"
    with open(output_file, encoding='utf-8', mode='w') as f_out:
        f_out.write(''.join(str(frequency) + '\n'))
        f_out.write(''.join(str(x)+'\n' for x in energy))
