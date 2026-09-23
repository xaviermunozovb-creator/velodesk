# Mejoras de VeloDesk derivadas de las reseñas

Fuentes: [INVESTIGACION-RUSTDESK.md](INVESTIGACION-RUSTDESK.md) y [INVESTIGACION-COMPETIDORES.md](INVESTIGACION-COMPETIDORES.md).

## Hechas en la versión 1.5.0

| # | Queja | Cambio | Dónde |
|---|---|---|---|
| 1 | Sin actualización automática (RustDesk #13; Splashtop, Zoho) | Comprobación diaria contra GitHub Releases del proyecto y actualización automática activada por defecto. | `src/brand.rs`, `src/common.rs`, `src/updater.rs` |
| 2 | Estafas de "soporte técnico" (RustDesk #1, AnyDesk #6, síntesis #10 y #12) | Aviso rojo con el texto antiestafa en el panel de aceptar conexión del escritorio; en Android se mantiene el diálogo existente. | `flutter/lib/desktop/pages/server_page.dart` |
| 3 | Cuentas, nags, "Powered by", enlaces a precios (síntesis #3, #4, #19) | Sin "Powered by", sin enlaces a planes de pago; el enlace "servidor público" lleva a la guía de servidor propio. | `src/brand.rs`, `flutter/lib/brand.dart` |
| 4 | Servidor público lento/caído/limitado (RustDesk #1-#4) | Servidor propio en un comando, guía en la web, opción de fijarlo en la build. | `server/`, `website/servidor.html` |
| 5 | Equipo remoto que se duerme (Splashtop, CRD; síntesis #15) | "Mantener despierto durante sesiones entrantes" por defecto. | `src/brand.rs` |
| 6 | Confusión gratis/Pro (RustDesk #14, #16) | Todo gratis, dicho en la web y en el README. | `website/` |
| 7 | Desconfianza y privacidad (RustDesk #5, síntesis #11, #13) | Política de privacidad propia, sin telemetría, un solo nombre de producto. | `website/privacidad.html` |
| 9 | Acceso desatendido con demasiados pasos y ventanas que molestan (RustDesk #4, síntesis #6) | Botón "Modo TPV" en Ajustes → Seguridad: contraseña permanente, aceptación por contraseña y ventana de conexión oculta en un clic (1.5.3). | `flutter/lib/desktop/pages/desktop_setting_page.dart` |
| 8 | Instalador con nombre ajeno | MSI y EXE con nombre, empresa y copyright de VeloDesk; app Android con identificador propio (`com.velodesk.app`) que convive con RustDesk. | `flutter/windows/runner/Runner.rc`, `flutter/android/app/build.gradle`, workflow |

## Siguientes (por impacto y esfuerzo)

| Prioridad | Mejora | Origen | Esfuerzo |
|---|---|---|---|
| Alta | Scroll a dos dedos y gestos configurables en la app móvil | RustDesk #9, síntesis #9 | Medio: `flutter/lib/models/input_model.dart`, `mobile/pages/remote_page.dart` |
| Alta | Wake-on-LAN con MAC manual en la libreta de direcciones | RustDesk #17, síntesis #15 | Medio: `flutter/lib/common/widgets/peer_card.dart`, `src/lan.rs` |
| Alta | Servicio Android que sobrevive en segundo plano (aviso de batería, reintento al cambiar de red) | RustDesk #8 | Medio-alto: `flutter/android/.../MainService.kt` |
| Alta | Servidor de libreta de direcciones gratuito (reimplementación mínima de la API) | RustDesk #14 | Alto: nuevo servicio en `server/` |
| Media | Bloqueo de fuerza bruta en el lado controlado (retardo progresivo tras fallos) | RustDesk #6 (CVE-2026-30790) | Bajo-medio: `src/server/connection.rs` |
| Media | Modo teclado "traducir" por defecto para evitar Z/Y y símbolos cambiados | RustDesk #21, síntesis #17 | Bajo: `src/brand.rs` (`keyboard-mode`) tras probarlo |
| Media | Barra de herramientas que no tape la ventana remota (auto-ocultar) | Splashtop, síntesis #11 | Medio: `flutter/lib/desktop/widgets/remote_toolbar.dart` |
| Media | Firma de código Windows con SignPath (gratis para código abierto) | RustDesk #7 | Bajo: trámite + workflow |
| Media | Cola, reanudación y arrastrar/soltar en transferencia de archivos | RustDesk #19, síntesis #8 | Alto |
| Baja | Impresión remota en macOS/Linux | RustDesk #18 | Alto |
| Baja | Redirección USB, lápiz, mandos | RustDesk #24 | Muy alto |
| No posible | Controlar un iPhone/iPad | RustDesk #10 | Apple no lo permite; solo compartir pantalla (ReplayKit) como mejora futura |

## Lo que se decide no hacer

- Detección de "uso comercial", límites de dispositivos, planes con renovación automática: son las tres quejas más repetidas contra los competidores y VeloDesk no las tendrá nunca. Si en el futuro se cobra por algo, será por servicios (servidor gestionado, soporte), con cancelación en un clic.
