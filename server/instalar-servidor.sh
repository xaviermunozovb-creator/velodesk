#!/usr/bin/env bash
# Instala el servidor de conexión de VeloDesk en Ubuntu/Debian (probado con la
# capa gratuita de Oracle Cloud, Hetzner y OVH). Ejecutar como root:
#
#   curl -fsSL https://raw.githubusercontent.com/CAMBIAR-USUARIO/velodesk/master/server/instalar-servidor.sh | sudo bash
#
set -euo pipefail

DIR=/opt/velodesk-server

if [ "$(id -u)" -ne 0 ]; then
  echo "Ejecuta este script como root (sudo)." >&2
  exit 1
fi

echo "==> Instalando Docker"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker

echo "==> Creando $DIR"
mkdir -p "$DIR/data"
cat > "$DIR/docker-compose.yml" <<'EOF'
services:
  hbbs:
    image: rustdesk/rustdesk-server:latest
    container_name: velodesk-hbbs
    command: hbbs -k _
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
    depends_on:
      - hbbr
  hbbr:
    image: rustdesk/rustdesk-server:latest
    container_name: velodesk-hbbr
    command: hbbr -k _
    volumes:
      - ./data:/root
    network_mode: host
    restart: unless-stopped
EOF

echo "==> Abriendo puertos en el firewall local"
# Oracle Cloud trae reglas iptables que rechazan todo lo que no esté permitido.
for p in 21115 21116 21117 21118 21119; do
  iptables -C INPUT -p tcp --dport "$p" -j ACCEPT 2>/dev/null || iptables -I INPUT 5 -p tcp --dport "$p" -j ACCEPT
done
iptables -C INPUT -p udp --dport 21116 -j ACCEPT 2>/dev/null || iptables -I INPUT 5 -p udp --dport 21116 -j ACCEPT
if command -v netfilter-persistent >/dev/null 2>&1; then netfilter-persistent save || true; fi
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  ufw allow 21115:21119/tcp || true
  ufw allow 21116/udp || true
fi

echo "==> Arrancando el servidor"
cd "$DIR"
docker compose pull
docker compose up -d

echo "==> Esperando a que se genere la clave"
for _ in $(seq 1 30); do
  [ -s "$DIR/data/id_ed25519.pub" ] && break
  sleep 1
done

IP=$(curl -fsS -4 https://api.ipify.org 2>/dev/null || hostname -I | awk '{print $1}')
echo
echo "=============================================================="
echo " Servidor VeloDesk instalado."
echo
echo " Servidor ID / Relé :  $IP"
echo " Key (clave pública):  $(cat "$DIR/data/id_ed25519.pub")"
echo
echo " Recuerda abrir en el panel de tu proveedor (Security List):"
echo "   TCP 21115-21119 y UDP 21116"
echo
echo " En la app: Ajustes > Red > Servidor ID/Relé -> pega la IP y la Key."
echo "=============================================================="
