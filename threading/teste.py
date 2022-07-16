import math
from threading import Thread, Lock

def write_file(lista_numeros):
    for numero in lista_numeros:
        lock.acquire()
        with open('teste.txt', 'a') as file:
            file.write(str(numero)+'\n')
            lock.release()
    # for indice in range(start, end):
    #     if indice >= len(lista):
    #         break
    #     with open('teste.txt', 'a') as file:
    #         try:
    #             lock.acquire()
    #             print(indice)
    #             file.write(str(lista[indice])+'\n')
    #             lock.release()
    #         except:
    #             print('Não foi possível escrever no arquivo')


lock = Lock()

lista = [i for i in range(443)]

offset = math.floor(len(lista)/8) + len(lista) % 8

for i in range(0, len(lista), offset):
    print(i)
    print(i+offset)
    print(lista[i:i+offset])
    Thread(target=write_file, args=([lista[i:i+offset]])).start()

#
# for i in range(0, len(lista)-1, offset-1):
#     if offset >= len(lista) - 1:
#         offset = len(lista) - 1
#
#     Thread(target=write_file, args=(i, i + offset-1)).start()