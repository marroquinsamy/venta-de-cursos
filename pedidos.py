# Algoritmos y programación básica
# Sección 60
# Rodrigo Lou 20164

import numpy as pd
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
from termcolor import cprint # Permite colorear el texto
from csv import writer # Permite escribir sobre archivos .csv
import os

# Función que me permitirá validar la opción a ejecutar en el menú principal
def validarSeleccionMenu(frase):
    while True:
        try:
            entrada = int(input(frase))
            return entrada
        except ValueError:
            cprint("ERROR: Dato incorrecto. Inténtalo de nuevo.", "red", attrs = ["bold"])

def añadirFilaCSV(archivoCSV, listaParaAñadir):
    # Abre el archivo CSV en modo añadir
    with open(archivoCSV, "a+", newline = "") as objetoEscritor:
        # Crea un objeto escritor desde el módulo csv
        escritorCSV = writer(objetoEscritor)
        # Añade el contenido de la lista como última línea en el archivo .csv
        escritorCSV.writerow(listaParaAñadir)

def validarEntradaNoVacia(frase):
    entrada = input(frase)
    while entrada == "":
        cprint("ERROR: el dato ingresado no puede estar vacío. Inténtelo de nuevo.", "red", attrs = ["bold"])
        entrada = input(frase)
    else:
        return entrada

def generadorContraseña(nombreCliente, totalCursos, nombreAsesor):
    print("Contraseña: " + (nombreCliente[0] + nombreCliente[1] + nombreCliente[2]).upper() + str(totalCursos) + (nombreAsesor[-3] + nombreAsesor[-2] + nombreAsesor[-1]).lower())

vendedor = validarEntradaNoVacia("Vendedor: ")
# Esto con objeto de no obtener error al generar la contraseña
while len(vendedor) < 3:
    cprint("ERROR: longitud menor a 3 caracteres. Inténtelo de nuevo.", "red", attrs = ["bold"])
    vendedor = validarEntradaNoVacia("Vendedor: ")

seleccionMenu = -1
while seleccionMenu != 0:
    os.system("clear")
    os.system("cls")
    cprint("BIENVENIDO, " + vendedor.upper(), "yellow", attrs = ["bold"])
    print("1. Inscribir un nuevo alumno\n2. Mostrar estadísticas\n3. Agregar más cursos\n0. Salir")
    seleccionMenu = validarSeleccionMenu("Selecciona la opción que deseas ejecutar: ")

    if seleccionMenu == 0:
        print("Programa finalizado.")
        break
    
    # Inscribir a un nuevo alumno
    if seleccionMenu == 1:
        clientes_db = pd.read_csv("clients_database.csv", delimiter = ",")
        cursos_db = pd.read_csv("courses_database.csv", delimiter = ",")
        os.system("clear")
        os.system("cls")
        datosCliente = []

        cprint("INSCRIPCIÓN DE ALUMNOS", "yellow", attrs = ["bold"])
        datosCliente.append(validarEntradaNoVacia("Nombre: "))
        # Esto con objeto de no tener problemas al generar la contraseña
        while len(datosCliente[0]) < 3:
            cprint("ERROR: longitud menor a 3 caracteres. Inténtelo de nuevo.", "red", attrs = ["bold"])
            datosCliente.pop(0)
            datosCliente.insert(0, validarEntradaNoVacia("Nombre: "))
        datosCliente.append(validarEntradaNoVacia("Correo electrónico: "))
        print("Cursos disponibles (para comprar varios cursos sepáralos con una , y un espacio entre cada uno de ellos): \n0. SALIR")

        # Se crea la lista de precios basados en el orden de los datos en el archivo .csv
        listaPrecios = []
        for precio in cursos_db.precio.values:
            listaPrecios.append(precio)

        # Se muestra la información al usuario acerca de los cursos disponibles y su precio
        listaCursos = []
        cantidadCursos = len(cursos_db.curso.values)
        for index, cursoDesdeDB in enumerate(cursos_db.curso.values):
            listaCursos.append(cursoDesdeDB)
            print(str(index + 1) + ". " + cursoDesdeDB.upper() + " - Q" + str(listaPrecios[index]))
        cursosElegidos = validarEntradaNoVacia("Cursos a tomar: ").split(", ")

        decision = ""
        for index, curso in enumerate(cursosElegidos):
            # Si la cadena de texto contiene un 0, se pregunta si quiere salir por si el usuario desea eso
            if int(curso) == 0:
                decision = validarEntradaNoVacia("¿Deseas salir? (s|n) ").lower()
                if decision == "s":
                    break
            # Si en dado caso el curso no existe, se vuelve a pedir
            if int(curso) < 1 or int(curso) > cantidadCursos:
                cursosElegidos.pop(index)
                cursosElegidos.insert(index, validarEntradaNoVacia("Este curso no existe (" + curso + "), inténtalo de nuevo: "))
        if decision == "s":
            continue
        
        # En este apartado se prepara toda la información para ser añadida a la base de datos
        cursosParaIngresar = ""
        precioSeleccionado = []
        total = 0
        totalCursos = 0
        index = 0
        for index, curso in enumerate(cursosElegidos):
            if index == 0:
                cursosParaIngresar += str(listaCursos[int(curso) - 1])
            else:
                cursosParaIngresar += ", " + str(listaCursos[int(curso) - 1])
            # Se van añadiendo los precios de los cursos a una lista para posteriormente sumarlos
            precioSeleccionado.append(listaPrecios[int(curso) - 1])
        totalCursos = index + 1

        total = sum(precioSeleccionado)
        datosCliente.append(cursosParaIngresar)
        print("\nRESUMEN")
        print("Cliente: " + datosCliente[0])
        print("Correo electrónico: " + datosCliente[1])
        print("Cursos: " + cursosParaIngresar)
        cprint("Total de la compra: Q" + str(total), "blue", attrs = ["bold"])
        seguir = validarEntradaNoVacia("¿Desea continuar? (s|n): ").lower()
        if seguir == "n":
            cprint("No se realizaron cambios sobre la base de datos.", "red", attrs = ["bold"])
            input()
            continue
        
        generadorContraseña(datosCliente[0], totalCursos, vendedor)
        datosCliente.append(vendedor.lower())
        añadirFilaCSV("clients_database.csv", datosCliente)
        cprint("El cliente ha sido añadido con éxito a la base de datos.", "green", attrs = ["bold"])
        input()
    
    # Mostrar estadísticas
    if seleccionMenu == 2:
        opcionEstadistica = -1
        while opcionEstadistica != 0:
            clientes_db = pd.read_csv("clients_database.csv", delimiter = ",")
            cursos_db = pd.read_csv("courses_database.csv", delimiter = ",")
            os.system("clear")
            os.system("cls")
            cprint("MOSTRAR ESTADÍSTICAS", "yellow", attrs = ["bold"])
            print("0. Salir\n1. Cantidad de personas inscritas por cada curso\n2. Cantidad de cursos vendidos por cada vendedor\n3. Porcentaje de cursos vendidos hasta la fecha en total")
            opcionEstadistica = validarSeleccionMenu("¿Qué estadística desea mostrar? ")
            
            # Cantidad de personas inscritas por curso
            if opcionEstadistica == 1:
                # Aquí se contrastan los cursos disponibles con la lectura de la base de datos de los clientes inscritos en cada uno de ellos separando cada curso por un ", " y en caso de coincidencia, se aumenta su número
                cantidadCursosComprados = []
                for index1, value1 in enumerate(cursos_db.curso.values):
                    cantidadCursosComprados.append(str(0) + "_" + str(value1))
                    contador = 0
                    for value2 in clientes_db.curso.values:
                        value2 = value2.split(", ")
                        for value3 in value2:
                            if value3 == value1:
                                contador += 1
                                cantidadCursosComprados[index1] = str(contador) + "_" + str(value1)

                # Separamos la cantidad de cursos de sus nombres por un "_" añadido anteriormente
                cantidad = []
                nombre = []
                for value in cantidadCursosComprados:
                    value = value.split("_")
                    cantidad.append(int(value[0]))
                    nombre.append(value[1])

                # Preparamos los datos para la creación de un nuevo Data Frame y así facilitar el despliegue de una gráfica
                datos = {
                    "curso": nombre,
                    "cantidad": cantidad
                }

                grafica = DataFrame(datos, columns = ["curso", "cantidad"])
                # Punto importante: acá se ordenan los datos de mayor a menor.
                grafica = grafica.sort_values("cantidad", ascending = False)
                grafica.plot(x = "curso", y = "cantidad", kind = "bar")
                plt.show()
                continue

            # Cantidad de cursos vendidos por cada vendedor
            if opcionEstadistica == 2:
                # Acá se anota el nombre del vendedor y luego se buscan celdas con ese nombre para saber cuántos cursos ha vendido basándonos en las , que pueden haber dentro de ellos
                cantidadCursosVendedor = []
                for index1, value1 in enumerate(clientes_db.vendedor.values):
                    contador = 0
                    cantidadCursosVendedor.append(str(0) + "_" + str(value1))
                    for index2, value2 in enumerate(clientes_db.curso.values):
                        if index1 == index2:
                            contador += value2.count(",") + 1
                            cantidadCursosVendedor[index1] = str(contador) + "_" + str(value1)
                
                # Se separa el nombre del vendedor con el número de cursos que ha vendido gracias a un "_" que se añadió anteriormente
                asesor = []
                cantidad = []
                for value in cantidadCursosVendedor:
                    value = value.split("_")
                    cantidad.append(int(value[0]))
                    asesor.append(value[1].capitalize())
                
                datos = {
                    "vendedor": asesor,
                    "cantidad": cantidad
                }

                if len(asesor) != 0 and len(cantidad) != 0:
                    grafica = DataFrame(datos, columns = ["vendedor", "cantidad"])
                    grafica.plot(x = "vendedor", y = "cantidad", kind = "bar")
                    plt.show()
                else:
                    print("ADVERTENCIA: No hay ningún curso vendido hasta la fecha.")
                    input()
                continue

            # Porcentaje de cursos vendidos hasta la fecha
            if opcionEstadistica == 3:
                # Se obtienen los cursos disponibles y luego en la base de datos de clientes se buscan coincidencias del actual curso y se aumenta su número para calcualar posteriormente un total
                cantidadCursosComprados = []
                for index1, value1 in enumerate(cursos_db.curso.values):
                    cantidadCursosComprados.append(str(0) + "_" + str(value1))
                    contador = 0
                    for value2 in clientes_db.curso.values:
                        value2 = value2.split(", ")
                        for value3 in value2:
                            if value3 == value1:
                                contador += 1
                                cantidadCursosComprados[index1] = str(contador) + "_" + str(value1)                

                cantidad = []
                nombre = []
                for value in cantidadCursosComprados:
                    value = value.split("_")
                    cantidad.append(int(value[0]))
                    nombre.append(value[1])

                cantidadCursosTotal = 0
                for value in clientes_db.curso.values:
                        cantidadCursosTotal += value.count(",") + 1

                if cantidadCursosTotal != 0:
                    # Se presenta la gráfica y se usa el atributo autopct para mostrar los porcentajes de cada dato
                    plt.pie(cantidad, labels = nombre, autopct = "%2.2f%%")
                    plt.show()
                else:
                    print("ADVERTENCIA: No hay ningún curso vendido hasta la fecha.")
                    input()
                continue

    # Agregar más cursos
    if seleccionMenu == 3:
        clientes_db = pd.read_csv("clients_database.csv", delimiter = ",")
        cursos_db = pd.read_csv("courses_database.csv", delimiter = ",")        
        os.system("clear")
        os.system("cls")
        seguir = "s"
        cprint("AÑADIR MÁS CURSOS", "yellow", attrs = ["bold"])
        
        while seguir == "s":
            cursoAIngresar = ""
            precioDelCurso = 0
            nuevoCurso = []
            print()
            cursoAIngresar = validarEntradaNoVacia("Nuevo curso: ")
            nuevoCurso.append(cursoAIngresar)
            precioDelCurso = float(validarEntradaNoVacia("Precio Q: "))
            # Si el usuario ingresa un 0 como precio se pretende que desea cancelar la operación
            if precioDelCurso == 0:
                cprint("No se realizaron cambios sobre la base de datos.", "red", attrs = ["bold"])
            else:
                decision = validarEntradaNoVacia("¿Desea agregar el curso? (s|n) ").lower()
                if decision == "s":
                    nuevoCurso.append(precioDelCurso)
                    añadirFilaCSV("courses_database.csv", nuevoCurso)
                    cprint("El curso y su precio han sido añadidos con éxito a la base de datos.", "green", attrs = ["bold"])
                else:
                    cprint("No se realizaron cambios sobre la base de datos.", "red", attrs = ["bold"])
            seguir = validarEntradaNoVacia("¿Desea continuar agregando nuevos cursos (s|n): ").lower()