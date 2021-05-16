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


code = input('Отправьте команду. Чтобы увидеть полный список команд и параметров введите "show":\n')
repeat_code = ''
f = ''
p = ''
while code != 'end':
    if code == 'find_extra':
        func_str = input('Введите функцию. Формат: x^2/2 - y^2/2 = 2z. '
                         'Чтобы изменить формат ввода измените параметр "FORMAT_COEFS" на True.\n')

        if func_str == 'f':
            func_str = f
            print('Введено: ', f)

        get_function_coefs(func_str, coefs)
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
              '"f" - ввод ранее введённой функции\n'
              '"t" - ввод ранее введённой точки\n'
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
