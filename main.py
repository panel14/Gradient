import re
import math

eps = 0.00001
rate = 0.1
coefs = [1, 1, 1]

is_minimum = True
is_repeat = False
is_param = False
criterion = 1

param_dict = {True: -1, False: 1}


class Point:

    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - self.y)

    def __abs__(self):
        math.hypot(self.x, self.y)


def GetFunctionCoefs(str_form):
    var_dict = {'x': 0, 'y': 1, 'z': 2}

    def Analyse(str: str):
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
            find = re.search(r'\d+', str)
            if find != None:
                str = find.group(0)
                coefs[num] = int(str) * coefs[num]

    if CheckFunction(str_form):
        for i in range(3):
            match = re.search(r'[+-]?\s*\d*[xyz](\^2/\d+)?', str_form)
            find = match.group(0)
            Analyse(find)
            str_form = str_form.replace(find, '')
            str_form.strip()


def CheckFunction(str_form):
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


func_str = input('Enter function\n')
lp_str = input('Input coordinates of point. Format: x y z\n')
lp_str = lp_str.strip()
lp_arr = lp_str.split()
previos_p = Point(float(lp_arr[0]), float(lp_arr[1]))
