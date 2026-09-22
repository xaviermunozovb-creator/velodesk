# Servidor de conexión de VeloDesk

VeloDesk (como RustDesk) necesita dos procesos en un servidor con IP pública:

- **hbbs**: servidor de encuentro. Los equipos se registran con su ID y él les dice cómo conectarse entre sí (intenta conexión directa con hole-punching).
- **hbbr**: servidor de relé. Si la conexión directa falla, el tráfico cifrado pasa por aquí.

Ambos son software libre (AGPL-3.0) y consumen muy pocos recursos.

## Dónde alojarlo gratis

| Opción | Coste | Notas |
|---|---|---|
| Oracle Cloud "Always Free" | 0 € para siempre | Máquinas ARM de hasta 4 núcleos y 24 GB. Piden tarjeta para verificar identidad. Recomendado. |
| PC en casa siempre encendido | 0 € | Hay que abrir los puertos en el router y usar un DNS dinámico (DuckDNS). |
| VPS de pago (Hetzner, OVH, Contabo) | 3-5 €/mes | Más sencillo, no gratuito. |
| Cloudflare | no sirve | Cloudflare gratuito solo sirve páginas web y funciones HTTP; no puede escuchar en los puertos TCP/UDP que necesita el servidor. Lo usamos para la web de descargas. |

## Instalación en un clic (Ubuntu/Debian)

```bash
curl -fsSL https://raw.githubusercontent.com/CAMBIAR-USUARIO/velodesk/master/server/instalar-servidor.sh | sudo bash
```

Al terminar imprime la IP y la clave pública. Abre además en el panel del proveedor los puertos TCP 21115-21119 y UDP 21116.

## Instalación manual

```bash
mkdir -p velodesk-server && cd velodesk-server
curl -O https://raw.githubusercontent.com/CAMBIAR-USUARIO/velodesk/master/server/docker-compose.yml
docker compose up -d
cat data/id_ed25519.pub
```

## Configurar los clientes

En cada equipo: **Ajustes → Red → Servidor ID/Relé**:

- Servidor ID: la IP o dominio del servidor.
- Servidor relé: vacío (usa el mismo).
- Key: la clave pública.

## Hacerlo el servidor por defecto de tu build

Si quieres que todas las descargas de VeloDesk vengan ya configuradas con tu servidor, añade estas dos claves a `DEFAULT_SETTINGS` en `src/brand.rs` y publica una versión nueva:

```json
"custom-rendezvous-server": "IP-O-DOMINIO",
"key": "CLAVE-PUBLICA"
```

## Problemas frecuentes

- **Key mismatch**: la clave copiada lleva un espacio o salto de línea al final.
- **"Ready" pero no conecta**: falta el puerto UDP 21116.
- **Siempre por relé**: uno de los routers no permite hole-punching. Funciona igual con algo más de latencia.
