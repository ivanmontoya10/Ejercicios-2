def guardar_en_archivo(nombre_archivo, texto):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(texto)
        print("El texto ha sido guardado correctamente")

if __name__ == "__main__":
    texto = input("Por favor, ingresa el texto que deseas guardar en el archivo: ")
    nombre_archivo = input("Ingresa el nombre del archivo: ")
    guardar_en_archivo(nombre_archivo, texto)