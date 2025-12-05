#!/bin/bash
USER_NAME="andresmmc"
USB_UUID="4E21-0000"
MOUNT_PATH="/mnt/Ventoy"
LLAVE="$MOUNT_PATH/llave.key"

# Múltiples directorios: "Origen_Cifrado:Destino_Desencriptado"
DIRECTORIOS=(
    "$HOME/.docs_cifrados:$HOME/Documentos"
    "$HOME/.imgs_cifrados:$HOME/Imágenes"
    "$HOME/.archivos_cifrados:$HOME/Escritorio/Archivos_Seguros"
)

while true; do
    sudo mount -U "$USB_UUID" "$MOUNT_PATH" 2>/dev/null

    if [ -f "$LLAVE" ]; then
        for dir in "${DIRECTORIOS[@]}"; do
            CIPHER="${dir%%:*}"
            PLAIN="${dir##*:}"
            if [ -d "$CIPHER" ] && ! mountpoint -q "$PLAIN"; then
                mkdir -p "$PLAIN"
                gocryptfs -passfile "$LLAVE" "$CIPHER" "$PLAIN"
            fi
        done
        # Desbloqueo inmediato
        sudo /usr/bin/loginctl unlock-session
        sudo /usr/bin/pkill -u "$USER_NAME" -9 betterlockscreen 2>/dev/null
    else
        # Bloqueo y cierre
        for dir in "${DIRECTORIOS[@]}"; do
            PLAIN="${dir##*:}"
            [ -d "$PLAIN" ] && fusermount -u "$PLAIN" 2>/dev/null
        done
        sudo umount "$MOUNT_PATH" 2>/dev/null
        if ! pgrep -x "betterlockscreen" >/dev/null; then
            betterlockscreen -l &
        fi
    fi
    sleep 2
done
