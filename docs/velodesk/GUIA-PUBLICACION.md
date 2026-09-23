# Guía de publicación de VeloDesk

Todo lo de esta guía es gratuito. Los únicos datos que introduces tú son los de tus propias cuentas (GitHub, Cloudflare, Oracle).

## 0. Lo que ya está hecho

- Código de RustDesk 1.5.0 con la marca VeloDesk, actualización automática desde tus GitHub Releases, aviso antiestafa y ajustes por defecto mejorados.
- Cadena de compilación de GitHub Actions ajustada: publica instaladores con nombres fijos (`VeloDesk-windows-x86_64.exe`, `VeloDesk-android.apk`, `VeloDesk-macos-aarch64.dmg`, `VeloDesk-ios-unsigned.ipa`), sin compilaciones nocturnas ni jobs de Linux.
- Clave de firma de Android generada en `C:\Users\xavie\Documents\VeloDesk-secretos\` (fuera del repositorio). **Guárdala en un sitio seguro**: sin ella no se pueden publicar actualizaciones de la app Android.
- Web de descargas en `website/` y servidor de conexión en `server/`.

## 1. Repositorio en GitHub

1. Entra en https://github.com/new. Nombre: `velodesk`. Visibilidad: **Public** (obligatorio por la licencia AGPL y para que la compilación sea gratuita e ilimitada). No marques "Add README".
2. En tu PC, en la carpeta del proyecto:

```bash
python res/brand/set_brand.py --repo TU-USUARIO/velodesk
```

```bash
git add -A && git commit -m "VeloDesk: repositorio propio"
```

```bash
git remote add origin https://github.com/TU-USUARIO/velodesk.git && git push -u origin master
```

Git te pedirá iniciar sesión en GitHub la primera vez.

## 2. Secretos de firma de Android

En GitHub: **Settings → Secrets and variables → Actions → New repository secret**. Crea estos cuatro, con los valores del archivo `VeloDesk-secretos\SECRETS-GITHUB.txt`:

| Nombre | Valor |
|---|---|
| `ANDROID_SIGNING_KEY` | contenido completo de `velodesk-android.keystore.base64` |
| `ANDROID_ALIAS` | `velodesk` |
| `ANDROID_KEY_STORE_PASSWORD` | la contraseña del archivo |
| `ANDROID_KEY_PASSWORD` | la misma contraseña |

Sin estos secretos el APK se publica sin firmar y Android no lo instala.

## 3. Primera compilación y release

```bash
git tag 1.5.0 && git push origin 1.5.0
```

En la pestaña **Actions** verás el flujo "Flutter Tag Build". Tarda entre 60 y 120 minutos la primera vez (después usa caché). Cuando termine, en **Releases** estará la versión `1.5.0` con todos los instaladores.

Si algún job falla, abre su registro: casi siempre es un paso de descarga externa que se reintenta relanzando el job ("Re-run failed jobs").

### Versiones siguientes

1. `python res/brand/bump_version.py 1.5.3` (actualiza Cargo.toml, Cargo.lock, pubspec y los flujos; sin esto la compilación falla con "lock file needs to be updated").
2. `git commit -am "Versión 1.5.3" && git tag 1.5.3 && git push origin master 1.5.3`.
3. Las apps instaladas detectan la nueva versión en 24 horas y se actualizan solas (Windows y macOS instalados; en Android muestran un botón de descarga).

## 4. Web de descargas en Cloudflare Pages

1. https://dash.cloudflare.com → **Workers & Pages → Create → Pages → Connect to Git**.
2. Elige el repositorio `velodesk`. Build command: vacío. **Build output directory: `website`**.
3. Deploy. Tu web quedará en `https://velodesk.pages.dev` (o el nombre que elijas). Si eliges otro nombre, ejecuta `python res/brand/set_brand.py --site https://TU-NOMBRE.pages.dev` y publica una versión nueva para que la app enlace a la web correcta.
4. Cada `git push` a `master` vuelve a desplegar la web. Los enlaces de descarga apuntan siempre a la última release, no hay que tocar la web al publicar versiones.

Enlaces cortos que quedan disponibles: `/descargar/windows`, `/descargar/android`, `/descargar/mac`, `/descargar/ios`.

## 5. Servidor de conexión (recomendado)

Ver [server/README.md](../../server/README.md). En resumen: cuenta gratuita de Oracle Cloud, instancia Ubuntu, `curl ... | sudo bash`, abrir puertos, copiar la clave a la app. Para que todas las descargas vengan configuradas con tu servidor, añade `custom-rendezvous-server` y `key` a `DEFAULT_SETTINGS` en `src/brand.rs`.

## 6. Instalación en cada plataforma

- **Windows**: el `.exe` es instalador y portable a la vez. SmartScreen avisa porque no está firmado con certificado de pago; "Más información → Ejecutar de todas formas". Para quitar el aviso más adelante existe [SignPath](https://signpath.org/) (firma gratuita para proyectos de código abierto) o un certificado de firma de código (a partir de unos 200 €/año).
- **Android**: instalar el APK, permitir "orígenes desconocidos", y en la app activar el servicio de accesibilidad para poder ser controlado. En Android 13+ hay que ir a Ajustes → Apps → VeloDesk → "Permitir ajustes restringidos" antes de activar la accesibilidad.
- **macOS**: abrir el `.dmg`, arrastrar a Aplicaciones, primera vez con clic derecho → Abrir. Conceder "Grabación de pantalla" y "Accesibilidad" cuando lo pida.
- **iOS**: instalar el `.ipa` con [AltStore](https://altstore.io/) o [Sideloadly](https://sideloadly.io/) y un Apple ID gratuito (hay que renovar cada 7 días; con la cuenta de desarrollador de 99 $/año dura un año y se puede publicar en TestFlight/App Store).

## 7. Qué necesita un Mac

Nada para compilar: GitHub lo hace. Un Mac solo hace falta para instalar la app en un iPhone con AltStore/Sideloadly (también funciona desde Windows) o para publicar en la App Store.

## 8. Costes futuros (opcionales)

| Concepto | Coste | Para qué |
|---|---|---|
| Google Play | 25 $ una vez | Publicar en la tienda de Android. |
| Apple Developer | 99 $/año | App Store, TestFlight, notarización de macOS. |
| Certificado de firma de código Windows | ~200 €/año | Quitar el aviso de SmartScreen. |
| Dominio propio | ~10 €/año | `velodesk.com` en lugar de `.pages.dev`. |
