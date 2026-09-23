# Falso positivo de Windows Defender en el instalador .exe

**Hecho comprobado el 23-09-2026**: Defender marca `VeloDesk-windows-x86_64.exe` como `Trojan:Win32/Wacatac.B!ml` (detección heurística por aprendizaje automático) y lo pone en cuarentena al descargarlo. El MSI de la misma release (`VeloDesk-windows-x86_64.msi`, SHA-256 `99e5bc31bc4ac1733b53892455f64cd71decbd21094b59fba2b03a5e2addfdea`) se analiza limpio.

Causa: el .exe es un autoextraíble (empaquetador portable de RustDesk) sin firma de código. Esa combinación dispara las heurísticas. No hay ningún código malicioso: es el código público del repositorio compilado por GitHub Actions.

## Medidas tomadas

1. La web y los enlaces cortos ofrecen el **MSI** como descarga principal de Windows. El .exe queda como opción secundaria con aviso.
2. Las instalaciones por MSI se actualizan con MSI (cambio en `src/updater.rs` y `src/flutter_ffi.rs`, sale en la 1.5.1).

## Reportar el falso positivo a Microsoft (5 minutos, gratis)

1. Descarga el .exe y, si Defender lo bloquea, en Seguridad de Windows → Historial de protección → "Permitir en el dispositivo".
2. Entra en https://www.microsoft.com/en-us/wdsi/filesubmission con una cuenta Microsoft.
3. Rellena:
   - **Submission type**: Software developer.
   - **Detection name**: `Trojan:Win32/Wacatac.B!ml`.
   - **Company name**: VeloDesk.
   - **Product name**: VeloDesk.
   - **Website**: https://velodesk.pages.dev
   - **File**: `VeloDesk-windows-x86_64.exe`.
   - **Comments** (copia y pega):

     > VeloDesk is an open-source remote desktop application derived from RustDesk (AGPL-3.0). The file is a self-extracting portable installer built by GitHub Actions from the public repository https://github.com/xaviermunozovb-creator/velodesk (release 1.5.0). It is flagged as Trojan:Win32/Wacatac.B!ml, which is a false positive: the same build packaged as MSI is not detected, and the source code is fully public. Please review and remove the detection.

4. Microsoft responde por correo, normalmente en 24-72 horas. Tras la respuesta, vuelve a descargar el .exe para comprobarlo.

## Firma de código gratuita (SignPath Foundation)

SignPath firma gratis proyectos de código abierto. Solicitud en https://signpath.org/apply con:

- **Project**: VeloDesk, https://github.com/xaviermunozovb-creator/velodesk
- **License**: AGPL-3.0
- **Description**: Free and open-source remote desktop for Windows, Android, macOS and iOS, derived from RustDesk, built on GitHub Actions. Windows binaries (EXE installer and MSI) are currently unsigned, which causes SmartScreen warnings and antivirus false positives.
- **Build system**: GitHub Actions, workflow `.github/workflows/flutter-build.yml`.

Requisitos que piden: repositorio público con licencia OSI, compilación reproducible en CI, y añadir un paso de firma en el flujo (ellos dan la acción de GitHub). Tarda de una a cuatro semanas.

## Alternativa de pago

Certificado de firma de código OV (unos 200 €/año) o Azure Trusted Signing (unos 10 $/mes, solo para empresas con 3 años de antigüedad). Quita el aviso de SmartScreen desde el primer día; las heurísticas de Defender mejoran mucho con firma pero no desaparecen del todo hasta que el archivo acumula reputación.
