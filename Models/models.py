import numpy as np
import matplotlib.pyplot as plt

class neuron():
    is_ingibitor, is_alpha, is_pacemaker, is_inter = False, False, False, False
    type = "\0"
    activate = np.zeros(10) # моделирует активность 0 - неактивен 1 - активен
    connections = np.zeros(10)
    def __init__(self, type):
        self.type = type
        types = ["ingibitor", "pacemaker", "alpha", "inter"]
        self.activate = np.array([])
        self.connections = np.array([])
        if type in types:
            self.type = type
        if type == "ingibitor":
            self.is_ingibitor = True
        elif type == "pacemaker":
            self.is_pacemaker = True
        elif type == "alpha":
            self.is_alpha = True
        elif type == "inter":
            self.is_inter = True
        else:
            print('unknown type')
            del(self)
            
        print(f'created {type} neuron')
    # деструктор
    def __del__(self):
        pass
        #print(f'{self.type} neuron deleted from network')
    
    def print(self):
        print(self.type)
    # однонаправленное соеднение
    # задаем нейроны, которые иннервируют данный
    def connect(self, neuron):
        if not neuron in self.connections:
            self.connections = np.append(self.connections, neuron)
            #neuron.connections = np.append(neuron.connections, self
            print(f"connected succesfully {neuron.type} -> {self.type}")
        else:
            print("Already connect")
            
    def disconnect(self, neuron):
        if neuron in self.connections:
            self.connections = np.delete(self.connections, neuron)
            print(f"disconnected succesfully {neuron.type} -> {self.type}")
        else:
            print("wasn't connected")
            
          
    def clear_cons(self):
        self.connections = np.zeros([])
        
    def clear_act(self):
        self.activate = np.array([])
    
    def compute_act(self, j):
        def fullsig(ingibitors, others):
            #print(ingibitors, others, iss)
            return others and not ingibitors    
            
        ingibitors = 0
        others = 0
        
        for n in self.connections:
            if n.is_ingibitor:
                ingibitors = ingibitors or n.activate[j]
            else:
                others = others or n.activate[j]
                
        l = fullsig(ingibitors, others)
        #str = f'ingibitors = {ingibitors}, others = {others}, iss = {iss}'
        self.activate = np.append(self.activate, l)   
        return l#, str
        #self.activate = np.append(self.activate, l)    


# activation functions
sigmoid = lambda t: 1/(1+np.exp(-t))
f = lambda t: (t >= 1).astype(float)

class NeuralNetwork:
    def __init__(self, layer0, layer1, layer2):
        self.layer0 = layer0
        self.layer1 = layer1
        self.layer2 = layer2
        self.layer_1 = [0, 0, 0, 0]
        self.layer_2 = [0, 0]
        self.W1 = np.array([[1, 0],
                            [0, 1],
                            [0, 1],
                            [1, 0]])
        
        self.W2 = np.array([[1, -100, 0, 0],
                            [0, 0, 1, -100],])

        self.W_1 = np.array([[-100, 0, 1, 0],
                             [0, 1, 0, -100]])

        self.W_2 = np.array([[1, 0],
                             [1, 0],
                             [0, 1],
                             [0, 1]])
        
        self.layer1 = f(np.dot(self.W1, self.layer0))
        self.layer2 = f(np.dot(self.W2, self.layer1))

    def feedforward(self):
        self.layer1 = f(np.dot(self.W1, self.layer0))
        self.layer2 = f(np.dot(self.W2, self.layer1))
        
    def backprop(self):
        self.layer_1 = f(np.dot(self.W_2, self.layer_2))
        self.layer0 = f(np.dot(self.W_1, self.layer_1)+self.layer0)


class Angle():
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.aflex = []
        self.aext = []
    def calc(self,l):
        return (l**2 - self.a**2 - self.b**2)/(-2*self.a*self.b)
        
    def flexion(self, f, e):
        self.aflex.append(self.calc(f))
        self.aext.append(self.calc(e))

class Muscule():    
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.c1 = 2*(a**2 + b**2)
        self.l_max = a + b
        lf = np.sqrt(a**2+b**2)
        le = np.sqrt(self.c1 - lf**2)
        print(lf, le)
        self.flexor = [lf]
        self.extenzor = [le]
        self.Angles = Angle(a, b)
        
    #возвращем активности нейронов -2 слоя    
    def reduction(self, a_p, a_m):
        l = lambda x: np.sqrt(self.c1-x**2)
        f_cur = self.flexor[-1]
        e_cur = self.extenzor[-1]
        self.Angles.flexion(f_cur, e_cur)
        if ((f_cur + a_p)<=self.l_max) & (e_cur+a_m<=self.l_max):
            f_cur += a_p
            e_cur = l(f_cur)
            e_cur += a_m
            f_cur = l(e_cur)
            ret = np.array([0,0])
        else:
            f_cur=f_cur
            e_cur=e_cur
           # self.flexor.append(f_cur)
            #self.extenzor.append(e_cur)
            ret = np.array([a_p, a_m])
        self.flexor.append(f_cur)
        self.extenzor.append(e_cur)
        return ret

class Limb(NeuralNetwork, Muscule, Angle):
    def __init__(self, a, b, layer0, layer1, layer2):
        Muscule.__init__(self, a, b)
        Angle.__init__(self, a, b)
        NeuralNetwork.__init__(self, layer0, layer1, layer2)

# Класс для описания симуляции получает на вход время симуляции и объет для моделирования типа Limb
class Runner:
    # Конструктор класс параметры N
    def __init__(self, N, system):
        # моделируемая система
        self.limb = system
        # тут описаны названия слоев их потом можно использовать для обращения к полям детектор
        self.layers = ["layer_2", "layer_1", "layer0", "layer1", "layer2"]
        
        #детектирование активности сети
        self.detector = {"layer_2" : [],
                        "layer_1" : [],
                        "layer0" : [],
                        "layer1" : [],
                        "layer2" : []
                        }
        # Определение интервала времени работы симуляции
        self.time = list(range(N))

    # Метод запуска симуляции
    def run_simulate(self):
        #
        act1 = lambda x: (x//6)%2#сюда надо веса и как либо обучать
        i = 1
        self.limb.layer0 = [act1(i),not act1(i)]
        for i in self.time: 
            self.limb.feedforward() 
            
            #save layer 2 activity
            self.detector["layer2"].append(self.limb.layer2)
        
            # get sensoric activity from musculs and ruduction segment
            self.limb.layer_2 = self.limb.reduction(self.limb.layer2[0], self.limb.layer2[1])

            #save activity of curent iteration
            self.detector["layer1"].append(self.limb.layer1)
            self.detector["layer_1"].append(self.limb.layer_1)
            self.detector["layer_2"].append(self.limb.layer_2)
            self.detector["layer0"].append(self.limb.layer0)
            
            #plotting alpha-neuron own handmade activity
            self.limb.layer0 = [act1(i), not act1(i)]
            plt.scatter(i, self.limb.layer0[0],color="red", marker="o")
            #plt.scatter(i, self.limb.layer0[1],color="red", marker="o")
            
            #save previous activity to use in next interation
            self.limb.backprop()
            plt.scatter(i, self.limb.layer0[0],color="black", marker='+')
            #plt.scatter(i, self.limb.layer0[1],color="magenta", marker='+')

    # Получение активности всех слоев сети в виде массиво активности отдельных нейронов 
    def get_detector(self):
            detector = {"layer_2" : [],
                        "layer_1" : [],
                        "layer0" : [],
                        "layer1" : [],
                        "layer2" : []
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
            plt.show()
            N = len(self.time)
            #musculs and angles
            fig, (ax, ay) = plt.subplots(1, 2, figsize=(15, 5))
            ax.set_title("musculs")
            ax.plot(self.time, self.limb.flexor[0:N], label = "flex")
            ax.plot(self.time, self.limb.extenzor[0:N], label = "ext")
            ax.set_xlabel("time, N")
            suml = np.sqrt(np.square(self.limb.flexor[0:N]) + np.square(self.limb.extenzor[0:N]))
            ax.plot(self.time, suml, label="sum" )
            ax.legend()
            #fig.savefig("мышечная активность")
            #plt.show()
            ay.set_title("angles")
            ay.plot(self.time, np.arccos(self.limb.Angles.aflex[0:N]), label = "flex")
            ay.plot(self.time, np.arccos(self.limb.Angles.aext[0:N]), label = "ext")
            ay.set_xlabel("time, N")
            sumA = np.array(np.arccos(self.limb.Angles.aflex[0:N]))+ np.arccos(self.limb.Angles.aext[0:N])
            ay.plot(self.time, sumA, label="sum")
            ay.legend()
        else:
            print("nn")
            #fig.savefig("Углы в суставах")
        
        