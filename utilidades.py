from sympy import sympify


def clear_screen():
    import os
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def portada(titulo):
    clear_screen()
    datos = ["Universidad Nacional Autónoma de México",
             "Facultad de Estudios Superiores Acatlán",
             "Matemáticas Aplicadas y Computación\n",
             "{:-^47}\n".format(""),
             titulo,
             "Métodos de Solución de Ecuaciones No Lineales\n",
             "Alcaraz López Bella Samara",
             "Camargo Badillo Luis Mauricio",
             "Leon Valdés Duhart Guillermo Arturo",
             "López Díaz Diego\n",
             "Métodos Numéricos I",
             "Grupo 1301\n",
             "{:-^47}\n".format(""),
             "Presiona enter para continuar"]

    for dato in datos:
        print(" {:^47} ".format(dato))

    input()
    clear_screen()

# Checks para alguna entrada booleana (sí/no, etc.); opt_1 y opt_2 son mayúsculas
def bool_option(prompt, opt_1, opt_2):
    ans = input(prompt)
    while ans != opt_1 and ans != opt_1.lower() and ans != opt_2 and ans != opt_2.lower():
        ans = input(f"Introduzca {opt_1} o {opt_2}: ")
    return ans


# Checks para la entrada de reales, con sympify (Real o Rational)
def insertar_reales(entrada, size=1):
    if type(entrada) == list:
        # Cuando la entrada es una lista, revisar además que haya exactamente size elementos
        while len(entrada) != size:
            entrada = input(
                f"--> Asegúrate de insertar exactamente {size} elementos con exactamente un espacio entre ellos: ").strip().split(" ")

        # Solo números reales
        while True:
            try:
                entrada = [sympify(elem) for elem in entrada]
                if not all(elem.is_real for elem in entrada):
                    raise ValueError
                break
            except:
                entrada = input(
                    f"--> Solo inserta números reales: ").strip().split(" ")
    else:
        # Solo números reales
        while True:
            try:
                entrada = sympify(entrada)
                if not entrada.is_real:
                    raise ValueError
                break
            except:
                entrada = input(
                    f"--> Solo inserta un número real: ")

    return entrada


# Checks para la entrada de enteros, con opción de un valor máximo
def int_input(prompt, maxim):
    while True:
        try:
            ans = int(input(prompt))

            if maxim is None:
                if ans < 0:
                    raise IndexError
            else:
                if ans < 0 or ans >= maxim:
                    raise IndexError

            break
        except IndexError:
            if maxim is None:
                prompt = "--> Introduzca un número entero mayor o igual que 0: "
            else:
                prompt = f"--> Introduzca un número entero entero del 0 al {maxim-1}: "
        except:
            prompt = "--> Introduzca un número entero: "

    return ans
