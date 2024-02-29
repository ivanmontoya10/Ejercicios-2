import json
import hashlib
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import os 

next_id = 1
clave_maestra_file = 'clave_maestra.key'

def obtener_datos_registro():
    global next_id  
    email = input("Ingrese el correo del usuario: ").strip()
    password = input("Ingrese la contraseña del usuario: ").strip()
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    nuevo_id = next_id
    next_id += 1
    
    return {
        "ID": nuevo_id,
        "Email": email,
        "Password": hashed_password,
        "Cuentas": []
    }

def cargar_usuarios_desde_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Se produjo un error al cargar los usuarios: {str(e)}")
        return []

def guardar_usuarios_en_json(usuarios, nombre_archivo):
    try:
        with open(nombre_archivo, 'w') as archivo:
            json.dump(usuarios, archivo, indent=4)
    except Exception as e:
        print(f"Se produjo un error al guardar los usuarios: {str(e)}")

def generar_o_cargar_clave_maestra():
    if os.path.exists(clave_maestra_file):
        with open(clave_maestra_file, 'rb') as f:
            clave = f.read()
    else:
        clave = Fernet.generate_key()
        with open(clave_maestra_file, 'wb') as f:
            f.write(clave)
    return clave

clave_maestra = generar_o_cargar_clave_maestra()

# Función para encriptar una cadena de texto
def encriptar(texto, clave):
    f = Fernet(clave)
    return f.encrypt(texto.encode()).decode()

# Función para desencriptar una cadena de texto
def desencriptar(texto_encriptado, clave):
    f = Fernet(clave)
    try:
        return f.decrypt(texto_encriptado.encode()).decode()
    except InvalidToken:
        print("Error: La clave no es válida para desencriptar.")
        return None

# Función para registrar un nuevo usuario
def registrar_usuario(usuarios):
    global next_id
    email = input("Ingrese el correo del usuario: ").strip()
    password = input("Ingrese la contraseña del usuario: ").strip()
    hashed_password = encriptar(password, clave_maestra)
    nuevo_id = next_id  # Obtener el próximo ID
    next_id += 1

    nuevo_usuario = {
        "ID": nuevo_id,
        "Email": email,
        "Password": hashed_password,
        "Cuentas": []
    }
    usuarios.append(nuevo_usuario)
    guardar_usuarios_en_json(usuarios, 'usuarios.json')
    return nuevo_usuario

# Función para iniciar sesión
def iniciar_sesion(usuarios):
    email = input("Ingrese el correo del usuario: ").strip()
    password = input("Ingrese la contraseña del usuario: ").strip()

    for usuario in usuarios:
        if usuario["Email"] == email and desencriptar(usuario["Password"], clave_maestra) == password:
            return usuario

    print("Credenciales incorrectas. Por favor, verifique que sean las credenciales correctas.")
    return None

# Función para agregar una cuenta
def agregar_cuenta(usuario):
    sitio = input("Ingrese el link del sitio web: ")
    usuario_cuenta = input("Ingrese el nombre de usuario: ")
    contraseña = input("Ingrese la contraseña: ")
    descripcion = input("Ingrese una descripción: ")

    nueva_cuenta = {
        "Sitio": encriptar(sitio, clave_maestra),
        "Usuario": encriptar(usuario_cuenta, clave_maestra),
        "Password": encriptar(contraseña, clave_maestra),
        "Descripción": encriptar(descripcion, clave_maestra)
    }

    usuario["Cuentas"].append(nueva_cuenta)
    print("Cuenta agregada con éxito.")

# Función para ver cuentas
def ver_cuentas(usuario):
    cuentas = usuario.get("Cuentas", [])

    if not cuentas:
        print("No hay cuentas registradas.")
    else:
        for i, cuenta in enumerate(cuentas, start=1):
            sitio = desencriptar(cuenta["Sitio"], clave_maestra)
            usuario_cuenta = desencriptar(cuenta["Usuario"], clave_maestra)
            contraseña = desencriptar(cuenta["Password"], clave_maestra)
            descripcion = desencriptar(cuenta["Descripción"], clave_maestra)

            print(f"\nCuenta {i}:")
            print(f"Sitio: {sitio}")
            print(f"Usuario: {usuario_cuenta}")
            print(f"Password: {contraseña}")
            print(f"Descripción: {descripcion}")

# Función para editar campos de una cuenta
def editar_cuenta(usuario):
    ver_cuentas(usuario)  # Muestra las cuentas para que el usuario elija cuál editar

    cuentas = usuario.get("Cuentas", [])
    if not cuentas:
        print("No hay cuentas para editar.")
        return

    try:
        cuenta_idx = int(input("Seleccione el número de la cuenta que desea editar: ")) - 1
        if 0 <= cuenta_idx < len(cuentas):
            cuenta = cuentas[cuenta_idx]

            # Puedes agregar opciones para editar diferentes campos (Sitio, Usuario, Contraseña, Descripción)
            campo_a_editar = input("Seleccione el campo que desea editar (Sitio/Usuario/Contraseña/Descripción): ")

            if campo_a_editar.lower() == "sitio":
                nuevo_sitio = input("Ingrese el nuevo sitio web: ")
                cuenta["Sitio"] = encriptar(nuevo_sitio, clave_maestra)
            elif campo_a_editar.lower() == "usuario":
                nuevo_usuario = input("Ingrese el nuevo nombre de usuario: ")
                cuenta["Usuario"] = encriptar(nuevo_usuario, clave_maestra)
            elif campo_a_editar.lower() == "contraseña":
                nueva_contraseña = input("Ingrese la nueva contraseña: ")
                cuenta["Password"] = encriptar(nueva_contraseña, clave_maestra)
            elif campo_a_editar.lower() == "descripción":
                nueva_descripción = input("Ingrese la nueva descripción: ")
                cuenta["Descripción"] = encriptar(nueva_descripción, clave_maestra)
            else:
                print("Campo no válido. Por favor, seleccione un campo válido.")
        else:
            print("Número de cuenta no válido.")
    except ValueError:
        print("Entrada no válida. Debe ingresar un número.")

# Función para eliminar una cuenta
def eliminar_cuenta(usuario):
    ver_cuentas(usuario)  # Muestra las cuentas para que el usuario elija cuál eliminar

    cuentas = usuario.get("Cuentas", [])
    if not cuentas:
        print("No hay cuentas para eliminar.")
        return

    try:
        cuenta_idx = int(input("Seleccione el número de la cuenta que desea eliminar: ")) - 1
        if 0 <= cuenta_idx < len(cuentas):
            cuenta_eliminada = cuentas.pop(cuenta_idx)
            print(f"La cuenta {cuenta_idx + 1} ha sido eliminada.")
        else:
            print("Número de cuenta no válido.")
    except ValueError:
        print("Entrada no válida. Debe ingresar un número.")

# Función principal
def main():
    usuarios = []
    usuario_actual = None

    while True:
        print("\nMenú Principal:")
        print("1. Registrar usuario nuevo")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción (1/2/3): ")

        if opcion == '1':
            nuevo_usuario = registrar_usuario(usuarios)
            print(f"Usuario {nuevo_usuario['Email']} registrado con éxito.")
        elif opcion == '2':
            usuario_actual = iniciar_sesion(usuarios)
            if usuario_actual:
                print(f"Bienvenido, {usuario_actual['Email']}!")
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")

        while usuario_actual:
            print("\nMenú de Usuario:")
            print("1. Agregar cuenta")
            print("2. Ver cuentas")
            print("3. Editar cuenta")
            print("4. Eliminar cuenta")
            print("5. Salir de sesión")

            opcion = input("Seleccione una opción (1/2/3/4/5): ")

            if opcion == '1':
                agregar_cuenta(usuario_actual)
                guardar_usuarios_en_json(usuarios, 'usuarios.json')
            elif opcion == '2':
                ver_cuentas(usuario_actual)
            elif opcion == '3':
                editar_cuenta(usuario_actual)
                guardar_usuarios_en_json(usuarios, 'usuarios.json')
            elif opcion == '4':
                eliminar_cuenta(usuario_actual)
                guardar_usuarios_en_json(usuarios, 'usuarios.json')
            elif opcion == '5':
                usuario_actual = None
                print("Sesión finalizada.")
            else:
                print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    print("¡Bienvenido!")
    main()