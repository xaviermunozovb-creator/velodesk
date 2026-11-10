# VeloDesk · Estado del proyecto y cómo retomarlo

Actualizado el 10-11-2026 desde el MSI. Este documento está pensado para que cualquiera de
los tres PCs (MSI, Asus, tercero), y el Claude Code que corra en ellos, pueda seguir el
proyecto sin preguntar nada. Léelo entero antes de tocar nada.

---

## 1. Qué es VeloDesk

- Escritorio remoto gratuito, código abierto (AGPL-3.0), basado en RustDesk 1.5.x con marca
  propia. Lo usa Xavier sobre todo para entrar en la **TPV de Casara** desde el móvil y los PCs.
- Repositorio público: `https://github.com/xaviermunozovb-creator/velodesk` (rama `master`).
- Web de descargas: `https://velodesk.pages.dev` (Cloudflare Pages, se despliega sola con cada
  push a `master`; carpeta `website/` del repo).
- Compilación: GitHub Actions, flujo "Flutter Tag Build". Se dispara al subir una **etiqueta**
  de versión y publica los instaladores en GitHub Releases con nombres fijos
  (`VeloDesk-windows-x86_64.msi`, `VeloDesk-android.apk`, `VeloDesk-macos-aarch64.dmg`,
  `VeloDesk-ios-unsigned.ipa`, etc.).
- Las apps comprueban actualizaciones una vez al día y se actualizan solas (ajuste de serie).

### Dónde está el código

| Copia | Dónde | Estado |
|---|---|---|
| Original | En el Asus, fuera de Proton Drive (carpeta donde se compiló) | Última vez tocada: versión 1.5.3 (23-09-2026). **Puede tener cambios sin subir: comprobar con `git status`.** |
| Compartida | `Proton Drive\Claude Code\Proyectos\VeloDesk` (clon superficial hecho el 29-10-2026) | Al día con GitHub (commit `7fd5b0d`, versión 1.5.4). Es la copia con la que se trabaja desde ahora. |

Regla: git sobre esta carpeta **desde un solo PC a la vez**, y esperar a que Proton Drive
marque "Sincronizado" antes de cambiar de PC (la carpeta `.git` también se sincroniza).

Archivos clave del repo:

- `src/brand.rs`: nombre, repo de actualizaciones, web y **ajustes por defecto** (aquí va el
  servidor propio). `flutter/lib/brand.dart` es su espejo para la interfaz.
- `res/brand/bump_version.py X.Y.Z`: sube la versión en todos los archivos.
- `res/brand/set_brand.py`: renombrar la app o cambiar de repo/web.
- `server/`: todo lo del servidor de conexión (ver sección 3).
- `docs/velodesk/GUIA-PUBLICACION.md`: guía completa de publicación.
- `docs/velodesk/MEJORAS.md`: mejoras hechas y pendientes, con su origen.

---

## 2. Cronología de lo hecho

**Antes del 29-10-2026 (en el Asus):** rebrand completo, aviso antiestafa, actualización
automática, web, guía de servidor propio, "Modo TPV" (acceso desatendido silencioso en un
clic, versión 1.5.3). Todo compilado y publicado desde GitHub Actions.

**29-10-2026 (desde el MSI):**

1. Diagnóstico: VeloDesk usaba los **servidores públicos de RustDesk** (`rs-ny.rustdesk.com`)
   sin cambios, porque `brand.rs` no fijaba servidor. VeloDesk y RustDesk original eran
   interoperables. Desde el MSI esos servidores respondían bien; el fallo "desde el Asus no
   conecta" **no quedó diagnosticado** (sin mensaje de error, simplemente no conecta).
2. Servidor propio instalado en **IslaTortuga** (el Hetzner del bot de trading), aislado del
   bot. Detalle en la sección 3.
3. Versión **1.5.4** publicada: el servidor propio va de serie en la app. Detalle en la
   sección 4.
4. 1.5.4 instalada en el MSI como servicio y verificada: conecta con IslaTortuga.
5. La TPV y el móvil quedaron en 1.5.3 esperando a actualizarse solos.

**10-11-2026 (desde el MSI):** carpeta compartida entre los tres PCs configurada (ver
`Proton Drive\Claude Code\CLAUDE.md`), memoria de Claude compartida y copia local diaria.
Este documento.

---

## 3. Servidor de conexión: IslaTortuga

| Dato | Valor |
|---|---|
| Máquina | Hetzner Cloud, Núremberg (nbg1-dc3), **ARM aarch64 (Ampere)**, Ubuntu. Es la misma del bot de trading T-1983 (`/opt/turtle`). |
| IP (Servidor ID y Relé) | `46.225.99.214` |
| Key (clave pública) | `SVusqX3Gxwr0kHzOBnxeLIRNdADaT2krBSxG+IxcIsU=` |
| Software | hbbs + hbbr (rustdesk-server **1.1.16**, binarios oficiales arm64, huella SHA-256 verificada) |
| Puertos abiertos | TCP 21115-21117 y UDP 21116 (solo los de la app nativa; 21118/21119 del cliente web NO) |
| Acceso | SSH como `root` **con contraseña** (la sabe Xavier). Sin clave SSH instalada. |

### Cómo está instalado (y por qué así)

Xavier exigió que el servidor VeloDesk **no pudiera afectar al bot**. Por eso no se usó el
instalador genérico con Docker, sino `server/instalar-islatortuga.sh`:

- Sin Docker: binarios en `/opt/velodesk-server/bin`, datos en `/opt/velodesk-server/data`.
- Usuario de sistema `velodesk` sin shell. Servicios systemd `velodesk-hbbs` y `velodesk-hbbr`
  encerrados: solo escriben en su carpeta de datos, `/opt/turtle` les es inaccesible,
  límite 256 MB de RAM y medio núcleo. Arrancan solos con la máquina.
- `-k _`: solo aceptan clientes que lleven la Key.
- ufw solo aditivo (dos reglas nuevas, nada más tocado). El script fotografía cron, firewall,
  `/opt/turtle` y servicios antes y después, y avisa si algo cambió.
- `server/desinstalar-islatortuga.sh` lo deshace entero sin tocar el bot.
- `server/diagnostico-udp.sh` (+ `diagnostico-udp.ps1` para lanzarlo desde Windows) comprueba
  desde dentro que todo responde.

### Cómo operar el servidor desde cualquier PC

Los scripts se copian con `scp` y se ejecutan con `ssh`; Windows pide la contraseña de root
en la terminal y la teclea Xavier (Claude no la ve ni la necesita):

```
scp instalar-islatortuga.sh root@46.225.99.214:/root/
ssh root@46.225.99.214 "bash /root/instalar-islatortuga.sh"
```

Si la conexión se cierra antes de teclear la contraseña, es el límite de dos minutos del
servidor: relanzar. En Windows la directiva de ejecución bloquea los `.ps1`: lanzarlos con
`powershell -NoProfile -ExecutionPolicy Bypass -File archivo.ps1`.

Verificado el 29-10-2026 desde fuera: TCP 21115-21117 y UDP 21116 responden al protocolo.
Una sonda UDP falló justo después de instalar y luego fue bien: no alarmarse a la primera.

Mejora pendiente, no urgente: un nombre de dominio apuntando a la IP, para no tener que
publicar versión nueva si algún día cambia la IP o el servidor.

---

## 4. Versión 1.5.4: servidor propio de serie

Cambios (commit `7fd5b0d`, etiqueta `1.5.4`):

- `src/brand.rs` → `DEFAULT_SETTINGS` incluye `custom-rendezvous-server` = `46.225.99.214` y
  `key` = la Key. Es ajuste **por defecto, no forzado**: cualquier equipo puede poner otro
  servidor en Ajustes → Red.
- `website/index.html`: dice que la app viene con servidor propio en Europa.
- `server/`: los scripts de IslaTortuga y una nota en `README.md`.
- Versión subida con `bump_version.py 1.5.4`.

Verificado en el MSI tras instalar: la IP y la Key están dentro de `librustdesk.dll`
(el `.exe` es solo el lanzador de Flutter), el servicio "VeloDesk" corre, y hay conexión
establecida con IslaTortuga.

### Cómo publicar la siguiente versión

```
python res/brand/bump_version.py 1.5.5
git commit -am "Versión 1.5.5: ..."
git tag 1.5.5
git push origin master 1.5.5
```

La compilación tarda **60-80 minutos**. Durante ese rato los botones de la web dan 404,
porque "última versión" ya apunta a la release nueva aunque esté vacía: es normal.

Incidente conocido: el primer intento de la 1.5.4 cayó por un **502 pasajero** de
`chromium.googlesource.com` al bajar `libwebm`, y dejó en "saltado" Windows x86_64, Android,
Mac e iOS. Receta: **cancelar el flujo** (no esperar al job de Windows 32 bits, que no sirve)
y "Re-run failed jobs". El segundo intento tardó una hora exacta.

---

## 5. Estado de cada equipo

| Equipo | Versión | Servidor | Notas |
|---|---|---|---|
| MSI (portátil) | 1.5.4, instalada como servicio el 29-10 | IslaTortuga | Verificada. Aún **no ha entrado en la TPV** (la TPV no estaba en 1.5.4). |
| TPV de Casara | 1.5.3 → se actualiza sola | públicos → IslaTortuga al actualizar | Modo TPV activo con **contraseña permanente** (la puso Xavier al activarlo; si no la recuerda, se cambia desde el móvil en Ajustes → Seguridad). |
| Móvil (Android) | 1.5.3 → se actualiza sola | públicos → IslaTortuga al actualizar | Tiene guardada la contraseña de la TPV. Entra en la TPV sin problema. |
| Asus | ? | ? | Es desde donde **no conectaba** con los públicos, sin mensaje. Sin diagnosticar. Tiene la copia original del código. |

Mientras dos equipos estén en servidores distintos **no se ven entre sí**, aunque todo
funcione. Al actualizarse ambos a 1.5.4, se ven.

---

## 6. Pendientes, por orden

1. **Probar MSI → TPV** cuando la TPV esté en 1.5.4 (comprobar desde el móvil en
   Ajustes → Acerca de). Si entra, el servidor propio queda confirmado de punta a punta.
2. **Diagnosticar el Asus**: instalar/actualizar a 1.5.4 e intentar entrar en la TPV. Si sigue
   sin conectar, anotar qué pone abajo a la izquierda ("Listo" / "No listo") y dónde se queda
   ("Conectando..." / "ID no existe" / tiempo agotado). Hipótesis vivas: red del Asus
   bloqueando UDP, o Asus en la misma Wi-Fi que la TPV con el firewall de la TPV cortando la
   conexión local, o RustDesk original instalado al lado con otro servidor configurado.
3. **Ventana de aceptar en la TPV**: Xavier dice que a veces sale un diálogo pese al Modo TPV.
   Analizado en el código: la ventana solo sale si el modo de aprobación no es "solo
   contraseña"; el servidor no influye. Comprobar en la TPV (Ajustes → Seguridad) que el Modo
   TPV figura activo, reactivarlo si no, y anotar el texto exacto de los botones la próxima
   vez (podría ser otro diálogo, como el de elevación).
4. **Unificar las dos copias del código en el Asus** (sección 1): `git status` en la
   original; si limpia, retirarla; si no, commit + push y `git pull` en `Proyectos\VeloDesk`.
5. Opcionales de la guía de publicación: dominio propio, firma de código Windows (quitar el
   aviso de SmartScreen), Google Play, Apple Developer.

---

## 7. Cómo retomar en otro PC (Asus o tercero)

1. Esperar a que Proton Drive baje `Claude Code` entera.
2. Doble clic en `Proton Drive\Claude Code\configurar-pc.cmd` con Claude Code cerrado:
   conecta la memoria de Claude con la compartida y crea la copia local diaria.
3. Abrir Claude Code con `Proton Drive\Claude Code` como carpeta de trabajo.
4. Decirle: "Lee `Proyectos\VeloDesk\ESTADO-PROYECTO.md` y seguimos con VeloDesk". Con la
   memoria compartida ya sabrá el resto; sin ella, este documento basta.

---

## 8. Cosas que cuesta recordar

- IslaTortuga es **ARM**, no AMD, aunque se le llame así. Binarios arm64.
- El `.exe` de VeloDesk en Windows no contiene la configuración; está en `librustdesk.dll`.
- `hide_cm` (ocultar la ventana de conexión) solo se respeta porque la app se llama distinto
  de "RustDesk" (`is_custom_client()`), y se decide una vez al arrancar el gestor de conexiones.
- El servidor público de RustDesk está en Nueva York; IslaTortuga en Núremberg: un tercio de
  latencia desde España.
- Cloudflare gratuito no sirve para alojar el servidor de conexión (no abre puertos TCP/UDP);
  solo la web.
- iOS no se deja controlar en remoto por diseño: en iPhone VeloDesk solo controla, no es
  controlado.
