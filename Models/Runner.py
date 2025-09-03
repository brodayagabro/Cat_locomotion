import numpy as np
import matplotlib.pyplot as plt
from Models.Limb import Limb

# структура данных для детектирования сетки и актиности мышц
class Detector:
    def __init__(self, lf, le):
        self.network = {
                "layer_2": [],
                "layer_1": [],
                "layer0": [],
                "layer1": [],
                "layer2": []
            }
        self.flexor = [lf]
        self.extenzor = [le]
        self.alpha_flexor = []
        self.alpha_extenzor = []
    def detect(self, limb, lens, angles):
        #save activity of curent iteration
        self.network["layer1"].append(limb.layer1)
        self.network["layer_1"].append(limb.layer_1)
        self.network["layer_2"].append(limb.layer_2)
        self.network["layer0"].append(limb.layer0)
        self.flexor.append(lens[0])
        self.extenzor.append(lens[1])
        self.alpha_flexor.append(angles[0])
        self.alpha_extenzor.append(angles[1])

# Класс для описания симуляции получает на вход время симуляции и объет для моделирования типа Limb
class Runner:
  # Конструктор класс параметры N
    def __init__(self, N, Limb):
        # моделируемая система
        self.limb = Limb
        
        # тут описаны названия слоев их потом можно использовать для обращения к полям детектор
        self.layers = ["layer_2", "layer_1", "layer0", "layer1", "layer2"]

        #детектирование активности сети
        self.detector = Detector(Limb.flexor, Limb.extenzor)
        
        # Определение интервала времени работы симуляции
        self.time = list(range(N))

      # Метод запуска симуляции
    def run_simulate(self, act):
        i = 1
        # сигнал с генератора паттерна
        self.limb.layer0 = [act(i), not act(i)]
        for i in self.time:
            #прохождение сигнала с предыдущей итерации по сети от пейсмейкеров к мышце
            self.limb.feedforward()
            #save layer 2 activity
            # Активность мотонейронного слоя после такого прохождения
            self.detector.network["layer2"].append(self.limb.layer2)

            # get sensoric activity from musculs and ruduction segment
            # Активность сенсорного слоя после сгибания мышцы
            self.limb.layer_2, lens, angles = self.limb.reduction(self.limb.layer2)
            #plotting alpha-neuron own handmade activity
            # сигнал с генератора паттерна
            self.limb.layer0 = [act(i), not act(i)]
            #plt.scatter(i, self.limb.layer0[0], color="red", marker="o")
            #plt.scatter(i, self.limb.layer0[1],color="red", marker="o")

            # Детектирование активности сети и мышц
            self.detector.detect(self.limb, lens, angles)
            
            #save previous activity to use in next interation
            self.limb.backprop()
            #display alpha-neuron activity after back propogation    
            #plt.scatter(i, self.limb.layer0[0], color="black", marker='+')
            #plt.scatter(i, self.limb.layer0[1],color="magenta", marker='+')
        return self.limb  
  
# Получение активности всех слоев сети в виде массиво активности отдельных нейронов

  # вывод активности слоя layer
    def display_layer(self, layer):
        if layer in self.layers:
            fig1, ax = plt.subplots(figsize = (10, 3))
            ax.set_title(layer, size="x-large")
            ax.set_xlabel("N")
            ax.set_ylabel("Spikes")
            detects = self.detector.network
            layer = np.array(detects[layer]).transpose()
            for neuron in layer:
                ax.plot(self.time, neuron, label=str(neuron[1]))
                ax.legend()
        else:
            print("Undefined layer")

    def display_limb(self):
        N = len(self.time)
        #musculs and angles
        fig2, (ax, ay) = plt.subplots(1, 2, figsize=(10, 3))
        ax.set_title("Musculs")
        ax.plot(self.time, self.detector.flexor[0:N], label="flex")
        ax.plot(self.time, self.detector.extenzor[0:N], label="ext")
        ax.set_xlabel("time, N")
        ax.set_ylabel("Length")
        suml = np.sqrt(
              np.square(self.detector.flexor[0:N]) +
              np.square(self.detector.extenzor[0:N]))
        ax.plot(self.time, suml, label="sum")
        ax.legend(loc=4)
        
        ay.set_title("Angles")
        ay.plot(self.time, np.arccos(self.detector.alpha_flexor[0:N]), label="flex")
        ay.plot(self.time, np.arccos(self.detector.alpha_extenzor[0:N]), label="ext")
        ay.set_xlabel("time, N")
        ay.set_ylabel("Angle")
        sumA = np.array(np.arccos(self.detector.alpha_flexor[0:N])) + np.arccos(
            self.detector.alpha_extenzor[0:N])
        ay.plot(self.time, sumA, label="sum")
        ay.legend(loc=4)

