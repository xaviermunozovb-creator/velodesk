#!/usr/bin/env bash
# instalar-islatortuga.sh — Servidor de conexión de VeloDesk (hbbs + hbbr) en un
# servidor que YA tiene otra cosa corriendo (el bot de trading en /opt/turtle).
#
# Diferencias con instalar-servidor.sh (el genérico):
#   - Sin Docker: no instala ningún demonio nuevo como root ni toca iptables.
#   - Corre como el usuario de sistema `velodesk`, sin shell y sin privilegios.
#   - systemd lo encierra: solo puede escribir en su carpeta de datos, no ve /home
#     y /opt/turtle le es inaccesible aunque alguien lo reventara.
#   - Límite de 256 MB de RAM y medio núcleo: nunca puede quitarle recursos al bot.
#   - Abre solo los puertos de la app nativa (TCP 21115-21117, UDP 21116).
#   - Antes y después fotografía el cron, el firewall y /opt/turtle y comprueba
#     que son idénticos. Si algo hubiera cambiado, lo diría.
#
# Ejecutar como root:   bash /root/instalar-islatortuga.sh
# Deshacer todo:        bash /root/desinstalar-islatortuga.sh
set -euo pipefail

VER="1.1.16"
DIR=/opt/velodesk-server
USR=velodesk
BOT=/opt/turtle

[ "$(id -u)" -eq 0 ] || { echo "Ejecuta este script como root." >&2; exit 1; }
# Huellas SHA-256 de los zips oficiales de la versión $VER, calculadas el 29-10-2026.
case "$(uname -m)" in
  x86_64)  ARCH=amd64;   ZIP_SHA="0565c41affe6c3f409b0bddfaf5a24ccbf3f64f5f8e3fec250b69a0d5f6bdbcf" ;;
  aarch64) ARCH=arm64v8; ZIP_SHA="6a4ae3c5ca257a4278ded72fd17eb2ca4eeb0356a5425e63a3e7fcb0ec6c155c" ;;
  *) echo "Arquitectura no prevista: $(uname -m)." >&2; exit 1 ;;
esac
ZIP_URL="https://github.com/rustdesk/rustdesk-server/releases/download/${VER}/rustdesk-server-linux-${ARCH}.zip"
command -v systemctl >/dev/null || { echo "Hace falta systemd." >&2; exit 1; }

# ── 0. Fotografía del estado del bot ANTES de tocar nada ─────────────────────
foto() {
  {
    echo "## crontab root"; crontab -l 2>/dev/null || echo "(sin crontab)"
    # sin numerar: al añadir reglas ufw renumera las demás y parecería un cambio
    echo "## ufw";          ufw status 2>/dev/null || echo "(ufw no disponible)"
    echo "## $BOT";         [ -d "$BOT" ] && find "$BOT" -maxdepth 1 -printf '%M %u %s %p\n' | sort || echo "(no existe)"
    # packagekit se despierta solo al entrar por SSH (update-notifier): no cuenta
    echo "## servicios activos"; systemctl list-units --type=service --state=running --no-legend --plain | awk '{print $1}' | grep -v -E '^(velodesk-|packagekit)' | sort
  } 2>/dev/null
}
ANTES=$(mktemp); foto > "$ANTES"
echo "==> Estado del bot fotografiado (cron, firewall, $BOT, servicios)."

# ── 1. Sin paquetes nuevos: curl ya está, y el zip lo abre el python3 del bot ─
command -v curl >/dev/null    || { echo "Falta curl: apt-get install -y curl" >&2; exit 1; }
command -v python3 >/dev/null || { echo "Falta python3 (lo usa el bot; raro)." >&2; exit 1; }

# ── 2. Usuario de sistema sin shell ───────────────────────────────────────────
if ! id -u "$USR" >/dev/null 2>&1; then
  useradd --system --home-dir "$DIR" --no-create-home --shell /usr/sbin/nologin "$USR"
  echo "==> Usuario $USR creado (sin shell, sin contraseña)."
fi

# ── 3. Binarios verificados ──────────────────────────────────────────────────
echo "==> Descargando rustdesk-server $VER ($ARCH)"
TMP=$(mktemp -d)
curl -fsSL "$ZIP_URL" -o "$TMP/rs.zip"
echo "$ZIP_SHA  $TMP/rs.zip" | sha256sum -c --quiet || { echo "La suma SHA-256 del zip no coincide: NO instalo." >&2; exit 1; }
python3 -m zipfile -e "$TMP/rs.zip" "$TMP"
mkdir -p "$DIR/bin" "$DIR/data"
install -o root -g root -m 0755 "$TMP/$ARCH/hbbs" "$TMP/$ARCH/hbbr" "$DIR/bin/"
chown -R "$USR:$USR" "$DIR/data"; chmod 700 "$DIR/data"
rm -rf "$TMP"

# ── 4. Servicios systemd encerrados ──────────────────────────────────────────
unidad() {  # $1 nombre corto, $2 descripción, $3 comando, $4 dependencias extra
cat > "/etc/systemd/system/velodesk-$1.service" <<EOF
[Unit]
Description=VeloDesk $2
After=network-online.target $4
Wants=network-online.target
$( [ -n "$4" ] && echo "Requires=$4" )

[Service]
User=$USR
Group=$USR
WorkingDirectory=$DIR/data
ExecStart=$DIR/bin/$3
Restart=always
RestartSec=5
Nice=10

# Recursos: nunca por encima de esto, pase lo que pase.
MemoryMax=256M
CPUQuota=50%
TasksMax=256

# Aislamiento: solo escribe en su carpeta; el bot le es invisible.
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=$DIR/data
InaccessiblePaths=-$BOT
PrivateTmp=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectKernelLogs=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictSUIDSGID=yes
RestrictRealtime=yes
RestrictNamespaces=yes
LockPersonality=yes
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
CapabilityBoundingSet=
AmbientCapabilities=
SystemCallArchitectures=native
SystemCallFilter=@system-service

[Install]
WantedBy=multi-user.target
EOF
}
unidad hbbs "servidor de ID (hbbs)"   "hbbs -k _" ""
unidad hbbr "servidor relé (hbbr)"    "hbbr -k _" "velodesk-hbbs.service"
systemctl daemon-reload

# ── 5. Firewall: solo añadir reglas, nunca resetear ni cambiar el estado ─────
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  ufw allow 21115:21117/tcp comment 'VeloDesk' >/dev/null
  ufw allow 21116/udp        comment 'VeloDesk' >/dev/null
  echo "==> ufw: añadidas TCP 21115-21117 y UDP 21116. El resto sigue igual."
else
  echo "AVISO: ufw no está activo; no lo toco. Abre TCP 21115-21117 y UDP 21116 donde corresponda." >&2
fi

# ── 6. Arrancar: hbbs genera la clave, hbbr la espera ────────────────────────
systemctl enable --now velodesk-hbbs.service >/dev/null
for _ in $(seq 1 30); do [ -s "$DIR/data/id_ed25519.pub" ] && break; sleep 1; done
[ -s "$DIR/data/id_ed25519.pub" ] || { echo "hbbs no generó la clave. Mira: journalctl -u velodesk-hbbs" >&2; exit 1; }
systemctl enable --now velodesk-hbbr.service >/dev/null
sleep 2

# ── 7. Comprobación: el bot no ha cambiado ───────────────────────────────────
DESPUES=$(mktemp); foto > "$DESPUES"
# Las dos reglas nuevas de ufw son el único cambio esperado.
if diff <(grep -v VeloDesk "$ANTES") <(grep -v VeloDesk "$DESPUES") >/dev/null; then
  BOT_OK="idénticos antes y después: cron, firewall (salvo las 2 reglas nuevas), $BOT y servicios"
else
  BOT_OK="ATENCIÓN, hay diferencias; revísalas:"$'\n'"$(diff "$ANTES" "$DESPUES" || true)"
fi
rm -f "$ANTES" "$DESPUES"

IP=$(curl -fsS -4 https://api.ipify.org 2>/dev/null || hostname -I | awk '{print $1}')
echo
echo "=============================================================="
echo " Servidor VeloDesk instalado en IslaTortuga."
echo
echo " Servidor ID / Relé :  $IP"
echo " Key (clave pública):  $(cat "$DIR/data/id_ed25519.pub")"
echo
echo " Servicios: $(systemctl is-active velodesk-hbbs) (hbbs)  $(systemctl is-active velodesk-hbbr) (hbbr)"
echo " Escuchando:"; ss -tulnp 2>/dev/null | awk '/:2111[5-7] /{print "   " $1, $5}' | sort -u
echo
echo " Bot: $BOT_OK"
echo
echo " Si en el panel de Hetzner hay un 'Firewall' asignado a esta máquina,"
echo " abre ahí también TCP 21115-21117 y UDP 21116 (ufw no manda sobre él)."
echo " Registro: journalctl -u velodesk-hbbs -u velodesk-hbbr -f"
echo "=============================================================="
