#!/usr/bin/env bash
# desinstalar-islatortuga.sh — deshace todo lo que hizo instalar-islatortuga.sh.
# No toca nada más: ni cron, ni /opt/turtle, ni el resto de reglas del firewall.
set -euo pipefail
DIR=/opt/velodesk-server
USR=velodesk
[ "$(id -u)" -eq 0 ] || { echo "Ejecuta este script como root." >&2; exit 1; }

for s in velodesk-hbbr velodesk-hbbs; do
  systemctl disable --now "$s.service" 2>/dev/null || true
  rm -f "/etc/systemd/system/$s.service"
done
systemctl daemon-reload

if command -v ufw >/dev/null 2>&1; then
  ufw delete allow 21115:21117/tcp >/dev/null 2>&1 || true
  ufw delete allow 21116/udp        >/dev/null 2>&1 || true
fi

if [ -f "$DIR/data/id_ed25519" ]; then
  cp -a "$DIR/data/id_ed25519" "$DIR/data/id_ed25519.pub" /root/ 2>/dev/null || true
  echo "Copia de la clave del servidor guardada en /root/id_ed25519(.pub) por si reinstalas."
fi
rm -rf "$DIR"
id -u "$USR" >/dev/null 2>&1 && userdel "$USR" || true
echo "VeloDesk server desinstalado. Cron, /opt/turtle y el resto del firewall no se han tocado."
