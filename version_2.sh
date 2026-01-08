#!/bin/bash

# --- CONFIGURACIÓN SEGÚN TUS CAPTURAS ---
USER_NAME="andresmmc"
USB_UUID="4E21-0000"              # Tu UUID confirmado
MOUNT_PATH="/mnt/Ventoy"          # Tu punto de montaje confirmado
LLAVE="$MOUNT_PATH/llave.key"

# LISTA DE DIRECTORIOS (Añade todos los que quieras proteger)
DIRECTORIOS=(
    "$HOME/.docs_cifrados:$HOME/Documentos"
    "$HOME/.imgs_cifrados:$HOME/Imágenes"
    "$HOME/.archivos_cifrados:$HOME/Escritorio/Archivos_Seguros"
)

# ASEGURAR QUE LAS CARPETAS EXISTAN
sudo mkdir -p "$MOUNT_PATH"
for dir in "${DIRECTORIOS[@]}"; do
    mkdir -p "${dir%%:*}" "${dir##*:}"
done

while true; do
    # 1. Intentar montar la USB
    sudo mount -U "$USB_UUID" "$MOUNT_PATH" 2>/dev/null

    if [ -f "$LLAVE" ]; then
        # --- CASO: USB DETECTADA (DESENCRIPTAR Y DESBLOQUEAR) ---
        for dir in "${DIRECTORIOS[@]}"; do
            CIPHER="${dir%%:*}"
            PLAIN="${dir##*:}"

            if ! mountpoint -q "$PLAIN"; then
                # Desencriptación masiva usando la llave de la USB
                gocryptfs -passfile "$LLAVE" "$CIPHER" "$PLAIN" 2>/dev/null
            fi
        done

        # --- DESBLOQUEO INMEDIATO ---
        # Forzamos al sistema a liberar la sesión
        sudo /usr/bin/loginctl unlock-session

        # Matamos procesos de bloqueo específicos de Archcraft/XFCE
        sudo /usr/bin/pkill -u "$USER_NAME" -9 xfce4-screensaver 2>/dev/null
        sudo /usr/bin/pkill -u "$USER_NAME" -9 betterlockscreen 2>/dev/null

        # Despertar monitor
        xset dpms force on 2>/dev/null

    else
        # --- CASO: USB RETIRADA (BLOQUEAR Y CIFRAR) ---
        for dir in "${DIRECTORIOS[@]}"; do
            PLAIN="${dir##*:}"
            if mountpoint -q "$PLAIN"; then
                fusermount -u "$PLAIN"
            fi
        done

        sudo umount "$MOUNT_PATH" 2>/dev/null

        # Activar bloqueo si no hay USB
        if ! pgrep -x "xfce4-screensaver" > /dev/null && ! pgrep -x "betterlockscreen" > /dev/null; then
            betterlockscreen -l &
        fi
    fi
    sleep 2
done
