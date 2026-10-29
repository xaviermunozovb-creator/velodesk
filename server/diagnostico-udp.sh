#!/usr/bin/env bash
# diagnostico-udp.sh — por qué UDP 21116 no contesta desde fuera. Solo lee.
echo "== journal (hbbs/hbbr, 25 lineas)"; journalctl -u velodesk-hbbs -u velodesk-hbbr -n 25 --no-pager
echo "== sockets UDP"; ss -ulnp
echo "== iptables INPUT (2111x)"; iptables -S INPUT | grep -E "2111[5-9]"
echo "== ufw-user-input (2111x)"; iptables -S ufw-user-input 2>/dev/null | grep -E "2111[5-9]"
echo "== ufw"; ufw status verbose | head -8
echo "== nftables?"; command -v nft >/dev/null && nft list ruleset 2>/dev/null | grep -c . || echo "sin nft"
echo "== sonda UDP local y a la IP publica"
python3 - <<'EOF'
import socket
msg = b"\x32\x0b\x0a\x09123456789"
for host in ("127.0.0.1", "46.225.99.214"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.settimeout(4)
    try:
        s.sendto(msg, (host, 21116)); print("UDP", host, "->", s.recv(64).hex())
    except Exception as e:
        print("UDP", host, "-> sin respuesta:", e)
EOF
echo "== contador de paquetes UDP 21116 recibidos (iptables -v)"
iptables -L INPUT -v -n | grep -E "udp.*2111" || echo "(sin regla con contador)"
echo "== hetzner: metadata (firewall no se ve desde dentro; solo informativo)"
curl -s -m 3 http://169.254.169.254/hetzner/v1/metadata | head -5 || true
