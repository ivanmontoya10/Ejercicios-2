import os
import json

def guardar_credenciales(usuario, contrasena):
    # Crear un diccionario con las credenciales
    credenciales = {"user": usuario, "password": contrasena}

    # Convertir el diccionario a formato JSON
    datos_json = json.dumps(credenciales)

    ruta_archivo = os.path.join('credenciales.txt')

    # Guardar el JSON en un archivo
    with open(ruta_archivo, 'a') as archivo:  # Cambiado a 'a' para agregar al archivo existente
        archivo.write(datos_json + '\n')  # Agregar nueva línea entre registros

def imprimir_credenciales():
    ruta_archivo = os.path.join('credenciales.txt')

    # Verificar si el archivo existe antes de intentar abrirlo
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                # Cargar el JSON de cada línea y convertirlo a diccionario
                credenciales = json.loads(linea)
                print("Usuario:", credenciales["user"])
                print("Contraseña:", credenciales["password"])
                print("----")
    else:
        print("No hay registros guardados.")

def main():
    while True:
        print("1. Registrar credenciales")
        print("2. Imprimir credenciales")
        print("3. Salir")

        opcion = input("Seleccione una opción (1, 2 o 3): ")

        if opcion == '1':
            usuario = input("Ingrese el nombre de usuario: ")
            contrasena = input("Ingrese la contraseña: ")
            guardar_credenciales(usuario, contrasena)
            print("Las credenciales se han guardado correctamente en credenciales.txt")
        elif opcion == '2':
            imprimir_credenciales()
        elif opcion == '3':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if _name_ == "_main_":
    main()