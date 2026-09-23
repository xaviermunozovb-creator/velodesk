<p align="center"><img src="res/logo-header.svg" alt="VeloDesk" width="450"></p>

# VeloDesk

Escritorio remoto gratuito y de código abierto para **Windows, Android, macOS e iOS**, basado en [RustDesk](https://github.com/rustdesk/rustdesk) (licencia AGPL-3.0) y mejorado con lo que los usuarios de todo el mundo echan en falta en RustDesk, AnyDesk, TeamViewer, Chrome Remote Desktop, Parsec, Splashtop y compañía.

> Nombre provisional. Se cambia con un comando: `python res/brand/set_brand.py --name NuevoNombre --repo usuario/repositorio`.

## Qué cambia respecto a RustDesk

| Queja de los usuarios (ver `docs/velodesk/`) | Qué hace VeloDesk |
|---|---|
| No hay actualización automática fiable (RustDesk #13, Splashtop, Zoho) | Activada por defecto. Comprueba GitHub Releases una vez al día y se actualiza sola cuando no hay sesiones activas. |
| Cuenta obligatoria, "uso comercial sospechado", nags y popups (TeamViewer, AnyDesk, Parsec, RealVNC) | Sin cuenta, sin límites de dispositivos, sin detección de uso comercial, sin publicidad ni "Powered by". |
| Herramienta usada por estafadores (nº 1 en RustDesk y AnyDesk, alertas de Guardia Civil) | Aviso antiestafa en la ventana de aceptar conexión en escritorio (además del diálogo que RustDesk ya tenía en Android). |
| Servidor público lento, caído o con login obligatorio (RustDesk #1-#3) | Servidor propio en un comando (`server/instalar-servidor.sh`), gratis en Oracle Cloud, con guía en la web. Se puede dejar fijado en la build. |
| Confusión sobre qué es gratis y qué es "Pro" (RustDesk #14, Splashtop, Zoho) | Todo es gratis. La web lo dice en la primera línea. |
| Equipo remoto que se duerme en mitad de la sesión (Splashtop, CRD) | "Mantener despierto durante sesiones entrantes" activado por defecto. |
| Desconfianza sobre quién está detrás (RustDesk #5) | Código público, política de privacidad clara, sin telemetría. |
| Compilar en tres sistemas cuesta dinero (Mac, tiendas) | Todo se compila gratis en GitHub Actions, incluidos macOS e iOS. Descargas en la web (Cloudflare Pages) y GitHub Releases. |

El resto de mejoras detectadas en la investigación (scroll a dos dedos en móvil, Wake-on-LAN manual, impresión multiplataforma, etc.) están priorizadas en `docs/velodesk/MEJORAS.md`.

## Estructura del proyecto

- `src/brand.rs` y `flutter/lib/brand.dart`: nombre, repositorio y ajustes por defecto. Único sitio que hay que tocar para renombrar.
- `res/brand/set_brand.py`: aplica el nombre/repositorio/web a todos los archivos.
- `website/`: web de descargas para Cloudflare Pages.
- `server/`: servidor de conexión (Docker) y script de instalación.
- `docs/velodesk/`: investigación de reseñas, lista de mejoras y guía de publicación.
- El resto es el código de RustDesk 1.5.0 sin cambios estructurales.

## Cómo publicar la primera versión

Guía paso a paso en [docs/velodesk/GUIA-PUBLICACION.md](docs/velodesk/GUIA-PUBLICACION.md). Resumen:

1. Crea un repositorio público en GitHub y sube este código.
2. Ejecuta `python res/brand/set_brand.py --repo TU-USUARIO/velodesk` y sube el cambio.
3. Añade los cuatro secretos de firma de Android (carpeta `VeloDesk-secretos` fuera del repositorio).
4. Crea la etiqueta `1.5.0` y súbela: GitHub compila Windows, Android, macOS e iOS y publica la release.
5. Conecta el repositorio a Cloudflare Pages con la carpeta `website` como salida.

## Licencia

AGPL-3.0, la misma que RustDesk. Puedes vender la app, cobrar por soporte o por un servidor gestionado, pero el código fuente de cualquier versión que distribuyas debe ser público.
