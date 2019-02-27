#Andy Castillo 18040
#Abril Palencia 18
#1/3/19
#Simulador de procesos

import simpy
import random

class System:
    def __init__(self, env, instructionsRead):
        self.env = env
        self.ram = simpy.Container(env, init= 100, capacity= 100)
        self.cpu = simpy.Resource(env, capacity = 1)
        self.instructionsRead = instructionsRead


class Process:
    def __init__(self, env, name , memory, instructions, system):
        self.env = env
        self.name = name
        self.memory = memory
        self.instructions = instructions
        self.system = system
        self.action = env.process(self.ready(env,system))

    def ready(self,env,system):
        if system.ram.level >= self.memory:
            yield system.ram.get(self.memory)
            print("Memoria proceso",self.name,"es",self.memory)
            print("Queda",self.system.ram.level,"de RAM")
            print("El proceso",self.name,"tiene",self.instructions,"instrucciones")
            with system.cpu.request() as req:
                yield req
                self.instructions = self.instructions - system.instructionsRead
                print("Le quedan", self.instructions,"al proceso",self.name)
            
env = simpy.Environment()
sistema = System(env, 3)
#def processGenerator(env, system):
for i in range(10):
    name = i
    memory = random.randint(1,10)
    instructions = random.randint(1,10)
    process = Process(env,name,memory,instructions,sistema)
    

env.run()
