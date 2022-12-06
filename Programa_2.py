from utilidades import *
from copy import deepcopy
from sympy import Abs, Matrix, pretty, sympify

##########################
# Clase Matriz para todo #
##########################


class Matriz:
    # Básico
    principal = list(list())
    vect_ind = list()
    dim = int()
    edd = None
    # Triangulación
    determinante = 1
    triangulada = None
    # Solución
    vect_soluc = None

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

        # Determinar si es EDD o no
        self.is_edd()

    # Determinar si la matriz es Estrictamente Dominante Diagonalmente (EDD)
    def is_edd(self):
        # Revisar cada renglón
        for i in range(self.dim):
            suma = 0
            # Sumar todos los elementos del renglón en valor absoluto, menos el pivote
            for j in range(self.dim):
                if j != i:
                    suma = Abs(self.principal[i][j])
            # Si al menos un pivote es menor que la suma, no es EDD
            if Abs(self.principal[i][i]) < suma:
                self.edd = False
                return
        # Si se recorrió por completo el for, entonces sí es EDD
        else:
            self.edd = True

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

                if corregir == 'm' or corregir == 'M':
                    ren = int_input(
                        "• Introduzca el número del renglón del valor que desea corregir: ", self.dim) - 1
                    col = int_input(
                        "• Introduzca el número de la columna del valor que desea corregir: ", self.dim) - 1

                    entrada = input(
                        f"--> Introduzca el nuevo valor del elemento [{ren+1}][{col+1}]: ")
                    self.principal[ren][col] = insertar_reales(entrada)
                elif corregir == 'v' or corregir == 'V':
                    pos = int_input(
                        "• Introduzca la posición del elemento que desea corregir: ", self.dim) - 1

                    entrada = input(
                        f"--> Introduzca el nuevo valor del elemento [{pos+1}]: ")
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

    # Solucionar el sistema asociado a la matriz con el método de Jacobi
    def solucionar(self):
        # Calcular el determinante si es que no se ha realizado aún
        if self.determinante is None:
            self.calc_det()

        clear_screen()
        if self.determinante == 0:
            print(
                "El determinante de la matriz es 0, por lo que el sistema asociado no tiene solución.")
        else:
            print("Solución al sistema asociado a la matriz\n")

            # Inicializar vectores de solución
            self.vect_soluc = [0 for _ in range(self.dim)]
            vect_soluc_prec = [0 for _ in range(self.dim)]

            # Inserción del vector inicial
            entrada = input(
                f"• Inserte los valores del vector de aproximación inicial separados por un espacio: ").strip().split(" ")
            vect_soluc_prec = insertar_reales(entrada, self.dim)
            # Inserción de tolerancia y máximo de iteraciones
            max_it, toler = maxit_toler_checks()

            # Encabezado de la tabla
            clear_screen()
            encabezado = ["it", *["x_{:<2}".format(i+1) for i in range(self.dim)], "norma esp."]
            encabezado_print = "| {:^3} |"
            for i in range(self.dim+1):
                encabezado_print += " {:^14} |"
            # Divisor para el encabezado
            div_print = "| {:-^3} |"
            for i in range(self.dim+1):
                div_print += " {:-^14} |"
            div = ["" for i in range(self.dim+2)]

            # El arreglo que se utilizará para imprimir los cálculos de cada iteración
            fila = "| {:^3} |"
            for i in range(self.dim):
                fila += " {:< 14.6g} |"
            # Fila 0 que no tiene error absoluto
            fila_0 = fila + " {:<14} |"
            # Las demás filas sí tienen error absoluto
            fila += " {:< 14.6g} |"

            print("Tabla correspondiente a los cálculos:\n")
            print(encabezado_print.format(*encabezado))
            print(div_print.format(*div))
            print(fila_0.format(*[0, *[float(elem)
                  for elem in vect_soluc_prec], " N/A"]))

            # Jacobi hasta llegar a la iteración máxima
            for it in range(max_it):
                for i in range(self.dim):
                    # Inicializar la suma en b_i
                    suma = self.vect_ind[i]
                    # A la suma se le resta a_ij*x_i^{k}
                    for j in range(self.dim):
                        if j != i:
                            suma -= self.principal[i][j] * vect_soluc_prec[j]
                    # El elemento del vector solución es la suma entre a_ii
                    self.vect_soluc[i] = suma/self.principal[i][i]

                # Cálculo de error (norma espectral)
                vect_difer_abs = [
                    Abs(self.vect_soluc[i] - vect_soluc_prec[i]) for i in range(self.dim)]
                norma_espec = max(vect_difer_abs)

                # Crear otro arreglo igual al de la solución, pero con float
                # Agregarle it+1 al inicio, la norma espectral al final
                vect_impr = [it+1, *[float(elem) for elem in self.vect_soluc], float(norma_espec)]

                # Imprimir solución actual y norma espectral
                print(fila.format(*vect_impr))

                # Si la norma espectral es menor a la tolerancia, terminamos
                if norma_espec <= toler:
                    break
                else:
                    # Guardar el vector solución actual como el precedente, para continuar
                    vect_soluc_prec = deepcopy(self.vect_soluc)

            # Impresión de resultados
            vect_soluc_float = [float(elem) for elem in self.vect_soluc]
            # Si se convergió satisfactoriamente bajo la tolerancia
            if norma_espec <= toler:
                print(
                    f"\nSe convergió satisfactoriamente a la siguiente solución con una tolerancia menor o igual a {float(toler)}:\n")
                for i in range(len(vect_soluc_float)):
                    print(f"• x_{i+1} = {vect_soluc_float[i]}")
                print(
                    f"\nSe necesitó de {it+1} iteraciones y este cálculo tiene un error absoluto de {float(norma_espec)}.")
            # Si no se convergió
            else:
                print(
                    f"\nSe alcanzaron las {it+1} iteraciones máximas. No se pudo converger a una solución con una tolerancia menor o igual a {float(toler)}.")
                print("\nEl último cálculo obtenido fue:\n")
                for i in range(len(vect_soluc_float)):
                    print(f"• x_{i+1} = {vect_soluc_float[i]}")
                print(
                    f"\nEste cálculo tiene un error absoluto de {float(norma_espec)}.")

                # Ofrecer alternativas según si es EDD o no
                if self.edd:
                    print(
                        "\nLa matriz es EDD, por lo que se asegura la convergencia dado un número de iteraciones razonable para la tolerancia.")

                    resp = bool_option(
                        "--> ¿Desea volver a intentar solucionar el sistema, esta vez con más iteraciones u otra tolerancia? (S/n) ", 'S', 'N')
                    if resp == 'S' or resp == 's':
                        self.solucionar()
                else:
                    print(
                        "\nLa matriz no es EDD, por lo que la convergencia no está garantizada.")

                    resp = bool_option(
                        "--> Puede intentar con (O)tro vector inicial, más iteraciones u otra tolerancia, o (M)odificar la matriz para que sea EDD: (O/M) ", 'O', 'M')
                    if resp == 'O' or resp == 'O':
                        self.solucionar()
                    else:
                        self.corregir()
                        self.det_soluc()

    # Método que combina el cálculo del determinante y el de la solución del sistema
    def det_soluc(self):
        clear_screen()
        self.calc_det()
        print("La matriz triangular asociada es:")
        self.print_triang()
        print(
            f"• Multiplicando los valores de la diagonal, se obtuvo que el determinante de la matriz es {(self.determinante).round(20)}")

        if self.determinante == 0:
            print(
                "--> Como el determinante es 0, el sistema asociado no tiene solución.")
        else:
            print(
                "--> Como el determinante es distinto de 0, el sistema asociado tiene solución.")
            if self.edd:
                print(
                    "--> Además, la matriz asociada es EDD, así que se garantiza la convergencia a la solución.")
            else:
                print(
                    "--> No obstante, la matriz no es EDD, así que no se garantiza la convergencia a la solución.")
                resp = bool_option(
                    "--> ¿Deseas modificar la matriz para que sea EDD? (S/n) ", 'S', 'N')
                if resp == 'S' or resp == 's':
                    self.corregir()

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
