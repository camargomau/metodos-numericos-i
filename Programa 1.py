import sympy
x = sympy.Symbol('x')

#########
# Otros #
#########

def clear_screen():
    import os
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

#########
# Menús #
#########

def menu_metodos():
    global eleccion_metodo
    opciones_metodos = {
        1: "Método de Bisección",
        2: "Método de la Posición Falsa",
        3: "Método de Newton",

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

        if (eleccion_metodo >= 0) and (eleccion_metodo <= len(opciones_metodos.keys())):
            break
        else:
            print(f"\nIntroduzca un número entre 0 y {len(opciones_metodos.keys())-1}")

    if eleccion_metodo != 0:
        menu_funciones()

def menu_funciones():
    global func, eleccion_funcion
    opciones_funciones = {
        1: "x**2 * cos(x) - 2*x",
        2: "(((6-2)/x**2) * E**(x+2))/(4+1)",
        3: "x**3 - 3*sin(x**2) + 1",
        4: "x**3 + 6*(x**2) + 9.4*x + 2.5",

        # Funciones de los ejercicios del portafolio
        #5: "((50 + (37.49/x**2)) * (x - 0.197)) - (0.08205*348.15)",
        #6: "x * ((15*x)/(15+2*x))**(2/3) - ((0.015*20)/(15*sqrt(0.001)))",

        0: "Regresar al menú de métodos"
    }
    
    clear_screen()
    print("Funciones disponibles:\n")
    print("--------------------------------\n")
    for opcion in opciones_funciones.keys():
        if opcion != 0:
            pretty_func = sympy.printing.pretty(sympy.sympify(opciones_funciones[opcion]), use_unicode=True)
            print(f"• Función {opcion}:\n")
            print(f"{pretty_func}\n")
            print("--------------------------------\n")
        else:
            print("Introduzca 0 para regresar al menú de métodos.\n")

    while True:
        try:
            eleccion_funcion = int(input("¿Qué función desea utilizar? "))
        except:
            print("\nIntroduzca un número entero.")
            continue

        if (eleccion_funcion >= 0) and (eleccion_metodo <= len(opciones_funciones.keys())):
            break
        else:
            print(f"\nIntroduzca un número entre 0 y {len(opciones_funciones.keys())-1}")

    if eleccion_funcion != 0:
        func = sympy.sympify(opciones_funciones[eleccion_funcion])
        trigger_metodo()
    else:
        menu_metodos()

###########
# Métodos #
###########

# Según las elecciones del usuario en el menú, utilizar el método deseado
def trigger_metodo():
    global it, deriv
    it = 0

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
            try:
                a = float(input("• Valor de a (extremo izquierdo del intervalo): "))
                b = float(input("• Valor de b (extremo derecho): "))
            except:
                print("\nIntroduzca números reales.\n")
                continue

            try:
                fa = func.evalf(subs={x:a})
                fb = func.evalf(subs={x:b})
            except:
                print(f"\nLa función no está definida en {a} o en {b}. Intenta con otro intervalo.\n")
                continue
                
            if (fa * fb) < 0:
                break
            else:
                print(f"\nLa función evaluada en {a} y en {b} tiene signos iguales.")
                print(f"Es posible que no haya una raíz en el intervalo [{a}, {b}]. Intenta con otro intervalo.\n")

        # Iteraciones máximas y sus checks
        while True:
            try:
                max_it = int(input("• Máximo de iteraciones: "))
            except:
                print("\nIntroduzca un número entero.\n")
                continue

            if max_it > 0:
                break
            else:
                print("\nIntroduzca un número entero mayor que 0\n")

        # Tolerancia y sus checks
        while True:
            try:
                toler = float(input("• Tolerancia (error relativo): "))
            except:
                print("\nIntroduzca un número real.\n")
                continue
            
            if (toler > 0) and (toler < 1):
                break
            else:
                print("\nIntroduzca un valor en (0, 1).\n")

        # Todo correcto si se llegó hasta aquí
        # Encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        encabezado = [["it.", "a", "b", "f(a)", "f(b)", "p", "err. rel."], ["", "", "", "", "", "", ""]]
        print("| {:^3} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} | {:^14} |".format(*encabezado[0]))
        print("| {:-^3} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} | {:-^14} |".format(*encabezado[1]))
        
        # Procesar e imprimir resultados
        raiz, err_rel = biseccion_posFalsa(a, b, 0, max_it, toler)
        if err_rel <= toler:
            print(f"\nSe encontró una raíz en el intervalo [{a}, {b}] con un error relativo menor o igual a {toler}")
            print(f"La raíz encontrada fue {raiz}")
            print(f"Se necesitó de {it} iteraciones y la raíz tiene un error relativo de {err_rel}")
            input("\nPresiona enter para continuar")
        else:
            print(f"\nSe alcanzaron las {it} iteraciones máximas")
            print(f"No se pudo encontrar una raíz en el intervalo [{a}, {b}] con un error relativo menor a {toler}")
            print(f"El valor más preciso encontrado fue {raiz}, que tiene un error relativo de {err_rel}")
            print("Puede volver a intentar encontrar una raíz, esta vez con más iteraciones, otra tolerancia u otro intervalo")
            input("\nPresiona enter para continuar")
    
    # Newton
    elif eleccion_metodo == 3:
        print(f"Elegiste el método de Newton.")

        deriv = sympy.diff(func)

        # x0 y sus checks
        while True:
            try:
                x0 = float(input("• Valor inicial (x_0): "))
            except:
                print("\nIntroduzca un número real.\n")
                continue

            try:
                dx0 = deriv.evalf(subs={x:x0})
            except:
                print(f"\nLa derivada no está definida en {x0}. Intenta con otro valor.\n")
                continue

            if dx0 != 0:
                break
            else:
                print(f"\nLa derivada evaluada en {x0} es igual a 0. Intenta con otro valor.\n")
        
        # Iteraciones máximas y sus checks
        while True:
            try:
                max_it = int(input("• Máximo de iteraciones: "))
            except:
                print("\nIntroduzca un número entero.\n")
                continue

            if max_it > 0:
                break
            else:
                print("\nIntroduzca un número entero mayor que 0\n")

        # Tolerancia y sus checks
        while True:
            try:
                toler = float(input("• Tolerancia (error relativo): "))
            except:
                print("\nIntroduzca un número real.\n")
                continue
            
            if (toler > 0) and (toler < 1):
                break
            else:
                print("\nIntroduzca un valor en (0, 1).\n")

        # Todo correcto si se llegó hasta aquí
        # Encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        encabezado = [["it", "x_k", "f(x_k)", "f'(x_k)", "err. rel."], ["", "", "", "", ""]]
        print("| {:^3} | {:^14} | {:^14} | {:^14} | {:^14} |".format(*encabezado[0]))
        print("| {:-^3} | {:-^14} | {:-^14} | {:-^14} | {:-^14} |".format(*encabezado[1]))
        
        # Procesar e imprimir resultados
        raiz, err_rel = newton(x0, max_it, toler)
        if err_rel <= toler:
            print(f"\nSe encontró una raíz a partir del punto inicial {x0} con un error relativo menor o igual a {toler}")
            print(f"La raíz encontrada fue {raiz}")
            print(f"Se necesitó de {it} iteraciones y la raíz tiene un error relativo de {err_rel}")
            input("\nPresiona enter para continuar")
        else:
            print(f"\nSe alcanzaron las {it} iteraciones máximas")
            print(f"No se pudo encontrar una raíz a partir del punto inicial {x0} con un error relativo menor a {toler}")
            print(f"El valor más preciso encontrado fue {raiz}, que tiene un error relativo de {err_rel}")
            print("Puede volver a intentar encontrar una raíz, esta vez con más iteraciones, otra tolerancia u otro valor inicial")
            input("\nPresiona enter para continuar")

    fin_metodo()

# Función para el método de bisección *y* el de la posición falsa
def biseccion_posFalsa(a, b, anterior, max_it, toler):
    global it

    fa = func.evalf(subs={x:a})
    fb = func.evalf(subs={x:b})

    assert (fa * fb) < 0, "f(a) y f(b) deberían tener signos diferentes; en teoría nunca debería imprimirme"

    # Calcular el punto medio, según el método seleccionado
    # Bisección
    if eleccion_metodo == 1:
        p = (a + b)/2
    # Falsa posición
    elif eleccion_metodo == 2:
        p = b - (fb * (a - b)/(fa - fb))

    fp = func.evalf(subs={x:p})
    err_rel = abs(p - anterior)/abs(p)

    # Imprimir la tabla de los cálculos
    fila = [it+1, float(a), float(b), float(fa), float(fb), float(p), float(err_rel)]
    print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} |".format(*fila))

    it += 1
    # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
    if (it == max_it) or (err_rel < toler):
        return p, err_rel
    # De otra forma, continuar, cambiando el intervalo según se necesite
    elif (fa * fp) < 0:
        return biseccion_posFalsa(a, p, p, max_it, toler)
    else:
        return biseccion_posFalsa(p, b, p, max_it, toler)

def newton(xk, max_it, toler):
    global it
    # Evaluación de x_k en la función y devirada
    fxk = func.evalf(subs={x:xk})
    dxk = deriv.evalf(subs={x:xk})
    # Cálculo del siguiente valor y del error
    xkp1 = xk - (fxk/dxk)

    if (fxk == 0) or (dxk == 0) or (xkp1 == 0):
        print("\n| {105} |".format("Valor inicial desafortunado (división entre 0). Intenta con otro"))
        input("\nPresiona enter para continuar")
        trigger_metodo()

    err_rel = abs(xkp1 - xk)/abs(xkp1)

    # Imprimir la tabla de los cálculos
    fila = [it+1, float(xk), float(fxk), float(dxk), float(err_rel)]
    print("| {:^3} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} | {:< 14.6g} |".format(*fila))

    it += 1
    # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
    if (it == max_it) or (err_rel < toler):
        return xkp1, err_rel
    # De otra forma, continuar, ahora utilizando el valor recién calculado
    else:
        return newton(xkp1, max_it, toler)

def fin_metodo():
    clear_screen()

    print("1 --- Calcular otra raíz de la misma función con el mismo método")
    print("2 --- Regresar al menú de funciones")
    print("3 --- Regresar al menú de métodos")

    resp = int(input("\n¿Qué desea hacer a continuación? "))
    while True:
        if resp == 1:
            trigger_metodo()
            break
        elif resp == 2:
            menu_funciones()
            break
        elif resp == 3:
            break
        else:
            print("Introduzca un número entre el 1 y el 3: ")

#############
# Principal #
#############

menu_metodos()