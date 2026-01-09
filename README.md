# Guia de Uso

================================================================
      GUÍA DE PRUEBA FINAL: SEGURIDAD USB 
================================================================

--- PASO 1: ACTIVACIÓN ---
1. Ejecute en terminal: chmod +x ~/seguridad_usb.sh
2. Inicie el script: sudo ~/seguridad_usb.sh

--- PASO 2: PRUEBA DE DESBLOQUEO INMEDIATO ---
1. Bloquee su pantalla (Super + L).
2. Retire la USB (espere a que el script detecte la ausencia).
3. Inserte la USB: La pantalla debe desaparecer sola en 1 segundo.

--- PASO 3: PRUEBA DE DESENCRIPTACIÓN MASIVA ---
1. Al insertar la USB, observe las notificaciones en el escritorio.
2. Verifique que sus carpetas 'Documentos', 'Imágenes' y 'Archivos_Seguros' 
   muestren su contenido real.

--- PASO 4: PRUEBA DE CLONACIÓN ---
1. Con la USB maestra conectada, inserte otra USB vacía.
2. Como ya creó la carpeta 'CLONAR', el script copiará la llave 
   automáticamente y borrará la carpeta tras terminar.
3. Busque la notificación de "¡Nueva llave creada!".

--- PASO 5: MANTENIMIENTO ---
* Para detener todo: sudo pkill -f seguridad_usb.sh.
* Para restaurar aplicaciones: sudo chmod +x /usr/bin/*.
================================================================
