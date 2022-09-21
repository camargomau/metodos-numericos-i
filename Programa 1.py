from tkinter import E
import sympy 

x = sympy.Symbol('x')
it = 0

# Limpiar pantalla
def clear_screen():
    import os

    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def menu():
    global func, eleccion_metodo, eleccion_funcion

    opciones_metodos = {
        1: "Método de Bisección",
        2: "Método de Newton"
    }
    
    opciones_funciones = {
        1: "x**2 * cos(x) - 2*x",
        2: "(((6-2)/x**2) * E**(x+2))/(4+1)",
        3: "x**3 - 3*sin(x**2) + 1",
        4: "x**3 + 6*(x**2) + 9.4*x + 2.5",
        5: "((50 + (37.49/x**2)) * (x - 0.197)) - (0.08205*348.15)"
    }

    # Menú de métodos
    clear_screen()
    for opcion in opciones_metodos.keys():
        print(f"{opcion} --- {opciones_metodos[opcion]}")
    eleccion_metodo = int(input("¿Qué método desea utilizar? "))
    clear_screen()

    # Método de funciones
    for opcion in opciones_funciones.keys():
        print(f"{opcion} --- {opciones_funciones[opcion]}")
    eleccion_funcion = int(input("¿Qué función desea utilizar? "))
    clear_screen()

    # Definir la función según la elección del usuario
    func = sympy.sympify(opciones_funciones[eleccion_funcion])

# Según las elecciones del usuario en el menú, utilizar el método deseado
def proceso_metodo():
    global it
    it = 0

    if eleccion_metodo == 1:
        print(f"Elegiste el método de bisección y la función [print the (pretty) function here]")

        a = float(input("- Valor de a: "))
        b = float(input("- Valor de b: "))
        max_it = int(input("- Máximo de iteraciones: "))
        toler = float(input("- Tolerancia: "))
        
        # Evaluar la función en a y b
        try:
            fa = func.evalf(subs={x:a})
            fb = func.evalf(subs={x:b})
        # Si no está definida en alguno de los dos, terminar y notificar 
        except:
            print(f"\nLa función no está definida en {a} o {b}. Intenta con otros valores.\n")
            proceso_metodo()

        # Imprimir según la existencia de la raíz en el intervalo
        if (fa * fb) < 0:
            # Imprimir el encabezado de la tabla
            clear_screen()
            print("Tabla correspondiente a los cálculos:\n")
            print("| it. |      a       |      b       |     f(a)     |     f(b)     |      p       |  err. rel.   |")
            print("|-----|--------------|--------------|--------------|--------------|--------------|--------------|")
            
            # Procesar todo con la función correspondiente; imprimir resultados
            raiz, err_rel = biseccion(a, b, 0, max_it, toler)

            print(f"\nLa raíz encontrada en el intervalo [{a}, {b}] fue {raiz}")
            print(f"Se necesitó de {it-1} iteraciones y este cálculo tiene un error relativo de {err_rel}")
        else:
            print(f"\nNo hay una raíz en el intervalo [{a}, {b}]")
    
    elif eleccion_metodo == 2:
        print(f"Elegiste el método de bisección y la función {func}")

        x0 = float(input("- Valor inicial (x_0): "))
        max_it = int(input("- Máximo de iteraciones: "))
        toler = float(input("- Tolerancia: "))

        # Imprimir el encabezado de la tabla
        clear_screen()
        print("Tabla correspondiente a los cálculos:\n")
        print("| it. |     x_k      |    f(x_k)    |    f'(x_k)   |   err. rel.  |")
        print("|-----|--------------|--------------|--------------|--------------|")
        
        # Procesar todo con la función correspondiente; imprimir resultados
        raiz, err_rel = newton(x0, max_it, toler)

        print(f"\nLa raíz encontrada a partir del punto inicial {x0} fue {raiz}")
        print(f"Se necesitó de {it-1} iteraciones y este cálculo tiene un error relativo de {err_rel}")
        

def biseccion(a, b, anterior, max_it, toler):
    global it
    # Evaluar la función en a y b
    fa = func.evalf(subs={x:a})
    fb = func.evalf(subs={x:b})

    # Verificar que entre a y b haya una raíz
    if (fa * fb) < 0:
        # Calcular el punto medio
        p = (a + b)/2
        fp = func.evalf(subs={x:p})
        err_rel = abs(p - anterior)/abs(p)

        # Imprimir la tabla de los cálculos
        fila = [it, format(a, '.6f'), format(b, '.6f'), format(fa, '.6f'), format(fb, '.6f'), format(p, '.6f'), format(err_rel, '.6f')]
        print("| {:>3} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} | {:>12} |".format(*fila))

        it += 1
        
        # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
        if (it == max_it) or (err_rel < toler):
            return p, err_rel
        # De otra forma, continuar, cambiando el intervalo según se necesite
        elif (fa * fp) < 0:
            return biseccion(a, p, p, max_it, toler)
        else:
            return biseccion(p, b, p, max_it, toler)

def newton(xk, max_it, toler):
    global it
    # Derivada y evaluación
    deriv = sympy.diff(func)
    fxk = func.evalf(subs={x:xk})
    dxk = deriv.evalf(subs={x:xk})
    # Cálculo del siguiente valor y del error
    xkp1 = xk - (fxk/dxk)
    err_rel = abs(xkp1 - xk)/abs(xkp1)

    # Imprimir la tabla de los cálculos
    fila = [it, format(xk, '.6f'), format(fxk, '.6f'), format(dxk, '.6f'), format(err_rel, '.6f')]
    print("| {:>3} | {:>12} | {:>12} | {:>12} | {:>12} |".format(*fila))

    it += 1

    # Si se ha llegado a la iteración máxima o el error ya es menor al deseado, terminar
    if (it == max_it) or (err_rel < toler):
        return xkp1, err_rel
    # De otra forma, continuar, ahora utilizando el valor recién calculado
    else:
        return newton(xkp1, max_it, toler)

###
# Principal
###

while True:
    menu()
    proceso_metodo()

    resp = input("\n¿Desea regresar al menú? S para sí, N para salir del programa ")
    if (resp != 's') and (resp != 'S'):
        break
