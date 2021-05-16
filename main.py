#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math
import numpy as np

import matplotlib.pyplot as plt

eps = 0.0000001
rate = 0.01
coefs = [1, 1, 1]

is_coefs_format = False
is_minimum = True
is_repeat = False
is_param = False
criterion = 1

param_min_dict = {True: -1, False: 1}


class Point:

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - self.y)

    def __abs__(self):
        math.hypot(self.x, self.y)


def make_data():
    x = np.arange(-10, 10, 0.1)
    y = np.arange(-10, 10, 0.1)
    x_grid, y_grid = np.meshgrid(x, y)
    z_grid = (x_grid ** 2 / coefs[0] + y_grid ** 2 / coefs[1]) / coefs[2]
    return x_grid, y_grid, z_grid


def show_function():
    x, y, z = make_data()
    fig = plt.figure(figsize=(15, 15))
    axes = fig.add_subplot(1, 1, 1, projection='3d')
    axes.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.7)
    return axes


def get_function_coefs(str_form, coefs):
    var_dict = {'x': 0, 'y': 1, 'z': 2}

    def analyse(str: str):
        letter = re.search(r'[xyz]', str)
        num = var_dict.get(letter.group(0))
        start = 0
        if str.__contains__('-'):
            coefs[num] = coefs[num] * (-1)
        if letter.group(0) == 'x' or letter.group(0) == 'y':
            start = str.find(letter.group(0))
            str = str[start:len(str)]
            str = str.lstrip()
            start = str.find('/')
            if start != -1:
                str = str[start + 1:len(str)]
                coefs[num] = int(str) * coefs[num]
        else:
            funded_str = re.search(r'\d+', str)
            if funded_str is not None:
                str = funded_str.group(0)
                coefs[num] = int(str) * coefs[num]

    if check_function(str_form):
        for i in range(3):
            match = re.search(r'[+-]?\s*\d*[xyz](\^2/\d+)?', str_form)
            find = match.group(0)
            analyse(find)
            str_form = str_form.replace(find, '')
            str_form.strip()


def check_function(str_form):
    match = re.search(r'x\^2(/\d+)?\s*[+-]\s*y\^2(/\d+)?\s*=\s*-*\d*z', str_form)
    if not match:
        print('Функция введена неверно')
        return False
    else:
        return True


def get_dx(point):
    # return 2 * point.x / (coefs[0] * coefs[2])
    delta_p = Point(point.x + eps, point.y)
    test = (get_function_value(delta_p) - get_function_value(point)) / eps
    return test


def get_dy(point):
    # return 2*point.y / (coefs[1] * coefs[2])
    delta_p = Point(point.x, point.y + eps)
    test = (get_function_value(delta_p) - get_function_value(point)) / eps
    return test


def get_function_value(point):
    return (point.x ** 2 / coefs[0] + point.y ** 2 / coefs[1]) / coefs[2]


def get_gradient(point):
    return get_dx(point) + get_dy(point)


def get_first_criterion(cur_p, prev_p, eps):
    func_val_1 = get_function_value(cur_p)
    func_val_2 = get_function_value(prev_p)
    if abs(func_val_1 - func_val_2) >= eps:
        return True
    else:
        return False


def get_sec_criterion(cur_p, prev_p, eps):
    x_sub = cur_p.x - prev_p.x
    y_sub = cur_p.y - prev_p.y
    if abs(x_sub) >= eps and abs(y_sub) >= eps:
        return True
    else:
        return False


def get_minimum(point, axes):
    current_p = point
    previous_p = Point(0, 0)
    main_criterion = get_first_criterion
    if criterion == 2:
        main_criterion = get_sec_criterion
    while main_criterion(current_p, previous_p, eps):
        previous_p.x = current_p.x
        previous_p.y = current_p.y
        current_p.x = previous_p.x + param_min_dict.get(is_minimum) * rate * abs(get_dx(previous_p))
        current_p.y = previous_p.y + param_min_dict.get(is_minimum) * rate * abs(get_dy(previous_p))
    z = get_function_value(current_p)
    axes.scatter(current_p.x, current_p.y, get_function_value(current_p), color='red')
    find = 'Минимум'
    if not is_minimum:
        find = 'Максимум'
    print(f'{find}: ({current_p.x:.6f}; {current_p.y:.6f}; {z:.6f}).')


code = input('Отправьте команду. Чтобы увидеть полный список команд и параметров введите "show":\n')
repeat_code = ''
f = ''
p = ''
while code != 'end':
    if code == 'find_extra':
        format = 'x^2/2 - y^2/2 = 2z.'
        if is_coefs_format:
            format = '2 -2 2'
        func_str = input('Введите функцию. Формат: ' + format +
                         '\nЧтобы изменить формат ввода измените параметр "FORMAT_COEFS" на True.\n')

        if func_str == 'f':
            func_str = f
            print('Введено: ', f)

        if not is_coefs_format:
            get_function_coefs(func_str, coefs)
        else:
            print("Введите коэффициенты для уравнения параболоида:")
            func_str = func_str.strip()
            coefs_arr = func_str.split()
            for i in range(3):
                coefs[i] = int(coefs_arr[i])
        axes = show_function()
        lp_str = input('Введите координаты точки. Формат: x y. Координата z найдётся автоматически.\n')

        if lp_str == 't':
            lp_str = t
            print('Введено: ', t)

        lp_str = lp_str.strip()
        lp_arr = lp_str.split()
        previous_p = Point(float(lp_arr[0]), float(lp_arr[1]))
        get_minimum(previous_p, axes)
        plt.show()
        f = func_str
        t = lp_str
        coefs = [1, 1, 1]
    elif code == 'graph':
        func_str = input('Введите функцию:\n')

        if func_str == 'f':
            func_str = f
            print('Введено: ', f)

        get_function_coefs(func_str, coefs)
        show_function()
        plt.show()
        f = func_str
    elif code == 'show':
        print('Команды:\n'
              '"find_extra" - найти минимум функции.\n'
              '"graph" - отобразить график функции.\n'
              '"end" - закрыть приложение.\n'
              '"r" - повтор прошлой команды.\n'
              '"f" - ввод ранее введённой функции.\n'
              '"t" - ввод ранее введённой точки.\n'
              'Параметры:\n'
              '"IS_MINIMUM" - определяет, ищется максимум или минимум функции. Формат ввода: IS_MINIMUM = True.'
              'По умолчанимю True.\n'
              '"FORMAT_COEFS" - определяет формат ввода - функция вводится целиком или только коэфициенты. '
              'Формат ввода: FORMAT_COEFS = True. По умолчанию True.\n'
              '"HYPER" - задаёт коэффициент обучения. По умолчанию равен 0.01.\n'
              '"EPS" - задаёт параметр останова алгоритма. По умолчанию равен 0.0000001.\n'
              '"CRITERION" - задаёт критерий останова. По умолчанию равен 1.\n')
    elif code == "r":
        code = repeat_code
        is_repeat = True
    elif code.__contains__('IS_MINIMUM'):
        if code.__contains__('True'):
            is_minimum = True
            print('Поиск минимума.')
        else:
            is_minimum = False
            print('Поиск максимума.')
    elif code.__contains__('FORMAT_COEFS'):
        is_coefs_format = True
        print('Формат ввода функции изменён.')
        is_param = True
    elif code.__contains__('HYPER'):
        rate = float(code.split('=')[1])
        print('Значение коэффициента обучения изменено.')
        is_param = True
    elif code.__contains__('EPS'):
        eps = float(code.split('=')[1])
        print('Значение критерия останова изменено.')
        is_param = True
    elif code.__contains__('CRITERION'):
        criterion = int(code.split('=')[1])
        print('Критерий останова изменен. Текущий критерий: ')
        if criterion == 1:
            print('|f(x1,y1) - f(x0,y0)| < EPS')
        else:
            print('|x1 - x0| < EPS AND |y1 - y0| < EPS')
        is_param = True
    else:
        print('Неизвестная команда')
        is_param = True
    if not is_param:
        repeat_code = code
    if not is_repeat:
        code = input('Отправьте команду:\n')
    is_repeat = False
    is_param = False
