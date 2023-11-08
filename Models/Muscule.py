import numpy as np
from .Network import NeuralNetwork


class Angle():

  def __init__(self, a, b):
    self.a, self.b = a, b
    self.aflex = []
    self.aext = []

  def calc(self, l):
    return (l**2 - self.a**2 - self.b**2) / (-2 * self.a * self.b)

  def flexion(self, f, e):
    self.aflex.append(self.calc(f))
    self.aext.append(self.calc(e))


class Muscule():

  def __init__(self, a, b):
    self.a, self.b = a, b
    self.c1 = 2 * (a**2 + b**2)
    self.l_max = a + b
    lf = np.sqrt(a**2 + b**2)
    le = np.sqrt(self.c1 - lf**2)
    print(lf, le)
    self.flexor = [lf]
    self.extenzor = [le]
    self.Angles = Angle(a, b)

  #возвращем активности нейронов -2 слоя
  def reduction(self, a_p, a_m):
    l = lambda x: np.sqrt(self.c1 - x**2)
    f_cur = self.flexor[-1]
    e_cur = self.extenzor[-1]
    self.Angles.flexion(f_cur, e_cur)
    if ((f_cur + a_p) <= self.l_max) & (e_cur + a_m <= self.l_max):
      f_cur += a_p
      e_cur = l(f_cur)
      e_cur += a_m
      f_cur = l(e_cur)
      ret = np.array([0, 0])
    else:
      f_cur = f_cur
      e_cur = e_cur
      # self.flexor.append(f_cur)
      #self.extenzor.append(e_cur)
      ret = np.array([a_p, a_m])
    self.flexor.append(f_cur)
    self.extenzor.append(e_cur)
    return ret
