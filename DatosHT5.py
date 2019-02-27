#Andy Castillo 18040
#Abril Palencia 18
#1/3/19
#Simulador de procesos

import simpy
import random
random.seed(5)

class System:
    def __init__(self, env, instructionsRead):
        self.env = env
        self.ram = simpy.Container(env, init= 15, capacity= 15)
        self.cpu = simpy.Resource(env, capacity = 1)
        self.instructionsRead = instructionsRead


class Process:
    def __init__(self, env, name , memory, instructions, system):
        self.env = env
        self.name = name
        self.memory = memory
        self.instructions = instructions
        self.system = system
        self.cronometro = 0
        self.action = env.process(self.ready(env,system))

    def ready(self,env,system):
        yield self.system.ram.get(self.memory)
        print("ram",self.system.ram.level)
        print("Memoria proceso",self.name,"es",self.memory)
        print("El proceso",self.name,"tiene",self.instructions,"instrucciones\n")
        while self.instructions > 0:
            with system.cpu.request() as req:
                yield req
                self.instructions -= system.instructionsRead
                self.cronometro += 1
                print("Tiempo proceso",self.name,"es",self.cronometro)
                print("Le quedan", self.instructions,"instrucciones al proceso",self.name,"\n")
                
            if self.instructions <=0:
                print("Se termino de ejecutar el programa")
                yield system.ram.put(self.memory)
                print("memoria ram",self.system.ram.level,"\n")
            
env = simpy.Environment()
sistema = System(env, 3)
#def processGenerator(env, system):
for i in range(10):
    name = i
    memory = random.randint(1,10)
    instructions = random.randint(1,10)
    process = Process(env,name,memory,instructions,sistema)
    

env.run()
