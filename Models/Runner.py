import numpy as np
import matplotlib.pyplot as plt
from Models.Limb import Limb


# Класс для описания симуляции получает на вход время симуляции и объет для моделирования типа Limb
class Runner:
  # Конструктор класс параметры N
  def __init__(self, N, system):
    # моделируемая система
    self.limb = system
    # тут описаны названия слоев их потом можно использовать для обращения к полям детектор
    self.layers = ["layer_2", "layer_1", "layer0", "layer1", "layer2"]

    #детектирование активности сети
    self.detector = {
        "layer_2": [],
        "layer_1": [],
        "layer0": [],
        "layer1": [],
        "layer2": []
    }
    # Определение интервала времени работы симуляции
    self.time = list(range(N))

  # Метод запуска симуляции
  def run_simulate(self):
    #
    act1 = lambda x: (x // 6) % 2  #сюда надо веса и как либо обучать
    i = 1
    self.limb.layer0 = [act1(i), not act1(i)]
    for i in self.time:
      self.limb.feedforward()

      #save layer 2 activity
      self.detector["layer2"].append(self.limb.layer2)

      # get sensoric activity from musculs and ruduction segment
      self.limb.layer_2 = self.limb.reduction(self.limb.layer2[0],
                                              self.limb.layer2[1])

      #save activity of curent iteration
      self.detector["layer1"].append(self.limb.layer1)
      self.detector["layer_1"].append(self.limb.layer_1)
      self.detector["layer_2"].append(self.limb.layer_2)
      self.detector["layer0"].append(self.limb.layer0)

      #plotting alpha-neuron own handmade activity
      self.limb.layer0 = [act1(i), not act1(i)]
      plt.scatter(i, self.limb.layer0[0], color="red", marker="o")
      #plt.scatter(i, self.limb.layer0[1],color="red", marker="o")

      #save previous activity to use in next interation
      self.limb.backprop()
      plt.scatter(i, self.limb.layer0[0], color="black", marker='+')
      #plt.scatter(i, self.limb.layer0[1],color="magenta", marker='+')

  # Получение активности всех слоев сети в виде массиво активности отдельных нейронов
  def get_detector(self):
    detector = {
        "layer_2": [],
        "layer_1": [],
        "layer0": [],
        "layer1": [],
        "layer2": []
    }
    for l in self.layers:
      detector[l] = np.array(self.detector[l]).transpose()
    return detector

  # вывод активности слоя layer
  def display(self, layer):
    if layer in self.layers:
      detects = self.get_detector()
      plt.plot(self.time, detects["layer0"][0])
      #plt.plot(self.time, detects["layer0"][1])
      #plt.show()
      N = len(self.time)
      #musculs and angles
      fig, (ax, ay) = plt.subplots(1, 2, figsize=(15, 5))
      ax.set_title("musculs")
      ax.plot(self.time, self.limb.flexor[0:N], label="flex")
      ax.plot(self.time, self.limb.extenzor[0:N], label="ext")
      ax.set_xlabel("time, N")
      suml = np.sqrt(
          np.square(self.limb.flexor[0:N]) +
          np.square(self.limb.extenzor[0:N]))
      ax.plot(self.time, suml, label="sum")
      ax.legend()
      #fig.savefig("мышечная активность")
      #plt.show()
      ay.set_title("angles")
      ay.plot(self.time, np.arccos(self.limb.Angles.aflex[0:N]), label="flex")
      ay.plot(self.time, np.arccos(self.limb.Angles.aext[0:N]), label="ext")
      ay.set_xlabel("time, N")
      sumA = np.array(np.arccos(self.limb.Angles.aflex[0:N])) + np.arccos(
          self.limb.Angles.aext[0:N])
      ay.plot(self.time, sumA, label="sum")
      ay.legend()
      plt.show()
    else:
      print("nn")
      #fig.savefig("Углы в суставах")
