
import numpy as np #numpy es una de las librerias más famosas de Python. Tiene muchas funcionalidad numericas.
from random import random #Librería para generar
from random import randint
from random import seed
from random import sample
import math

abecedario = []
numeros_primos = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
combined = np.append(abecedario, numeros_primos)
np.random.shuffle(combined)


def crearSemilla():
     # ----------------creación de semilla pseuda-aleatoria---------#
    seed = []
    for i in range(500):
        seed.append(randint(0, 9))

    subset = sample(seed, 6)
    return subset

def listToString(s):
    """Funcion que permite pasar de una variable tipo lista a string"""
    str1 = ""
    for ele in s:
        str1 += ele
    return str1

def crearKey():
    subset = crearSemilla()
    key = []
    for i in range(len(subset)):
        key.append(combined[subset[i]])

    return listToString(key)