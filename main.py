import re
import math

EPS = 0.00001
RATE = 0.1


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
        coefs = [1, 1, 1]
        for i in range(3):
            match = re.search(r'[+-]?\s*\d*[xyz](\^2/\d+)?', str_form)
            find = match.group(0)
            Analyse(find)
            str_form = str_form.replace(find, '')
            str_form.strip()
        return coefs


def CheckFunction(str_form):
    match = re.search(r'x\^2(/\d+)?\s*[+-]\s*y\^2(/\d+)?\s*=\s*-*\d*z', str_form)
    if not match:
        print('Функция введена неверно')
        return False
    else:
        return True


def GetDx(coefs, point):
    return 2 * point.x / (coefs[0] * coefs[2])


def GetDy(coefs, point):
    return 2 * point.y / (coefs[1] * coefs[2])


def GetFunctionValue(coefs, point):
    return (point.x ** 2 / coefs[0] ** 2 + point.y ** 2 / coefs[1] ** 2)/coefs[2]


def Go(point, coefs):
    previos_p = point
    current_p = Point(0, 0)
    x_bord = 99999
    y_bord = 99999
    while (x_bord >= EPS) and (y_bord >= EPS):
        current_p.x = previos_p.x - RATE * GetDx(coefs, previos_p)
        current_p.y = previos_p.y - RATE * GetDy(coefs, previos_p)
        x_bord = abs(current_p.x - previos_p.x)
        y_bord = abs(current_p.y - previos_p.y)
        previos_p = current_p
    z = GetFunctionValue(coefs, current_p)
    print('Minimum: (', format(current_p.x, '.6f'), ';', format(current_p.y, '.6f'), ';', format(z, '.6f'), ')')


func_str = input('Enter function\n')
lp_str = input('Input coordinates of point. Format: x y z\n')
lp_str = lp_str.strip()
lp_arr = lp_str.split()
previos_p = Point(float(lp_arr[0]), float(lp_arr[1]))
coefs = GetFunctionCoefs(func_str)
print(coefs)
# Go(previos_p, coefs)
