#!/bin/bash

USER_NAME="andresmmc"
USB_UUID="4E21-0000"
MOUNT_PATH="/mnt/Ventoy"
LLAVE="$MOUNT_PATH/llave.key"
CIPHER_DIR="$HOME/.archivos_cifrados"
PLAIN_DIR="$HOME/Escritorio/Archivos_Seguros"

while true; do
    # Intento de montaje rápido
    sudo mount -U "$USB_UUID" "$MOUNT_PATH" 2>/dev/null

    if [ -f "$LLAVE" ]; then
        if ! mountpoint -q "$PLAIN_DIR"; then
            # MOMENTO DE DESENCRIPTACIÓN:
            # Aquí es cuando tus archivos se vuelven legibles en la carpeta 'Archivos_Seguros'
            gocryptfs -passfile "$LLAVE" "$CIPHER_DIR" "$PLAIN_DIR"

            # DESBLOQUEO INMEDIATO:
            # Estos comandos fuerzan la desaparición de la pantalla de bloqueo
            sudo /usr/bin/loginctl unlock-session
            sudo /usr/bin/pkill -u "$USER_NAME" -9 betterlockscreen 2>/dev/null
            sudo /usr/bin/pkill -u "$USER_NAME" -9 i3lock 2>/dev/null
        fi
    else
        # BLOQUEO Y PROTECCIÓN:
        if mountpoint -q "$PLAIN_DIR"; then
            fusermount -u "$PLAIN_DIR"
            sudo umount "$MOUNT_PATH" 2>/dev/null
        fi
        # Lanza el candado si la USB no está
        if ! pgrep -x "betterlockscreen" >/dev/null && ! pgrep -x "i3lock" >/dev/null; then
            betterlockscreen -l &
        fi
    fi
    sleep 1 # Revisión cada 1 segundo para mayor velocidad
done
