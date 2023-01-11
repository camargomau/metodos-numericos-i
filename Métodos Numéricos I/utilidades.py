from sympy import sympify, Float

def clear_screen():
    import os
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def portada(titulo, desc):
    clear_screen()
    datos = ["Universidad Nacional Autónoma de México",
             "Facultad de Estudios Superiores Acatlán",
             "Matemáticas Aplicadas y Computación\n",
             "{:-^47}\n".format(""),
             titulo,
             f"{desc}\n",
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

# Introducción de iteraciones máximas, tolerancia y sus checks
def maxit_toler_checks():
    while True:
        try:
            max_it = int(input("• Máximo de iteraciones: "))
        except:
            print("\nIntroduzca un número entero.\n")
            continue

        if max_it > 0:
            break
        else:
            print("\nIntroduzca un número entero mayor que 0.\n")

    # Tolerancia y sus checks
    while True:
        try:
            toler = Float(input("• Tolerancia: "), 20)
        except:
            print("\nIntroduzca un número real.\n")
            continue

        if (toler > 0) and (toler < 1):
            break
        else:
            print("\nIntroduzca un valor en (0, 1).\n")

    return max_it, toler

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

# Checks para la entrada de enteros en [1, maxim]; maxim es opcional
def int_input(prompt, maxim):
    while True:
        try:
            ans = int(input(prompt))

            if maxim is None:
                if ans < 1:
                    raise IndexError
            else:
                if ans < 1 or ans > maxim:
                    raise IndexError

            break
        except IndexError:
            if maxim is None:
                prompt = "--> Introduzca un número entero mayor o igual que 1: "
            else:
                prompt = f"--> Introduzca un número entero entero del 1 al {maxim}: "
        except:
            prompt = "--> Introduzca un número entero: "

    return ans
