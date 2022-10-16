from sympy import Abs, diff, Float, nan, printing, Pow, real_root, Rational, sympify, Symbol, zoo

# x es la variable
x = Symbol('x')

#########
# Otros #
#########

def clear_screen():
    import os
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def portada():
    clear_screen()
    datos = ["Universidad Nacional Autónoma de México",
             "Facultad de Estudios Superiores Acatlán",
             "Matemáticas Aplicadas y Computación\n",
             "{:-^47}\n".format(""),
             "Programa 1:",
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

#########
# Menús #
#########

def menu_metodos():
    global eleccion_metodo
    opciones_metodos = {
        1: "Método de Bisección",
        2: "Método de la Posición Falsa",
        3: "Método de Newton",
        4: "Método de la Secante",

        0: "Salir del programa"
    }

    clear_screen()

    print("Métodos disponibles:\n")
    for opcion in opciones_metodos.keys():
        print(f"{opcion} --- {opciones_metodos[opcion]}")

    while True:
        try:
            eleccion_metodo = int(input("\n¿Qué método desea utilizar? "))
        except:
            print("\nIntroduzca un número entero.")
            continue

        if (eleccion_metodo >= 0) and (eleccion_metodo < len(opciones_metodos.keys())):
            break
        else:
            print(
                f"\nIntroduzca un número entre 0 y {len(opciones_metodos.keys())-1}.")

    if eleccion_metodo != 0:
        menu_funciones()

def menu_funciones():
    global func, eleccion_funcion
    opciones_funciones = {
        1: "x**2 * cos(x) - 2*x",
        2: "(6 - (2/x**2)) * (E**(2+x)/4) + 1",
        3: "x**3 - 3*sin(x**2) + 1",
        4: "x**3 + 6*(x**2) + 9.4*x + 2.5",

        # Funciones de los ejercicios del portafolio
        #5: "((50 + (37.49/x**2)) * (x - 0.197)) - (0.08205*348.15)",
        #6: "x * ((15*x)/(15+2*x))**(2/3) - ((0.015*20)/(15*sqrt(0.001)))",
        #7: "(((2+0.4*x**2)/2.4)**3.5 - 1)/(0.7*x**2*(-0.383)) - (sqrt(1-x**2)+(((x**2*(-0.383))/2)/(1+sqrt(1-x**2))))**(-1)",

        0: "Regresar al menú de métodos"
    }

    clear_screen()
    print("Funciones disponibles:\n")
    print("--------------------------------\n")
    for opcion in opciones_funciones.keys():
        if opcion != 0:
            pretty_func = printing.pretty(
                sympify(opciones_funciones[opcion]), use_unicode=False)
            print(f"• Función {opcion}:\n")
            print(f"{pretty_func}\n")
            print("--------------------------------\n")
        else:
            print("Introduzca 0 para regresar al menú de métodos.\n")

    while True:
        try:
            eleccion_funcion = int(input("¿Qué función desea utilizar? "))
        except:
            print("\nIntroduzca un número entero.\n")
            continue

        if (eleccion_funcion >= 0) and (eleccion_funcion < len(opciones_funciones.keys())):
            break
        else:
            print(
                f"\nIntroduzca un número entre 0 y {len(opciones_funciones.keys())-1}\n")

    if eleccion_funcion != 0:
        # func es la función elegida por el usuario
        # el .replace() es para evaluar obtener las ráices reales de toda raíz que se calcule
        func = sympify(opciones_funciones[eleccion_funcion]).replace(lambda expr: isinstance(
            expr, Pow) and isinstance(expr.exp, Rational), lambda expr: real_root(expr.base, expr.exp.q)**expr.exp.p)
        trigger_metodo()
    else:
        menu_metodos()

###########
# Métodos #
###########

# Introducción de iteraciones máximas, tolerancia y sus checks
def maxIt_toler_checks():
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
            toler = Float(input("• Tolerancia (error relativo): "), 20)
        except:
            print("\nIntroduzca un número real.\n")
            continue

        if (toler > 0) and (toler < 1):
            break
        else:
            print("\nIntroduzca un valor en (0, 1).\n")

    return max_it, toler

# Según las elecciones del usuario en el menú, utilizar el método deseado
def trigger_metodo():
    global deriv
    clear_screen()

    # Bisección y posición falsa
    if eleccion_metodo == 1 or eleccion_metodo == 2:
        if eleccion_metodo == 1:
            metodo_seleccionado = "bisección"
        else:
            metodo_seleccionado = "la posición falsa"
        print(f"Elegiste el método de {metodo_seleccionado}.\n")

        # Intervalo y sus checks
        while True:
            # Como pueden haber funciones sin ninguna raíz, dar la opción de regresar
            print("(introduzca una 'x' si desea regresar al menú de funciones)")

            a = input("• Valor de a (extremo izquierdo del intervalo): ")
            if (a == 'x') or (a == 'X'):
                menu_funciones()

            try:

                a = Float(a, 20)
                b = Float(input("• Valor de b (extremo derecho): "), 20)
            except:
                print("\nIntroduzca números reales.\n")
                continue

            try:
                fa = func.evalf(subs={x: a})
                fb = func.evalf(subs={x: b})
            except:
                print(
                    f"\nLa función no está definida en {float(a)} o en {float(b)}. Intenta con otro intervalo.\n")
                continue

            try:
                fa = Float(fa, 20)
                fb = Float(fb, 20)
            except:
                print(
                    f"\nLa función evaluada en {float(a)} o en {float(b)} da como resultado un número complejo. Intenta con otro intervalo.\n")
                # continue

            fb = Float(fb, 20)

            if fa*fb < 0:
                break
            else:
                print(
                    f"\nLa función evaluada en {float(a)} y en {float(b)} tiene signos iguales.")
                print(
                    f"Es posible que no haya una raíz en el intervalo [{float(a)}, {float(b)}]. Intenta con otro intervalo.\n")

        # Iteraciones máximas, tolerancia y sus checks
        max_it, toler = maxIt_toler_checks()

        # Todo correcto si se llegó hasta aquí
        # Encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        encabezado = [["it.", "a", "b", "f(a)", "f(b)", "p", "err. rel."], [
            "", "", "", "", "", "", ""]]
        print("| {:^3} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} |".format(
            *encabezado[0]))
        print(
            "| {:-^3} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} |".format(*encabezado[1]))

        # Procesar e imprimir resultados
        raiz, err_rel, it = biseccion_posFalsa(a, b, max_it, toler)

        if err_rel == 0:
            print(
                f"\nSe encontró una raíz en el intervalo [{float(a)}, {float(b)}]:")
            print(f"- La raíz encontrada fue {float(raiz)}")
            print(
                f"- Se necesitó de {it} iteraciones y esta raíz es exacta")
            input("\nPresiona enter para continuar.")
        elif err_rel <= toler:
            print(
                f"\nSe encontró una raíz en el intervalo [{float(a)}, {float(b)}] con un error relativo menor o igual a {float(toler)}:")
            print(f"- La raíz encontrada fue {float(raiz)}")
            print(
                f"- Se necesitó de {it} iteraciones y la raíz tiene un error relativo de {float(err_rel)}")
            input("\nPresiona enter para continuar.")
        else:
            print(f"\nSe alcanzaron las {it} iteraciones máximas:")
            print(
                f"- No se pudo encontrar una raíz en el intervalo [{float(a)}, {float(b)}] con un error relativo menor a {float(toler)}")
            print(
                f"- El valor más preciso encontrado fue {float(raiz)}, que tiene un error relativo de {float(err_rel)}")
            print("Puede volver a intentar encontrar una raíz, esta vez con más iteraciones, otra tolerancia u otro intervalo.")
            input("\nPresiona enter para continuar.")

    # Newton
    elif eleccion_metodo == 3:
        print(f"Elegiste el método de Newton.\n")

        deriv = diff(func)

        # x0 y sus checks
        while True:
            print("(introduzca una 'x' si desea regresar al menú de funciones)")

            x0 = input("• Valor inicial (x_0): ")
            if (x0 == 'x') or (x0 == 'X'):
                menu_funciones()

            try:
                x0 = Float(x0, 20)
            except:
                print("\nIntroduzca un número real.\n")
                continue

            try:
                dx0 = deriv.evalf(subs={x: x0}).round(20)
            except:
                print(
                    f"\nLa derivada no está definida en {float(x0)}. Intenta con otro valor.\n")
                continue

            if dx0 != 0:
                break
            else:
                print(
                    f"\nLa derivada evaluada en {float(x0)} es igual a 0. Intenta con otro valor.\n")

        # Iteraciones máximas, tolerancia y sus checks
        max_it, toler = maxIt_toler_checks()

        # Todo correcto si se llegó hasta aquí
        # Encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        encabezado = [["it", "x_k", "f(x_k)", "f'(x_k)", "err. rel."], [
            "", "", "", "", ""]]
        print("| {:^3} | {:^14} | {:^14} | {:^14} | {:^14} |".format(
            *encabezado[0]))
        print(
            "| {:-^3} | {:-^14} | {:-^14} | {:-^14} | {:-^14} |".format(*encabezado[1]))

        # Procesar e imprimir resultados
        raiz, err_rel, it = newton(x0, max_it, toler)

        if err_rel <= toler:
            print(
                f"\nSe encontró una raíz a partir del punto inicial {float(x0)} con un error relativo menor o igual a {float(toler)}:")
            print(f"- La raíz encontrada fue {float(raiz)}")
            print(
                f"- Se necesitó de {it} iteraciones y la raíz tiene un error relativo de {float(err_rel)}")
            input("\nPresiona enter para continuar.")
        else:
            print(f"\nSe alcanzaron las {it} iteraciones máximas:")
            print(
                f"- No se pudo encontrar una raíz a partir del punto inicial {float(x0)} con un error relativo menor a {float(toler)}")
            print(
                f"- El valor más preciso encontrado fue {float(raiz)}, que tiene un error relativo de {float(err_rel)}")
            print("Puede volver a intentar encontrar una raíz, esta vez con más iteraciones, otra tolerancia u otro valor inicial.")
            input("\nPresiona enter para continuar.")

    # Secante
    elif eleccion_metodo == 4:
        print(f"Elegiste el método de la secante.\n")

        # Valores iniciales y sus checks
        while True:
            print("(introduzca una 'x' si desea regresar al menú de funciones)")

            x0 = input("• Valor de x_0: ")
            if (x0 == 'x') or (x0 == 'X'):
                menu_funciones()

            try:
                x0 = Float(x0, 20)
                x1 = Float(input("• Valor de x_1: "), 20)
            except:
                print("\nIntroduzca números reales.\n")
                continue

            try:
                fx0 = func.evalf(subs={x: x0})
                fx1 = func.evalf(subs={x: x1})
            except:
                print(
                    f"\nLa función no está definida en {float(x0)} o en {float(x1)}. Intenta con otro intervalo.\n")
                continue

            break

        # Iteraciones máximas, tolerancia y sus checks
        max_it, toler = maxIt_toler_checks()

        # Todo correcto si se llegó hasta aquí
        # Encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        encabezado = [["it", "x_k-1", "x_k",
                       "f(x_k-1)", "f(x_k)", "x_k+1", "err. rel."], ["", "", "", "", "", "", ""]]
        print("| {:^3} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} |".format(
            *encabezado[0]))
        print(
            "| {:-^3} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} |".format(*encabezado[1]))

        # Procesar e imprimir resultados
        raiz, err_rel, it = secante(x0, x1, max_it, toler)

        if err_rel <= toler:
            print(
                f"\nSe encontró una raíz a partir de los puntos iniciales {float(x0)} y {float(x1)} con un error relativo menor o igual a {float(toler)}:")
            print(f"- La raíz encontrada fue {float(raiz)}")
            print(
                f"- Se necesitó de {it} iteraciones y la raíz tiene un error relativo de {float(err_rel)}")
            input("\nPresiona enter para continuar.")
        else:
            print(f"\nSe alcanzaron las {it} iteraciones máximas:")
            print(
                f"- No se pudo encontrar una raíz a partir de los puntos iniciales {float(x0)} y {float(x1)} con un error relativo menor a {float(toler)}")
            print(
                f"- El valor más preciso encontrado fue {float(raiz)}, que tiene un error relativo de {float(err_rel)}")
            print("Puede volver a intentar encontrar una raíz, esta vez con más iteraciones, otra tolerancia u otro valor inicial.")
            input("\nPresiona enter para continuar.")

    fin_metodo()

# Función para el método de bisección *y* el de la posición falsa
def biseccion_posFalsa(a, b, max_it, toler):
    for it in range(max_it):
        fa = func.evalf(subs={x: a}).round(20)
        fb = func.evalf(subs={x: b}).round(20)
        assert (fa * fb) <= 0, "f(a) y f(b) deberían tener signos diferentes; en teoría nunca debería imprimirme."

        # Calcular el punto medio, según el método seleccionado
        # Bisección
        if eleccion_metodo == 1:
            p = (a + b)/2
        # Falsa posición
        elif eleccion_metodo == 2:
            p = b - (fb * (a - b)/(fa - fb))

        fp = func.evalf(subs={x: p})

        # Si p = 0, el error relativo no se puede calcular
        # pero aún así podemos continuar, con algunas consideraciones
        # sympy nos da zoo (infinidad compleja, x/0) o nan (0/0) cuando se divide entre 0
        if it != 0:
            err_rel = Abs(p - anterior)/Abs(p)
        else:
            err_rel = nan

        # Imprimir la tabla de los cálculos
        # Para primera iteración o si el err_rel no existe, imprimir N/A
        if (it == 0) or (err_rel is zoo) or (err_rel is nan):
            fila = [it+1, float(a), float(b), float(fa), float(fb),
                    float(p), " N/A"]
            print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:<14} |".format(*fila))
        else:
            fila = [it+1, float(a), float(b), float(fa), float(fb),
                    float(p), float(err_rel)]
            print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} |".format(*fila))

        it += 1

        # Determinar si continuar con el método o terminar
        # Se toma en cuenta si err_rel existe
        if (err_rel is not zoo) and (err_rel is not nan):
            # Si f(p) = 0, ya encontramos la raíz
            if fp == 0:
                return p, 0, it
            else:
                # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
                if (it == max_it) or (err_rel < toler):
                    return p, err_rel, it
                # De otra forma, continuar, cambiando el intervalo según se necesite
                elif (fa * fp) < 0:
                    b = p
                    anterior = p
                else:
                    a = p
                    anterior = p
        # Si no se pudo determinar err_rel anteriormente, siempre continuar
        else:
            if fp == 0:
                return p, 0, it
            else:
                if (fa * fp) < 0:
                    b = p
                    anterior = p
                else:
                    a = p
                    anterior = p

def newton(xk, max_it, toler):
    for it in range(max_it):
        # Evaluación de la función y devirada en x_k
        fxk = func.evalf(subs={x: xk}).round(20)
        dxk = deriv.evalf(subs={x: xk})
        if (dxk is not zoo) and (dxk is not nan):
            # Poco elegante pero funciona
            # un dxk.round(20) falla cuando el número abs es muy pequeño
            dxk = Float(round(eval(f'{dxk}'), 20))
        else:
            print("\n| {:^71} |".format(
                "Valor inicial desafortunado. Intenta con otro."))
            input("\nPresiona enter para continuar.")
            trigger_metodo()

        # Cálculo del siguiente valor
        # Si dxk = 0, xkp1 es zoo (infinidad compleja, x/0) o nan (0/0)
        xkp1 = xk - (fxk/dxk)
        if (xkp1 is zoo) or (xkp1 is nan):
            print("\n| {:^71} |".format(
                "Valor inicial desafortunado (la derivada es 0). Intenta con otro."))
            input("\nPresiona enter para continuar.")
            trigger_metodo()

        # Si xkp1 = 0, el error relativo no se puede calcular
        # pero aún así podemos continuar, con algunas consideraciones
        # sympy nos da zoo (infinidad compleja, x/0) o nan (0/0) cuando se divide entre 0
        err_rel = Abs(xkp1 - xk)/Abs(xkp1)

        # Imprimir la tabla de los cálculos
        # Si el err_rel no existe, imprimir N/A
        if (err_rel is zoo) or (err_rel is nan):
            fila = [it+1, float(xk), float(fxk), float(dxk), " N/A"]
            print(
                "| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:<14} |".format(*fila))
        else:
            fila = [it+1, float(xk), float(fxk), float(dxk), float(err_rel)]
            print(
                "| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} |".format(*fila))

        it += 1

        # Determinar si continuar con el método o terminar
        # Se toma en cuenta si err_rel existe
        if (err_rel is not zoo) and (err_rel is not nan):
            # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
            if (it == max_it) or (err_rel < toler):
                return xkp1, err_rel, it
            # De otra forma, continuar, ahora utilizando el valor recién calculado
            else:
                xk = xkp1
        # Si no se pudo determinar err_rel anteriormente, siempre continuar
        else:
            xk = xkp1

def secante(xkm1, xk, max_it, toler):
    for it in range(max_it):
        # Evaluación de la función en x_k y x_k-1
        fxkm1 = func.evalf(subs={x: xkm1}).round(20)
        fxk = func.evalf(subs={x: xk}).round(20)

        # Cálculo del siguiente valor
        # Si (fxm1 - fxk) = 0, xkp1 es zoo (infinidad compleja, x/0) o nan (0/0)
        xkp1 = xk - (fxk)*((xkm1 - xk)/(fxkm1 - fxk))
        if (xkp1 is zoo) or (xkp1 is nan):
            print("\n| {:^105} |".format(
                "Valor inicial desafortunado (división entre 0). Intenta con otro."))
            input("\nPresiona enter para continuar.")
            trigger_metodo()

        # Si xkp1 = 0, el error relativo no se puede calcular
        # pero aún así podemos continuar, con algunas consideraciones
        # sympy nos da zoo (infinidad compleja, x/0) o nan (0/0) cuando se divide entre 0
        err_rel = Abs(xkp1 - xk)/Abs(xkp1)

        # Imprimir la tabla de los cálculos
        # Si el err_rel no existe, imprimir N/A
        if (err_rel is zoo) or (err_rel is nan):
            fila = [it+1, float(xkm1).round(20), float(xk).round(20), float(fxkm1),
                    float(fxk), float(xkp1), " N/A"]
            print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:<14} |".format(*fila))
        else:
            fila = [it+1, float(xkm1), float(xk), float(fxkm1),
                    float(fxk), float(xkp1), float(err_rel)]
            print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} |".format(*fila))

        it += 1

        # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
        # Determinar si continuar con el método o terminar
        # Se toma en cuenta si err_rel existe
        if (err_rel is not zoo) and (err_rel is not nan):
            if (it == max_it) or (err_rel < toler):
                return xkp1, err_rel, it
            # De otra forma, continuar, ahora utilizando el valor recién calculado
            else:
                xkm1 = xk
                xk = xkp1
        # Si no se pudo determinar err_rel anteriormente, siempre continuar
        else:
            xkm1 = xk
            xk = xkp1

def fin_metodo():
    clear_screen()

    print("1 --- Calcular otra raíz de la misma función con el mismo método")
    print("2 --- Regresar al menú de funciones")
    print("3 --- Regresar al menú de métodos")

    while True:
        try:
            resp = int(input("\n¿Qué desea hacer a continuación? "))
        except:
            print("\nIntroduzca un número entero.")
            continue

        if resp == 1:
            trigger_metodo()
            break
        elif resp == 2:
            menu_funciones()
            break
        elif resp == 3:
            menu_metodos()
            break
        else:
            print("Introduzca un número entre el 1 y el 3: ")

#############
# Principal #
#############

portada()
menu_metodos()
