import os
import sys
from cryptography.fernet import Fernet
# Nota: La verificación de la USB es simulada leyendo un archivo clave del directorio 'keys'.

# --- CONFIGURACIÓN Y RUTAS ---
# Simula la ruta de la USB
USB_PATH = "./keys" 
USB_TOKEN_FILE = "usb_key_id.txt"
MASTER_KEY_FILE = "master_key.fernet"
TARGET_FILE = "data.txt"
ENCRYPTED_FILE = TARGET_FILE + ".enc"

# --- FUNCIONES CLAVE ---

def get_usb_key():
    """Verifica si la llave USB y su token están presentes."""
    try:
        with open(os.path.join(USB_PATH, USB_TOKEN_FILE), 'rb') as f:
            return f.read() # Devuelve el token (simulación de verificación)
    except FileNotFoundError:
        return None

def load_fernet_key():
    """Carga la Clave Maestra si la USB está presente."""
    if not get_usb_key():
        print("❌ ERROR: Llave de acceso (USB) no detectada.")
        return None
        
    try:
        # Se asume que la MASTER_KEY está guardada y el token USB garantiza el acceso.
        with open(os.path.join(USB_PATH, MASTER_KEY_FILE), 'rb') as f:
            MASTER_KEY = f.read()
            return Fernet(MASTER_KEY)
    except FileNotFoundError:
        print("❌ ERROR: Archivo de clave maestra no encontrado. Use 'init'.")
        return None

def process_file(action):
    """Cifra o descifra el archivo según la acción."""
    fernet = load_fernet_key()
    if not fernet:
        return

    input_path = TARGET_FILE if action == 'encrypt' else ENCRYPTED_FILE
    output_path = ENCRYPTED_FILE if action == 'encrypt' else TARGET_FILE
    
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
            
        processed_data = fernet.encrypt(data) if action == 'encrypt' else fernet.decrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(processed_data)
            
        os.remove(input_path)
        print(f"✅ Archivo {'Cifrado' if action == 'encrypt' else 'Descifrado'} exitosamente.")
        
    except FileNotFoundError:
        print(f"❌ ERROR: El archivo de entrada ({input_path}) no existe.")
    except Exception as e:
        print(f"❌ FALLO: No se pudo completar la operación. {e}")

# --- MANEJADOR DE COMANDOS ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python access_script.py [init | encrypt | decrypt | recover]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "init":
        # 1. Crear Token USB (simulado)
        if not os.path.exists(USB_PATH): os.makedirs(USB_PATH)
        if not os.path.exists(os.path.join(USB_PATH, USB_TOKEN_FILE)):
            with open(os.path.join(USB_PATH, USB_TOKEN_FILE), 'wb') as f:
                f.write(b"USB_TOKEN_12345") 
        # 2. Generar y Guardar Clave Maestra
        MASTER_KEY = Fernet.generate_key()
        with open(os.path.join(USB_PATH, MASTER_KEY_FILE), 'wb') as f:
            f.write(MASTER_KEY)
        print("✅ Sistema Inicializado. Llave Maestra y Token Creados.")
        
    elif command == "encrypt":
        process_file('encrypt')
            
    elif command == "decrypt":
        process_file('decrypt')

    elif command == "recover":
        # Simula la generación de llave copiando el token
        if get_usb_key():
            NEW_USB_PATH = "./recovery_keys"
            if not os.path.exists(NEW_USB_PATH): os.makedirs(NEW_USB_PATH)
            
            with open(os.path.join(NEW_USB_PATH, USB_TOKEN_FILE), 'wb') as f:
                f.write(get_usb_key())
            print(f"🔑 Llave de Recuperación CREADA en: {NEW_USB_PATH}/")
        else:
            print("❌ ACCESO DENEGADO: Necesita la llave original para crear una de recuperación.")
            
    else:
        print("Comando no reconocido.")