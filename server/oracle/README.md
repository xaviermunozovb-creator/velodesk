# Crear el servidor en Oracle Cloud con reintentos automáticos

La capa gratuita de Oracle suele responder **"Out of capacity"** al crear la máquina. La forma fiable de conseguirla es reintentar cada pocos minutos con un script. Este lo hace todo: red, puertos, máquina y, si quieres, la instalación del servidor de VeloDesk.

## 1. Clave API (una sola vez, 2 minutos)

1. En la consola de Oracle, arriba a la derecha: icono de usuario → **Mi perfil** (User settings).
2. Pestaña **Claves API** (API keys) → **Añadir clave API** → **Pegar clave pública**.
3. Pega el contenido de `C:\Users\xavie\.oci\velodesk_api_public.pem` y pulsa **Añadir**.
4. Oracle muestra un "fragmento de archivo de configuración". Cópialo en `C:\Users\xavie\.oci\config` y cambia la última línea por:

```
key_file=C:\Users\xavie\.oci\velodesk_api.pem
```

Queda algo así:

```
[DEFAULT]
user=ocid1.user.oc1..xxxx
fingerprint=xx:xx:...
tenancy=ocid1.tenancy.oc1..xxxx
region=eu-madrid-1
key_file=C:\Users\xavie\.oci\velodesk_api.pem
```

## 2. Lanzar los reintentos

```bash
python server/oracle/reintentar-instancia.py --instalar
```

Déjalo abierto. Cada 2 minutos intenta crear la máquina alternando ARM (A1.Flex) y AMD (E2.1.Micro). Puede tardar minutos u horas, a veces más de un día. Cuando lo consigue:

- imprime la IP pública y la guarda en `server/oracle/instancia.json`;
- con `--instalar`, entra por SSH e instala el servidor de conexión (imprime la Key al final).

## 3. Después

En la app: Ajustes → Red → Servidor ID/Relé → IP y Key. Para que todas las descargas de VeloDesk vengan configuradas, añade `custom-rendezvous-server` y `key` a `DEFAULT_SETTINGS` en `src/brand.rs`.

## Si prefieres no usar clave API

Puedes seguir pulsando **Crear** en el asistente de la consola hasta que entre. La otra opción es pasar la cuenta a "Pay As You Go" (botón Upgrade): Oracle da prioridad de capacidad a esas cuentas y sigue sin cobrar mientras solo uses recursos Always Free, pero ya hay tarjeta activa y conviene poner una alerta de presupuesto.
