#!/bin/bash

USER_NAME="andresmmc"
USB_UUID="4E21-0000"
MOUNT_PATH="/mnt/Ventoy"
LLAVE="$MOUNT_PATH/llave.key"

# LISTA DE DIRECTORIOS A DESENCRIPTAR (Añade aquí los que necesites)
# Formato: "Carpeta_Cifrada:Carpeta_Destino"
DIRECTORIOS=(
    "$HOME/.documentos_cifrados:$HOME/Documentos"
    "$HOME/.imagenes_cifradas:$HOME/Imágenes"
    "$HOME/.proyectos_cifrados:$HOME/Proyectos"
)

while true; do
    sudo mount -U "$USB_UUID" "$MOUNT_PATH" 2>/dev/null

    if [ -f "$LLAVE" ]; then
        # --- DESBLOQUEO Y DESENCRIPTACIÓN MASIVA ---
        for dir in "${DIRECTORIOS[@]}"; do
            CIPHER="${dir%%:*}"
            PLAIN="${dir##*:}"

            if [ -d "$CIPHER" ] && ! mountpoint -q "$PLAIN"; then
                mkdir -p "$PLAIN"
                gocryptfs -passfile "$LLAVE" "$CIPHER" "$PLAIN"
            fi
        done

        # Desbloqueo de pantalla inmediato
        sudo /usr/bin/loginctl unlock-session
        sudo /usr/bin/pkill -u "$USER_NAME" -9 betterlockscreen 2>/dev/null

    else
        # --- BLOQUEO Y CIERRE MASIVO ---
        for dir in "${DIRECTORIOS[@]}"; do
            PLAIN="${dir##*:}"
            if mountpoint -q "$PLAIN"; then
                fusermount -u "$PLAIN"
            fi
        done

        sudo umount "$MOUNT_PATH" 2>/dev/null

        if ! pgrep -x "betterlockscreen" >/dev/null; then
            betterlockscreen -l &
        fi
    fi
    sleep 2
done
