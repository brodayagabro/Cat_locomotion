import numpy as np


class neuron():
  is_ingibitor, is_alpha, is_pacemaker, is_inter = False, False, False, False
  type = "\0"
  activate = np.zeros(10)  # моделирует активность 0 - неактивен 1 - активен
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
      del (self)

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
    return l  #, str
    #self.activate = np.append(self.activate, l)
