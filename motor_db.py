import sqlite3
from cryptography.fernet import Fernet
import os

# 1. GESTIÓN DE LA LLAVE DE CIFRADO
def obtener_llave():
    """Genera una llave maestra si no existe, o la carga si ya está creada."""
    ruta_llave = "llave_maestra.key"
    if not os.path.exists(ruta_llave):
        llave = Fernet.generate_key()
        with open(ruta_llave, "wb") as archivo_llave:
            archivo_llave.write(llave)
        print("[*] Nueva llave maestra generada con éxito.")
    with open(ruta_llave, "rb") as archivo_llave:
        return archivo_llave.read()

# Instanciamos el motor de cifrado usando la llave
LLAVE_MAESTRA = obtener_llave()
cifrador = Fernet(LLAVE_MAESTRA)

# 2. CREACIÓN DE LA BASE DE DATOS 
def inicializar_base_datos():
    """Crea el archivo SQLite y la tabla si no existen."""
    conexion = sqlite3.connect("vaultx.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credenciales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sitio_web TEXT NOT NULL,
            usuario TEXT NOT NULL,
            password_cifrado BLOB NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# 3. LÓGICA: GUARDAR Y RECUPERAR 
def guardar_credencial(sitio_web, usuario, password_plano):
    """Cifra la contraseña y guarda todo el registro en la base de datos."""
    try:
        # Convertimos la contraseña plana a bytes y la ciframos
        password_bytes = password_plano.encode('utf-8')
        password_cifrado = cifrador.encrypt(password_bytes)
        
        # Conectamos a la BD e insertamos
        conexion = sqlite3.connect("vaultx.db")
        cursor = conexion.cursor()
        
        # Usamos '?' (consultas parametrizadas) para evitar inyecciones SQL
        cursor.execute('''
            INSERT INTO credenciales (sitio_web, usuario, password_cifrado) 
            VALUES (?, ?, ?)
        ''', (sitio_web, usuario, password_cifrado))
        
        conexion.commit()
        conexion.close()
        return True, "Credencial guardada con éxito."
    except Exception as e:
        return False, f"Error al guardar: {e}"

def obtener_credenciales():
    """Recupera todos los registros y descifra las contraseñas."""
    try:
        conexion = sqlite3.connect("vaultx.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT id, sitio_web, usuario, password_cifrado FROM credenciales")
        registros_crudos = cursor.fetchall()
        conexion.close()
        
        registros_descifrados = []
        for registro in registros_crudos:
            id_registro, sitio_web, usuario, password_cifrado = registro
            
            # El núcleo del programa: DESCIFRAR la información que sacamos de la BD
            password_descifrado = cifrador.decrypt(password_cifrado).decode('utf-8')
            
            # Guardamos el resultado limpio en una nueva lista
            registros_descifrados.append({
                "id": id_registro,
                "sitio_web": sitio_web,
                "usuario": usuario,
                "password": password_descifrado
            })
            
        return True, registros_descifrados
    except Exception as e:
        return False, f"Error al recuperar datos: {e}"

def eliminar_credencial(id_registro):
    """Elimina un registro específico de la base de datos de forma segura usando su ID."""
    try:
        conexion = sqlite3.connect("vaultx.db")
        cursor = conexion.cursor()
        
        # Ejecutamos el borrado apuntando exclusivamente al ID único
        cursor.execute("DELETE FROM credenciales WHERE id = ?", (id_registro,))
        
        conexion.commit()
        conexion.close()
        return True, "Credencial eliminada con éxito."
    except Exception as e:
        return False, f"Error al eliminar: {e}"
    
def actualizar_credencial(id_registro, nuevo_sitio, nuevo_usuario, nuevo_password_plano):
    """Cifra la nueva contraseña y actualiza un registro existente."""
    try:
        # 1. Volvemos a cifrar la nueva contraseña
        password_bytes = nuevo_password_plano.encode('utf-8')
        password_cifrado = cifrador.encrypt(password_bytes)
        
        conexion = sqlite3.connect("vaultx.db")
        cursor = conexion.cursor()
        
        # 2. Ejecutamos el UPDATE apuntando al ID
        cursor.execute('''
            UPDATE credenciales 
            SET sitio_web = ?, usuario = ?, password_cifrado = ?
            WHERE id = ?
        ''', (nuevo_sitio, nuevo_usuario, password_cifrado, id_registro))
        
        conexion.commit()
        conexion.close()
        return True, "Credencial actualizada con éxito."
    except Exception as e:
        return False, f"Error al actualizar: {e}"

# Bloque de prueba
if __name__ == "__main__":
    inicializar_base_datos()
    
    print("\n--- PRUEBA DE MOTOR VAULTX ---")
    # 1. Guardamos un dato de prueba
    exito, msj = guardar_credencial("github.com", "joaquinmedinamor-max", "MiSuperPassword123!")
    print(msj)
    
    # 2. Recuperamos los datos para comprobar que todo funcionó
    exito, datos = obtener_credenciales()
    if exito:
        print("\nDatos recuperados de la BD:")
        for dato in datos:
            print(f"Sitio: {dato['sitio_web']} | Usuario: {dato['usuario']} | Clave: {dato['password']}")