from utilidades import *
from sympy import Abs, Matrix, pretty
from copy import deepcopy


class EigenMatriz:
    dim = int()
    matriz = list(list())
    determinante = None

    sp_matriz = None
    sp_matriz_inv = None

    eigenvalor_max = None
    eigenvalor_min = None

    def __init__(self):
        # Obtención de dimensión e inicialización
        self.dim = int_input("• Inserta el tamaño de la matriz nxn: ", None)
        self.matriz = [[0 for _ in range(self.dim)]
                       for _ in range(self.dim)]

        # Inserción de los valores de la matriz
        print("\n• Inserción de los valores de la matriz. Inserte los valores de los renglones separados por un espacio (pueden ser fracciones):")
        for i in range(self.dim):
            entrada = input(
                f"--> Renglón {i+1}: ").strip().split(" ")
            self.matriz[i] = insertar_reales(entrada, self.dim)

        self.sp_matriz = Matrix(self.matriz)

    def __str__(self):
        return "\n" + pretty(Matrix(self.matriz)) + "\n"

    def corregir(self):
        while (True):
            clear_screen()
            print("La matriz insertada es:\n" + f"{self}")

            resp = bool_option("¿Desea corregir algún valor? (S/n) ", 'S', 'N')
            if resp == 's' or resp == 'S':
                ren = int_input(
                    "• Introduzca el número del renglón del valor que desea corregir: ", self.dim)-1
                col = int_input(
                    "• Introduzca el número de la columna del valor que desea corregir: ", self.dim)-1

                entrada = input(
                    f"--> Introduzca el nuevo valor del elemento [{ren+1}][{col+1}]: ")
                self.matriz[ren][col] = insertar_reales(entrada)

                self.sp_matriz = Matrix(self.matriz)
            else:
                break

    def invertir(self):
        if self.sp_matriz.det() != 0:
            self.sp_matriz_inv = self.sp_matriz**-1

    # Calcular un eigenvalor por el método de potencias
    def eigenvalores(self):
        mayor_menor = bool_option(
            "¿Desea obtener el valor propio de ma(Y)or o de me(N)or magnitud? (Y/N) ", 'Y', 'N')
        # Si se desea obtener el mayor, se utiliza la matriz original
        if mayor_menor == 'Y' or mayor_menor == 'y':
            mayor = True
            mult_matriz = deepcopy(self.sp_matriz)
        # Para el menor, se utiliza la matriz inversa
        else:
            mayor = False
            self.invertir()
            if self.sp_matriz_inv is not None:
                mult_matriz = deepcopy(self.sp_matriz_inv)
            else:
                print("La matriz tiene determinante de 0, por lo que no es invertible, y por consiguiente, no es posible utilizar el método de potencias para obtener el valor propio de menor magnitud.")
                ##################################################
                # Dar opciones a partir de aquí

        # Se inicia con un vector estimación
        vect_estim = [0 for _ in range(self.dim)]
        print("\n• Inserción de los valores del vector de la estimación inicial. Recuerda que el vector debe tener una norma espectral de 1:")
        while True:
            try:
                entrada = input(
                    f"--> Inserte los valores separados por un espacio: ").strip().split(" ")
                vect_estim = insertar_reales(entrada, self.dim)

                if Abs(max(vect_estim)) != 1:
                    raise ValueError
                else:
                    vect_estim = Matrix(vect_estim)
                    break
            except ValueError:
                print("\n! - Asegúrate de insertar un vector cuya norma espectral sea 1")

        # Inserción de tolerancia y máximo de iteraciones
        print()
        max_it, toler = maxit_toler_checks()

        # Preparación de la tabla
        print("Tabla correspondiente a los cálculos:\n")
        if mayor:
            encabezado = ["k", "x^(k)", "Ax^(k)", "λ^(k+1)",
                          "x^(k+1)", "err. abs."]
        else:
            encabezado = ["k", "x^(k)", "Ax^(k)", "1/λ^(k+1)",
                          "x^(k+1)", "err. abs."]
        separador = ["", "", "", "", "", ""]

        # Definición de strings que se usarán para imprimir los valores de la tabla
        fila_inic = "| {:^3} | {:^13} | {:^13} | {:^14.6g} | {:^13} | {:^14.6g} |"
        fila_inic_strend = "| {:^3} | {:^13} | {:^13} | {:^14.6g} | {:^13} | {:^14} |"
        fila = "| {:^3} | {:^13} | {:^13} | {:^14} | {:^13} | {:^14} |"
        fila_sep = "| {:^3} | {:^13} | {:^13} | {:^14} | {:^13} | {:^14} |"

        # Imprimir el encabezado y el separador
        print("| {:^3} | {:^13} | {:^13} | {:^14} | {:^13} | {:^14} |".format(
            *encabezado))
        print(
            "| {:-^3} | {:-^13} | {:-^13} | {:-^14} | {:-^13} | {:-^14} |".format(*separador))

        prec_eigenvalue = 0
        for it in range(max_it):
            producto = mult_matriz * vect_estim
            eigenvalue = Abs(max(producto))
            eigenvector = producto / max(producto)
            err_abs = Abs(eigenvalue - prec_eigenvalue)

            # Impresión de resultados en la tabla
            # Se imprimen los vectores verticalmente
            for i in range(self.dim):
                # Si se trata del primer elemento del vector, imprimir el eigenvalor y el error
                if i == 0:
                    # Si se trata de la primera iteración, el error es "N/A"
                    if it == 0:
                        impr = [it, "⎡{:^ 9.6g}⎤".format(float(vect_estim[i])), "⎡{:^ 9.6g}⎤".format(float(
                            producto[i])), float(eigenvalue), "⎡{:^ 9.6g}⎤".format(float(eigenvector[i])), "N/A"]
                        print(fila_inic_strend.format(*impr))
                    else:
                        impr = [it, "⎡{:^ 9.6g}⎤".format(float(vect_estim[i])), "⎡{:^ 9.6g}⎤".format(float(
                            producto[i])), float(eigenvalue), "⎡{:^ 9.6g}⎤".format(float(eigenvector[i])), float(err_abs)]
                        print(fila_inic.format(*impr))
                # Si se trata de cualquier otra fila, no imprimir ni el eigenvalor ni el error
                else:
                    if i == self.dim-1:
                        impr = ["", "⎣{:^ 9.6g}⎦".format(float(vect_estim[i])), "⎣{:^ 9.6g}⎦".format(
                            float(producto[i])), "", "⎣{:^ 9.6g}⎦".format(float(eigenvector[i])), ""]
                    else:
                        impr = ["", "⎢{:^ 9.6g}⎥".format(float(vect_estim[i])), "⎢{:^ 9.6g}⎥".format(
                            float(producto[i])), "", "⎢{:^ 9.6g}⎥".format(float(eigenvector[i])), ""]
                    print(fila.format(*impr))
            # Imprimir espacio en blanco al final de cada vector
            print(fila_sep.format(*separador))

            # Determinar si se sigue iterando o no, según la tolerancia
            if err_abs <= toler:
                break
            else:
                prec_eigenvalue = eigenvalue
                vect_estim = eigenvector

        # Si se quiso obtener el menor eigenvalor, se trata del recíproco del cálculo final
        if not mayor:
            eigenvalue = 1/eigenvalue

        # Si se convergío satisfactoriamente
        if err_abs <= toler:
            print(
                f"\nSe convergió satisfactoriamente con una tolerancia menor o igual a {float(toler)}:\n")
            print(f"• El valor propio obtenido fue {float(eigenvalue)}")
            print(
                f"\nSe necesitó de {it} iteraciones y este cálculo tiene un error absoluto de {float(err_abs)}.")

            if mayor:
                self.eigenvalor_max = eigenvalue
            else:
                self.eigenvalor_min = eigenvalue

            ##################################################
            # Dar opciones para calcularlo de nuevo o algo así
        # Si no se convergió
        else:
            print(
                f"\nSe alcanzaron las {max_it} iteraciones máximas. No se pudo converger con una tolerancia menor o igual a {float(toler)}.")
            print(
                f"• La última aproximación a un valor propio fue {float(eigenvalue)}")
            print(
                f"\nEste cálculo tiene un error absoluto de {float(err_abs)}.")
            ##################################################
            # Dar opciones para corregir la matriz (¿acaso necesitamos EDD?), dar otro vector inicial, otra tolerancia/maxit, o cosas así


la_matriz = EigenMatriz()
la_matriz.corregir()
la_matriz.eigenvalores()
