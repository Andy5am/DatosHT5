#Andy Castillo 18040
#Abril Palencia 18198
#01/03/2019
#Simulador de procesos

#importar librerias con las que se va a trabajar.
import simpy
import random
import statistics as stats

random.seed(5)

listaTiempos = []

#clase System, el sistema operativo.
class System:
    def __init__(self, env, instructionsRead):
        self.env = env
        self.ram = simpy.Container(env, init= 100, capacity= 100)
        self.cpu = simpy.Resource(env, capacity = 1)
        self.instructionsRead = instructionsRead

#clse Process, todos los procesos que va a ejecutar el sistema operativo
#cada proceso tiene una cantidada aleatoria de memoria, id y una cantidad
#aleatoria de instrucciones.
class Process:
    #inicializacion de cada proceso.
    def __init__(self, env, name , memory, instructions, system):
        self.env = env
        self.name = name
        self.memory = memory
        self.instructions = instructions
        self.system = system
        self.cronometro = 0
        self.action = env.process(self.run(env,system))
    #método el objeto proceso creado y le muestra al usuario el nombre, antidad
    #de momoria y cantidada de instrucciones.
    def run(self,env,system):
        yield self.system.ram.get(self.memory)
        print("El proceso",self.name,"tiene",self.instructions,"instrucciones")
        print("Memoria asignada al proceso",self.name,"\n")
        #empieza simulacion del sistema operativo.
        while self.instructions > 0:
            with system.cpu.request() as req:
                yield req
                self.instructions -= system.instructionsRead
                self.cronometro += 1
                if self.instructions>0:
                    print("Le quedan", self.instructions,"instrucciones al proceso",self.name,"\n")
                yield env.timeout(1)
                
                waiting = random.randint(1,2)
                if waiting == 1:
                    print("El proceso",self.name,"esta en waiting durante 1 unidad de tiempo")
                    yield env.timeout(1)
                    print("El proceso",self.name,"esta en ready\n")
                
            if self.instructions <=0:
                print("Se termino de ejecutar el proceso",self.name,"\n")
                yield system.ram.put(self.memory)
                listaTiempos.append(self.cronometro)
            
env = simpy.Environment()
sistema = System(env, 3)

#crea los procesos para la simulacion.
for i in range(10):
    name = i
    memory = random.randint(1,10)
    instructions = random.randint(1,10)
    process = Process(env,name,memory,instructions,sistema)


env.run()
tiempo = env.now
#mostrar cakculos y estadisticas de la simulacion.
print("El tiempo total de la ejecucion es de",tiempo)
print("El promedio de tiempo de ejecucion de cada proceso es de",stats.mean(listaTiempos))
print("La desviacion estandar del tiempo de ejecucion de cada proceso es de",stats.pstdev(listaTiempos))

