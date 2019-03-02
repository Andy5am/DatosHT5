#Andy Castillo 18040
#Abril Palencia 18198
#01/03/2019
#Simulador de procesos

#importar librerias con las que se va a trabajar.
import simpy
import random
import statistics as stats

random.seed(5)

#listas para tiempos de inicio y fin
listaInicio = []
listaTiempos = []
#lista para el promedio
listaPromedio=[]


#clase System, el sistema operativo.
class System:
    def __init__(self, env, instructionsRead):
        self.env = env
        self.ram = simpy.Container(env, init= 100, capacity= 100)#cambio de capacidad de memoria RAM
        self.cpu = simpy.Resource(env, capacity = 2)#cambio de capacidada de procesar del CPU
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
            #se solicita usar el cpu
            with system.cpu.request() as req:
                yield req
                #se restan las instrucciones
                self.instructions -= system.instructionsRead
                if self.instructions>0:
                    print("Le quedan", self.instructions,"instrucciones al proceso",self.name,"\n")
                yield env.timeout(1)
                #se genera el numero random y se va a wait o ready
                waiting = random.randint(1,2)
                if waiting == 1:
                    print("El proceso",self.name,"esta en waiting durante 1 unidad de tiempo")
                    yield env.timeout(1)
                    print("El proceso",self.name,"esta en ready\n")
            # si ya no tiene instrucciones termina
            if self.instructions <=0:
                print("Se termino de ejecutar el proceso",self.name,"\n")
                self.cronometro= env.now
                yield system.ram.put(self.memory)
                listaTiempos.append(self.cronometro)

#Se creo el environment         
env = simpy.Environment()
#se crea el sistema operativo
sistema = System(env, 3)
#metodo para generar procesos
def processGenerator(env,num):
    for i in range(200):
        name = i
        memory = random.randint(1,10)
        instructions = random.randint(1,10)
        listaInicio.append(env.now)
        process = Process(env,name,memory,instructions,sistema)
        yield env.timeout(random.expovariate(1.0/5))

#Simulacion
env.process(processGenerator(env,200))
env.run()


tiempo = env.now
#for para tiempos
for a in range(len(listaInicio)):
    listaPromedio.append(listaTiempos[a]-listaInicio[a])
#se muestran tiempos
print("El tiempo total de la ejecucion es de",tiempo)
print("El promedio de tiempo de ejecucion de cada proceso es de",stats.mean(listaPromedio))
print("La desviacion estandar del tiempo de ejecucion de cada proceso es de",stats.pstdev(listaPromedio))
