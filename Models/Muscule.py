import numpy as np
#from .Network import NeuralNetwork
# Класс описывает углы между горизонатольной проскостью и направлением сегмента конечности
class Angles():
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.aflex = 0
        self.aext = 0

    def calc(self, l):
        return (self.a**2 + self.b**2 - l**2) / (2 * self.a * self.b)

    def flexion(self, f, e):
        self.aflex = self.calc(f)
        self.aext = self.calc(e)
        return (self.aflex, self.aext)

# Описание динамики мышц сгибателей и разгибателей
class Muscule():
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.c1 = 2 * (a**2 + b**2)
        self.l_max = a + b
        lf = np.sqrt(a**2 + b**2)
        le = np.sqrt(self.c1 - lf**2)
        print(lf, le)
        self.flexor = lf
        self.extenzor = le
        self.Angles = Angles(a, b)

    #возвращем активности нейронов -2 слоя
    ## Функция описывает сокращение мышцы согласно Модели Хила
    def reduction(self, alpha):
        l = lambda x: np.sqrt(self.c1 - x**2)
        f_cur = self.flexor
        e_cur = self.extenzor
        angles = self.Angles.flexion(f_cur, e_cur)
        a_p = alpha[0]
        a_m = alpha[1]
        # Если сокращение не возможно, то мышца возбудает Ia аксон и 
        # сеть выбрасывает сигнал ингибирующий дальшнейшее движение в этом направлении
        if (l(f_cur - a_p) <= self.l_max) & (l(e_cur - a_m) <= self.l_max):
            f_cur -= a_p
            e_cur = l(f_cur)
            e_cur -= a_m
            f_cur = l(e_cur)
            ret = np.array([0, 0])
        else:
            f_cur = f_cur
            e_cur = e_cur
            ret = np.array([a_p, a_m])
            
        self.flexor = f_cur
        self.extenzor = e_cur
        return ret, (f_cur, e_cur), angles
