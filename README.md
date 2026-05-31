<<<<<<< HEAD
# Gestor de contrasenas local
=======
# VaultPassword - Gestor de Contraseñas Local

VaultPassword es una aplicación de escritorio diseñada para almacenar y gestionar credenciales de forma local. Implementa una arquitectura separada (Frontend/Backend) utilizando cifrado de grado militar para proteger la información sensible en una base de datos persistente.

## Características principales
- **Cifrado Simétrico:** Utiliza la librería `cryptography` (Fernet) para asegurar que las contraseñas se almacenen como objetos binarios (BLOB) ilegibles.
- **Base de Datos Local:** Implementación de `SQLite` nativo mediante consultas parametrizadas para evitar inyección SQL.
- **Gestión Segura del Portapapeles:** La interfaz oculta visualmente las contraseñas y permite copiarlas directamente a la memoria del sistema para evitar exposición.
- **Ciclo CRUD Completo:** Permite crear, leer, actualizar y eliminar registros de forma segura.
- **UI Minimalista:** Interfaz plana construida con `CustomTkinter` enfocada en la usabilidad.

## Tecnologías utilizadas
- Python 3.x
- `sqlite3` (Base de Datos)
- `cryptography` (Seguridad)
- `CustomTkinter` (Frontend)

## Instalación
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/joaquinmedinamor-max/VaultPassword.git](https://github.com/joaquinmedinamor-max/VaultPassword.git)
>>>>>>> 281bf95 (VaultPassword)
