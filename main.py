# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import math
import numpy as np

import matplotlib.pyplot as plt

## @var Критерий точности алгоритма градиентного спуска
eps = 0.0000001
## @brief Коэффициент обучения (гиперпараметр)
rate = 0.01
## @brief Коэффициенты введённой пользователем функции
coefs = [1, 1, 1]

## @brief Переменная, несёт в себе логическое значение параметра FORMAT_COEFS
is_coefs_format = False
## @brief Переменная, несёт в себе логическое значение параметра IS_MINIMUM
is_minimum = True
## @brief Переменная, определяет, был ли использован повтор команды в консоли
is_repeat = False
## @brief Переменная, определяет, является ли введённое пользователем сообщение параметром
is_param = False
## @brief Переменная, несёт в себе значение параметра CRITERION
criterion = 1
## @brief Словарь, по которому происхоидит определение поиска максимума/минимума
param_min_dict = {True: -1, False: 1}


## Класс точки
class Point:
    # Конструктор класса точки
    #
    # @param: x - Значение x координаты точки
    # @param: y - Значение y координаты точки
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    ## Операнд вычитания точек
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - self.y)

    ## Модульное значение точки
    def __abs__(self):
        math.hypot(self.x, self.y)


## Функция для создания координатной плоскости
#
# @return: Координаты точек плоскости
def make_data():
    x = np.arange(-10, 10, 0.1)
    y = np.arange(-10, 10, 0.1)
    x_grid, y_grid = np.meshgrid(x, y)
    z_grid = (x_grid ** 2 / coefs[0] + y_grid ** 2 / coefs[1]) / coefs[2]
    return x_grid, y_grid, z_grid


## Функция для построения графиков
#
# @return: Координатная плоскость с построенным графиком
def show_function():
    x, y, z = make_data()
    fig = plt.figure(figsize=(15, 15))
    axes = fig.add_subplot(1, 1, 1, projection='3d')
    axes.plot_surface(x, y, z, rstride=5, cstride=5, alpha=0.7)
    return axes


## Функция парсинга вводимой пользователем функции
#
# @param: str_form - строка, введённая пользователем
# @param: coefs - список коэффициентов (изначально равен [1, 1, 1]
def get_function_coefs(str_form, coefs):
    var_dict = {'x': 0, 'y': 1, 'z': 2}

    # Функция анализа строки
    #
    # @param: подстрока, содержащая в себе одну из переменных: x, y или z
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
            return True
    return False


## Функция проверки строки
# @brief Функция проверяет введённую строку на соотвествие функции вида (x^2/a + y^2/b = cz)
#
# @param: str_form - введённая пользователем строка
# @return: логическое значение, прошла ли строка проверку
# @retval: True - проверка пройдена
# @retval: False - проверка не пройдена
def check_function(str_form):
    match = re.search(r'x\^2(/\d+)?\s*[+-]\s*y\^2(/\d+)?\s*=\s*-*\d*z', str_form)
    if not match:
        return False
    else:
        return True


## Функция частной производной по аргументу x в заданной точке
#
# @param: point - точка, в которой находится значение производной
# @return: dx - значение частной производной в заданной точке
def get_dx(point):
    delta_p = Point(point.x + eps, point.y)
    dx = (get_function_value(delta_p) - get_function_value(point)) / eps
    return dx


## Функция частной производной по аргументу y в заданной точке
#
# @param: point - точка, в которой находится значение производной
# @return: dy - значение частной производной в заданной точке
def get_dy(point):
    delta_p = Point(point.x, point.y + eps)
    dy = (get_function_value(delta_p) - get_function_value(point)) / eps
    return dy


## Функция, находит значение основной функции в заданной точке
#
# @param: point - точка, в которой находится значение функции
# @return: значение функции в заданной точке
def get_function_value(point):
    return (point.x ** 2 / coefs[0] + point.y ** 2 / coefs[1]) / coefs[2]


## Функция, находит значение градиента в заданной точке
#
# @param: point - точка, в которой находится значение градиента функции
# @return: значение градиента функции в заданной точке
def get_gradient(point):
    return get_dx(point) + get_dy(point)


## Функция, определяет, пройден ли первый критерий останова
# @brief Происходит определение прохождения алгоритмом градиентного спуска первого критерия останова:
# |f(cur_p) - f(prev_p)| <= eps
# @param: cur_p (current point) - текущая точка алгоритма
# @param: prev_p (previous point) - предыдущая точка алгоритма
# @retval: True - критерий не преодолен, алгоритм продолжается
# @retval: False - критерий преодолен, алгоритм останавливается
def get_first_criterion(cur_p, prev_p, eps):
    func_val_1 = get_function_value(cur_p)
    func_val_2 = get_function_value(prev_p)
    if abs(func_val_1 - func_val_2) >= eps:
        return True
    else:
        return False


## Функция, определяет, пройден ли второй критерий останова
# @brief Происходит определение прохождения алгоритмом градиентного спуска второго критерия останова:
# |cur_p - prev_p| <= eps
# @param: cur_p (current point) - текущая точка алгоритма
# @param: prev_p (previous point) - предыдущая точка алгоритма
# @retval: True - критерий не преодолен, алгоритм продолжается
# @retval: False - критерий преодолен, алгоритм останавливается
def get_sec_criterion(cur_p, prev_p, eps):
    x_sub = cur_p.x - prev_p.x
    y_sub = cur_p.y - prev_p.y
    if abs(x_sub) >= eps and abs(y_sub) >= eps:
        return True
    else:
        return False


## Функция градиентного спуска
#
# @brief При отсуствии у функции точки максимума/минимума функция возвращает большое значение координат
# найденной точки
# @param: point - точка, с которой начинается спуск
# @param: axes - координатная плоскость с построенным графиком функции
# @return: Вывод в консоль координат найденной точки экстремума, график функции, с отмеченной найденной точкой
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


## Функция формирования сообщения для пользователя
#
# @brief Формирует сообщение о вводе функции на основе значения параметра FORMAT_COEFS
# @param: is_coefs_format - логическая переменная, передаёт значение параметра FORMAT_COEFS
# @return: Выводит сообщение для пользователя и получает от него строку
def form_output_mess(is_coefs_format):
    format = 'x^2/2 - y^2/2 = 2z.'
    if is_coefs_format:
        format = '2 -2 2'
    func_str = input('Введите функцию. Формат: ' + format +
                     '\nЧтобы изменить формат ввода измените параметр "FORMAT_COEFS" на True.\n')
    return func_str


## Функция воспроизведения предыдущей команды
#
# @param: func_str - введённая пользователем строка
# @param: memory_func - последняя введённая пользователем функция
# @return: Если введенная функция эквивалентна предыдущей, строка становится равной ей
def remember_func(func_str, memory_func):
    if func_str == 'f':
        print('Введено: ', memory_func)
        return memory_func
    else:
        return func_str


## Функция воспроизведения предыдущей точки
#
# @param: func_str - введённая пользователем строка
# @param: memory_func - последняя введённая пользователем точка
# @return: Если введенная точка эквивалентна предыдущей, строка становится равной ей
def remember_point(point_str, memory_point):
    if point_str == 'p':
        print('Введено: ', memory_point)
        return memory_point
    else:
        return point_str


## Функция проверки формата строки
#
# @brief Осуществляется проверка введённой строки
# @param: is_coefs_format - логическая переменная, передаёт значение параметра FORMAT_COEFS
# @param: str - анализируемая строка
# @return: Логическое значение, была ли введенная строка верной по формату
def check_format(is_coefs_format, str):
    if not is_coefs_format:
        if get_function_coefs(str, coefs):
            return True
        else:
            return False
    else:
        match = re.search(r'\d\s+\d\s+\d', str)
        if not match:
            return False
        str = str.strip()
        coefs_arr = str.split()
        for i in range(3):
            coefs[i] = int(coefs_arr[i])
        return True


## @brief Консольная часть программы
#
# @brief Данная часть программы отвечает за консольное взаимодействие с пользователем - прием
# и анализ введённых пользователем команд и значений и их анализ
code = input('Отправьте команду. Чтобы увидеть полный список команд и параметров введите "show":\n')
repeat_code = ''
f = ''
p = ''
while code != 'end':
    if code == 'find_extra':
        func_str = form_output_mess(is_coefs_format)
        func_str = remember_func(func_str, f)
        if not check_format(is_coefs_format, func_str):
            print('Неверный формат ввода.')
            continue
        axes = show_function()
        lp_str = input('Введите координаты точки. Формат: x y. Координата z найдётся автоматически.\n')
        lp_str = remember_point(lp_str, p)
        lp_str = lp_str.strip()
        lp_arr = lp_str.split()
        previous_p = Point(float(lp_arr[0]), float(lp_arr[1]))
        get_minimum(previous_p, axes)
        plt.show()
        f = func_str
        p = lp_str
    elif code == 'graph':
        func_str = form_output_mess(is_coefs_format)
        func_str = remember_func(func_str, f)
        if not check_format(is_coefs_format, func_str):
            print('Неверный формат ввода.')
            continue
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
              '"p" - ввод ранее введённой точки.\n'
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
    coefs = [1, 1, 1]
