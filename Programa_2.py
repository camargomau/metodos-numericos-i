from utilidades import *
from copy import deepcopy
from sympy import Matrix, pretty, sympify

##########################
# Clase Matriz para todo #
##########################

class Matriz:
    principal = list(list())
    vect_ind = list()
    dim = int()
    determinante = 1
    triangulada = None

    # Constructor
    def __init__(self):
        # Obtención de dimensión e inicialización
        self.dim = int_input("• Inserta el tamaño de la matriz nxn: ", None)
        self.principal = [[0 for _ in range(self.dim)]
                          for _ in range(self.dim)]
        self.vect_ind = [0 for _ in range(self.dim)]

        # Inserción de los valores de la matriz
        print("\n• Inserción de los valores de la matriz. Inserte los valores de los renglones separados por un espacio (pueden ser fracciones):")
        for i in range(self.dim):
            entrada = input(
                f"--> Renglón {i}: ").strip().split(" ")
            self.principal[i] = insertar_reales(entrada, self.dim)

        # Inserción del vector independiente
        print("\n• Inserción de los valores del vector independiente")
        entrada = input(
            f"--> Inserte los valores separados por un espacio: ").strip().split(" ")
        self.vect_ind = insertar_reales(entrada, self.dim)

    # Impresora
    def __str__(self):
        return "\n" + pretty(Matrix(self.principal)) + "\n"

    # Impresora del vector independiente
    def print_vector(self):
        print("\n" + pretty(Matrix(self.vect_ind)) + "\n")

    # Corregir elementos de la matriz
    def corregir(self):
        while (True):
            clear_screen()
            print("La matriz insertada es:\n" + f"{self}")
            print("El vector independiente es:")
            self.print_vector()

            resp = bool_option("¿Desea corregir algún valor? (S/n) ", 'S', 'N')
            if resp == 's' or resp == 'S':
                corregir = bool_option(
                    "¿Desea corregir la matriz o el vector? (M/V) ", 'M', 'V')

                print("\n(considere que los índices inician en 0)")

                if corregir == 'm' or corregir == 'M':
                    ren = int_input(
                        "• Introduzca el número del renglón del valor que desea corregir: ", self.dim)
                    col = int_input(
                        "• Introduzca el número de la columna del valor que desea corregir: ", self.dim)

                    entrada = input(
                        f"--> Introduzca el nuevo valor del elemento [{ren}][{col}]: ")
                    self.principal[ren][col] = insertar_reales(entrada)
                elif corregir == 'v' or corregir == 'V':
                    pos = int_input(
                        "• Introduzca la posición del elemento que desea corregir: ", self.dim)

                    entrada = input(
                        f"--> Introduzca el nuevo valor del elemento [{pos}]: ")
                    self.vect_ind[pos] = insertar_reales(entrada)
            else:
                break

    # Triangular por Gauss
    def triangular(self):
        self.triangulada = deepcopy(self.principal)

        # Primer ciclo para cambiar de pivote (todo pivote es a_ii)
        # Toma valores en [0, dim-2] porque solo trabajamos con dim-1 pivotes (de los dim totales)
        for piv in range(self.dim-1):
            # Segundo ciclo para el renglón modificado; [piv+1, dim-1]
            # Modificamos los renglones a partir del siguiente del pivote hasta el último
            for renMod in range(piv+1, self.dim):
                # Intercambiar renglones cuando el pivote sea 0, para evitar división entre 0
                # Una mejor versión que realiza pivoteo es:
                # > if abs(self.triangulada[renMod][piv]) > abs(self.triangulada[piv][piv]):
                # No obstante, no la utilicé para no intercambiar renglones a menos que sea absolutamente necesario
                # Espero que sympy sea suficiente para compensar contra el error de redondeo
                if self.triangulada[piv][piv] == 0:
                    self.triangulada[piv], self.triangulada[renMod] = self.triangulada[renMod], self.triangulada[piv]
                    self.determinante = -self.determinante

                # Si el elemento que está debajo del pivote ya es 0, no hace falta procesar su renglón
                if self.triangulada[renMod][piv] == 0:
                    continue

                # El factor se define de forma que el elemento que está debajo del pivote se vuelva 0
                factor = -(self.triangulada[renMod]
                        [piv]/self.triangulada[piv][piv])

                # Tercer ciclo para ir iterando por las columnas de la matriz
                # Esto nos permite iterar por cada elemento del renMod
                for columna in range(piv, self.dim):
                    # A cada elemento del renMod, se le suma el elemento correspondiente
                    # del renglón del pivote multiplicado por el factor
                    self.triangulada[renMod][columna] += factor * \
                        self.triangulada[piv][columna]

    # Impresora de triangulada
    def print_triang(self):
        print("\n" + pretty(Matrix(self.triangulada)) + "\n")

    # Calcular determinante
    def calc_det(self):
        # Triangular la matriz si es que no se ha realizado aún
        if self.triangulada is None:
            self.triangular()

        for i in range(self.dim):
            self.determinante *= self.triangulada[i][i]

    # Solucionar el sistema asociado a la matriz
    def solucionar(self):
        # Calcular el determinante si es que no se ha realizado aún
        if self.determinante is None:
            self.calc_det()

        clear_screen()
        if self.determinante == 0:
            print(
                "El determinante de la matriz es 0, por lo que el sistema asociado no tiene solución.")
        else:
            print("--- Aquí se realizará el procedimiento de solución del sistema ---")
            print(
                "--- Esta parte del programa se implementará posteriormente para la entrega del Programa 3 ---")

    # Método que combina el cálculo del determinante y el de la solución del sistema
    # Está aquí para cumplir con el procedimiento requerido del programa 2
    def det_soluc(self):
        clear_screen()
        self.calc_det()
        print("La matriz triangular asociada es:")
        self.print_triang()
        print(
            f"• Multiplicando los valores de la diagonal, se obtuvo que el determinante de la matriz es {(self.determinante).round(20)}")

        if self.determinante == 0:
            print(
                "--> Como el determinante es 0, el sistema asociado no tiene solución")
        else:
            print(
                "--> Como el determinante es distinto de 0, el sistema asociado tiene solución.")

            resp = bool_option(
                "\n¿Desea solucionar el sistema asociado? (S/n) ", 'S', 'N')
            if resp == 'S' or resp == 's':
                self.solucionar()

#############################
# Función para dirigir todo #
#############################

def matrices():
    while True:
        clear_screen()
        print("Determinante de una matriz y solución del sistema asociado\n")

        la_matriz = Matriz()
        la_matriz.corregir()
        la_matriz.det_soluc()

        resp = bool_option(
            "\n¿Desea obtener el determinante o solucionar el sistema de otra matriz? (S/n) ", 'S', 'N')

        if resp != 'S' and resp != 's':
            break

#############
# Principal #
#############

if __name__ == "__main__":
    portada("Programa 2", "Matrices y Solución de Ecuaciones Lineales")
    matrices()
