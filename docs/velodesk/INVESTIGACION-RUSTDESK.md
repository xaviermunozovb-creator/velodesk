# Investigación: quejas, reseñas negativas y funciones más pedidas de RustDesk (2025-2026)

Fecha: 22 de septiembre de 2026.

## Nota metodológica y límites

- **Google Play**: no hay reseñas recientes porque RustDesk se auto-retiró de Google Play el 3-sep-2023 para frenar estafas; Android se distribuye por GitHub/F-Droid ([blog oficial](https://rustdesk.com/blog/rustdesk-and-remote-access-scams/), [discusión #5660](https://github.com/rustdesk/rustdesk/discussions/5660)).
- **G2/Capterra**: no existe ficha de RustDesk (confirmado por [OpenMSP, jun-2026](https://www.openmsp.ai/blog/rustdesk-review)). Se usaron Trustpilot (2,9/5, 6 reseñas), SourceForge (2,3/5), AlternativeTo (4,1/5, 33 valoraciones) y App Store (4,2/5, 75 valoraciones).
- **Reddit**: bloqueado para el rastreador. La opinión de r/sysadmin, r/selfhosted y r/msp se recoge indirectamente vía OpenMSP, que la sintetiza como "seguro si se configura bien, arriesgado tal cual viene".
- **Foros en español**: ElOtroLado y Forocoches accesibles; Mediavida devolvió 403. Xataka Móvil (may-2026) es la reseña reciente principal.

Señal: **Muy alta** = múltiples fuentes independientes + hilos con decenas de comentarios/votos o cobertura de prensa; **Alta** = varias fuentes o hilo GitHub con >10 votos/participantes; **Media** = 2-3 hilos o reseñas coincidentes; **Baja** = aislado pero relevante.

## Ranking (1 = mayor peso)

**1. Abuso por estafadores/botnets y las contramedidas que rompen el servidor público** — Señal: Muy alta — Servidor + Docs
RustDesk es la herramienta de acceso remoto más usada en estafas; en ene-2026 un botnet ("Go Client", ~2 M de IPs) obligó a bloquear conexiones entre ciudades distintas en el servidor público, dejando fuera a usuarios legítimos. Además ahora el controlador debe iniciar sesión con Google/GitHub, regla que los usuarios consideran ambigua y con dudas de privacidad.
Fuentes: [#14167](https://github.com/rustdesk/rustdesk/discussions/14167), [SecurityOnline](https://securityonline.info/the-go-client-trap-why-your-rustdesk-id-is-currently-under-automated-botnet-siege/), [wiki login obligatorio](https://github.com/rustdesk/rustdesk/wiki/Login-required-for-public-server), [#15251](https://github.com/rustdesk/rustdesk/discussions/15251), [#14805](https://github.com/rustdesk/rustdesk/discussions/14805), [#10640](https://github.com/rustdesk/rustdesk/discussions/10640), [Malwarebytes ene-2026](https://www.malwarebytes.com/blog/threat-intel/2026/01/how-real-software-downloads-can-hide-remote-backdoors), [Forocoches](https://forocoches.com/foro/showthread.php?t=9937353), [HN 46840655](https://news.ycombinator.com/item?id=46840655).

**2. Conexiones lentas, por relay en vez de directas, o que tardan 15-25 s en establecerse** — Señal: Muy alta — Cliente + Servidor + Docs
Hole-punching que falla y cae a relay, latencia alta, "connection timeout", relays no cifrados cuando hay key mismatch. Un usuario tardó semanas en descubrir que desactivar IPv6 lo arreglaba; el establecimiento sin especificar servidor tarda 15-25 s frente a inmediato con servidor explícito.
Fuentes: [#10924](https://github.com/rustdesk/rustdesk/discussions/10924), [#7422](https://github.com/rustdesk/rustdesk/discussions/7422), [#7574](https://github.com/rustdesk/rustdesk/discussions/7574), [#12668](https://github.com/rustdesk/rustdesk/discussions/12668), [Medium: relayed & unencrypted](https://medium.com/@gdadkisson/donovan-adkisson-how-to-solve-rustdesk-relayed-and-unencrypted-connection-issues-4f4de5fddf86), [Xataka Móvil](https://www.xatakamovil.com/aplicaciones/no-hace-falta-pagar-para-tener-escritorio-remoto-rustdesk-open-source-funciona-a-mil-maravillas-movil-1).

**3. Servidor público caído, saturado o "no apto para producción"** — Señal: Alta — Servidor + Docs
DDoS de ene-2024 que dejó sin servicio a todo el que no se auto-hospedaba; la wiki dice ahora que el servidor público es "solo para demo y pruebas".
Fuentes: [#7027](https://github.com/rustdesk/rustdesk/issues/7027), [wiki](https://github.com/rustdesk/rustdesk/wiki/Login-required-for-public-server), [Slashdot](https://slashdot.org/software/p/RustDesk/), [AirDroid alternatives 2026](https://www.airdroid.com/mdm/best-rustdesk-alternatives/).

**4. Complejidad del self-hosting (claves, puertos, "key mismatch", "ID does not exist")** — Señal: Alta — Docs/Onboarding + Cliente
Errores típicos: clave pública con espacio final, UDP 21116 bloqueado, Docker sin `network_mode: host`. Reseña AlternativeTo (abr-2026, 1★): "no funciona sin esa configuración complicada de servidor"; Forocoches: "el usuario doméstico se pierde si le metes código o mucho campo que tocar".
Fuentes: [AlternativeTo](https://alternativeto.net/software/rustdesk/about/), [SourceForge](https://sourceforge.net/software/product/RustDesk/), [Forocoches](https://forocoches.com/foro/showthread.php?t=9937353), [rustdesk-server #436](https://github.com/rustdesk/rustdesk-server/discussions/436), [#7008](https://github.com/rustdesk/rustdesk/discussions/7008), [Arch BBS](https://bbs.archlinux.org/viewtopic.php?id=303627), [doc Docker](https://rustdesk.com/docs/en/self-host/rustdesk-server-oss/docker/).

**5. Desconfianza sobre origen/propiedad (China vs. Singapur), anonimato y certificado raíz** — Señal: Alta — Docs/Transparencia + Cliente
Persiste desde 2021: "operación anónima de un solo hombre", instalación de un certificado raíz SHA-1 con validez 10 años, ausencia de SOC 2 o auditoría independiente.
Fuentes: [HN 39256493](https://news.ycombinator.com/item?id=39256493), [HN 39262265](https://news.ycombinator.com/item?id=39262265), [#1159](https://github.com/rustdesk/rustdesk/discussions/1159), [Trustpilot](https://www.trustpilot.com/review/rustdesk.com), [OpenMSP](https://www.openmsp.ai/blog/rustdesk-review), [HN 42963070](https://news.ycombinator.com/item?id=42963070).

**6. Debilidades de seguridad: fuerza bruta sin límite (CVE-2026-30790, CVSS 9,3), credenciales locales mal protegidas (CVE-2026-30785, 8,2), IP directa sin cifrar** — Señal: Alta — Servidor + Cliente
Fuentes: [NVD CVE-2026-30790](https://nvd.nist.gov/vuln/detail/CVE-2026-30790), [SentinelOne CVE-2026-30785](https://www.sentinelone.com/vulnerability-database/cve-2026-30785/), [HN 49300759](https://news.ycombinator.com/item?id=49300759).

**7. Falsos positivos de antivirus y expulsión de WinGet (mar-2026)** — Señal: Alta — Cliente (firma/distribución) + Docs
ESET marca `Win64/RemoteAdmin.RustDesk.A`, Defender/Trend Micro/Kaspersky lo tratan como PUA; 1.4.2 fue rechazado en WinGet.
Fuentes: [#13025](https://github.com/rustdesk/rustdesk/discussions/13025), [winget-pkgs #368229](https://github.com/microsoft/winget-pkgs/issues/368229), [foro ESET](https://forum.eset.com/topic/48322-rustdesk-winget-validation-failed-due-to-eset-detection-and-other-remote-desktop-tools-pass/), [#6988](https://github.com/rustdesk/rustdesk/discussions/6988), [#2485](https://github.com/rustdesk/rustdesk/discussions/2485).

**8. Android como lado controlado: input bloqueado por "Restricted Setting", servicio muerto en segundo plano, batería** — Señal: Alta — Cliente + Docs
En Samsung One UI 8.5/Android 16 no existe opción para autorizar el servicio de accesibilidad; en Android 13/MIUI el toggle sale gris; el servicio de captura muere a las 2-3 h o al cambiar de red.
Fuentes: [#15723](https://github.com/rustdesk/rustdesk/issues/15723), [#6241](https://github.com/rustdesk/rustdesk/discussions/6241), [#10491](https://github.com/rustdesk/rustdesk/discussions/10491), [#5626](https://github.com/rustdesk/rustdesk/issues/5626), [#6192](https://github.com/rustdesk/rustdesk/issues/6192), [#9902](https://github.com/rustdesk/rustdesk/issues/9902), [#11218](https://github.com/rustdesk/rustdesk/issues/11218), [#10650](https://github.com/rustdesk/rustdesk/discussions/10650), [WirelessMoves oct-2025](https://blog.wirelessmoves.com/2025/10/remote-android-support-with-rustdesk-part-1.html).

**9. UX de la app móvil como controlador: scroll a tres dedos, gestos no configurables, ajustes que no se guardan** — Señal: Alta — Cliente
El scroll con tres dedos choca con gestos del sistema; "most other apps have 2 finger swipe"; App Store (may-2025): "The mouse actions aren't configurable, and three finger scroll rarely works"; los ajustes de pantalla/ratón no persisten entre sesiones.
Fuentes: [#7277](https://github.com/rustdesk/rustdesk/discussions/7277), [#3744](https://github.com/rustdesk/rustdesk/issues/3744), [App Store reseñas](https://apps.apple.com/us/app/rustdesk-remote-desktop/id1581225015?see-all=reviews&platform=iphone), [#14442](https://github.com/rustdesk/rustdesk/discussions/14442).

**10. iOS no puede ser controlado ni siquiera visualizado** — Señal: Media-Alta — Cliente (limitación de Apple + prioridad)
Fuentes: [#4839](https://github.com/rustdesk/rustdesk/discussions/4839), [blog Android/iOS](https://rustdesk.com/blog/rustdesk-remote-control-android-ios/).

**11. Linux/Wayland: pantalla negra, pantalla de login inaccesible** — Señal: Alta — Cliente + Docs
Fuentes: [#12497](https://github.com/rustdesk/rustdesk/discussions/12497), [#9474](https://github.com/rustdesk/rustdesk/discussions/9474), [#10825](https://github.com/rustdesk/rustdesk/discussions/10825), [#11131](https://github.com/rustdesk/rustdesk/discussions/11131), [doc Linux](https://rustdesk.com/docs/en/client/linux/), [HN 49300759](https://news.ycombinator.com/item?id=49300759).

**12. Consumo de CPU excesivo (servicio Linux en reposo; 800-1200 % en sesión)** — Señal: Alta — Cliente
Fuentes: [#11156](https://github.com/rustdesk/rustdesk/issues/11156), [#15520](https://github.com/rustdesk/rustdesk/issues/15520), [#16312](https://github.com/rustdesk/rustdesk/issues/16312), [#15740](https://github.com/RustDesk/RustDesk/issues/15740), [#7646](https://github.com/rustdesk/rustdesk/discussions/7646).

**13. Sin actualización automática/silenciosa fiable del cliente** — Señal: Alta — Cliente
Petición repetida desde 2023; la opción `allow-auto-update` existe pero en mar-2026 el mantenedor responde "Not ready yet"; sin esto el despliegue empresarial es inviable.
Fuentes: [#14466](https://github.com/rustdesk/rustdesk/discussions/14466), [#10345](https://github.com/rustdesk/rustdesk/discussions/10345), [#4704](https://github.com/rustdesk/rustdesk/discussions/4704), [#5146](https://github.com/rustdesk/rustdesk/discussions/5146), [#3346](https://github.com/rustdesk/rustdesk/issues/3346), [server-pro #661](https://github.com/rustdesk/rustdesk-server-pro/discussions/661), [RustDeskUpdater](https://github.com/alesanGreat/RustDeskUpdater).

**14. Libreta de direcciones sincronizada, cuentas y consola solo en Pro; confusión sobre qué es gratis** — Señal: Alta — Servidor (OSS) + Cliente + Docs
Fuentes: [#6161](https://github.com/rustdesk/rustdesk/discussions/6161), [#7533](https://github.com/rustdesk/rustdesk/discussions/7533), [#7725](https://github.com/rustdesk/rustdesk/discussions/7725), [Welentis](https://github.com/Welentis/rustdesk-address-book), [Realmagnum](https://github.com/Realmagnum/rustdesk-address-book), [Cybis320](https://github.com/Cybis320/rustdesk-addressbook), [CWL ene-2026](https://cwl.cc/2026/01/heres-a-free-rustdesk-address-book-tool-you-might-not-have-tried.html/), [OpenMSP](https://www.openmsp.ai/blog/rustdesk-review).

**15. Soporte deficiente/brusco, bugs cerrados con workarounds** — Señal: Alta — Proceso/Docs
Fuentes: [SourceForge](https://sourceforge.net/software/product/RustDesk/), [Trustpilot](https://www.trustpilot.com/review/rustdesk.com), [server-pro #636](https://github.com/rustdesk/rustdesk-server-pro/issues/636), [HN 49300759](https://news.ycombinator.com/item?id=49300759).

**16. Licenciamiento Pro: sin reembolsos, cobro por endpoint, dependencia del servidor de licencias** — Señal: Media-Alta — Servidor + Docs
Server Pro 1.7.5 dejó de funcionar por completo cuando rustdesk.com fue inalcanzable (feb-2026), pese a licencia válida.
Fuentes: [server-pro #902](https://github.com/rustdesk/rustdesk-server-pro/issues/902), [Trustpilot](https://www.trustpilot.com/review/rustdesk.com), [HN 45385536](https://news.ycombinator.com/item?id=45385536), [#5942](https://github.com/rustdesk/rustdesk/discussions/5942), [programming.dev](https://programming.dev/post/38109895).

**17. Wake-on-LAN incompleto (solo en pestaña "Discovered", sin MAC manual)** — Señal: Media — Cliente
Fuentes: [#5583](https://github.com/rustdesk/rustdesk/discussions/5583), [#12274](https://github.com/rustdesk/rustdesk/discussions/12274), [#1249](https://github.com/rustdesk/rustdesk/discussions/1249), [#981](https://github.com/rustdesk/rustdesk/issues/981).

**18. Impresión remota solo en Windows y con errores** — Señal: Media — Cliente
Fuentes: [#286](https://github.com/rustdesk/rustdesk/issues/286), [#5159](https://github.com/rustdesk/rustdesk/discussions/5159), [#14181](https://github.com/rustdesk/rustdesk/issues/14181), [#12314](https://github.com/rustdesk/rustdesk/discussions/12314), [HN 42963070](https://news.ycombinator.com/item?id=42963070).

**19. Transferencia de archivos lenta y con poca calidad de vida** — Señal: Media — Cliente (+ relay)
~30 MB/s con enlace de 1 Gb/s; peticiones de cola, reanudación y drag&drop.
Fuentes: [#13181](https://github.com/rustdesk/rustdesk/discussions/13181), [#10803](https://github.com/rustdesk/rustdesk/discussions/10803), [#1607](https://github.com/rustdesk/rustdesk/discussions/1607), [#9118](https://github.com/rustdesk/rustdesk/discussions/9118).

**20. Portapapeles inconsistente entre plataformas** — Señal: Media — Cliente
Fuentes: [#13463](https://github.com/rustdesk/rustdesk/issues/13463), [#12458](https://github.com/rustdesk/rustdesk/discussions/12458), [#4657](https://github.com/rustdesk/rustdesk/issues/4657), [#11203](https://github.com/rustdesk/rustdesk/issues/11203).

**21. Mapeo de teclado erróneo entre layouts/SO** — Señal: Media — Cliente
Fuentes: [#10520](https://github.com/rustdesk/rustdesk/issues/10520), [#14338](https://github.com/rustdesk/rustdesk/issues/14338), [#12945](https://github.com/rustdesk/rustdesk/discussions/12945), [#5692](https://github.com/rustdesk/rustdesk/issues/5692), [#13038](https://github.com/rustdesk/rustdesk/discussions/13038).

**22. Permisos y elevación: UAC congela/ennegrece la sesión (Windows), TCC en macOS** — Señal: Media — Cliente + Docs
Fuentes: [#12691](https://github.com/rustdesk/rustdesk/issues/12691), [#14216](https://github.com/rustdesk/rustdesk/issues/14216), [#6034](https://github.com/rustdesk/rustdesk/issues/6034), [#70](https://github.com/rustdesk/rustdesk/issues/70), [#3261](https://github.com/rustdesk/rustdesk/issues/3261), [gHacks](https://www.ghacks.net/2024/10/17/how-to-fix-rustdesk-not-working-on-macos/).

**23. Modo privacidad roto** — Señal: Media — Cliente
Fuentes: [#11436](https://github.com/rustdesk/rustdesk/issues/11436), [#11186](https://github.com/rustdesk/rustdesk/issues/11186), [#12888](https://github.com/rustdesk/rustdesk/issues/12888), [#16269](https://github.com/rustdesk/rustdesk/issues/16269), [#15294](https://github.com/rustdesk/rustdesk/issues/15294), [#11639](https://github.com/rustdesk/rustdesk/issues/11639).

**24. Periféricos: USB passthrough, lápiz/tableta, micrófono, mandos** — Señal: Media (las más votadas de Feature Request) — Cliente
Fuentes: [Feature Request ordenado por votos](https://github.com/rustdesk/rustdesk/discussions/categories/feature-request?discussions_q=is%3Aopen+category%3A%22Feature+Request%22+sort%3Atop), [#6014](https://github.com/rustdesk/rustdesk/discussions/6014), [#6537](https://github.com/rustdesk/rustdesk/discussions/6537), [#6868](https://github.com/rustdesk/rustdesk/discussions/6868), [#3762](https://github.com/rustdesk/rustdesk/issues/3762).

**25. Multi-monitor/HiDPI: ventana en blanco (Flutter), escalado diminuto** — Señal: Media — Cliente
Fuentes: [#6756](https://github.com/rustdesk/rustdesk/issues/6756), [#7427](https://github.com/rustdesk/rustdesk/discussions/7427), [#4821](https://github.com/rustdesk/rustdesk/discussions/4821), [#14251](https://github.com/rustdesk/rustdesk/discussions/14251), [HN 42963070](https://news.ycombinator.com/item?id=42963070).

## Resumen por tipo de cambio

| Tipo | Ítems |
|---|---|
| **Cliente** (mayoría) | 2, 6, 7, 8, 9, 10, 11, 12, 13, 17-25 |
| **Servidor** (público u OSS/Pro) | 1, 2, 3, 6, 14, 16 |
| **Docs/Onboarding/Proceso** | 1, 2, 3, 4, 5, 7, 8, 11, 14, 15, 16, 22 |

## Observaciones transversales

- Los tres bloques con más volumen y más "dolor" en 2025-2026 son: (a) el ecosistema de abuso y las contramedidas del servidor público (1, 3, 7), (b) fiabilidad/latencia de conexión y fricción de self-hosting (2, 4), y (c) el lado móvil, sobre todo Android controlado e iOS (8, 9, 10).
- Frente a AnyDesk/TeamViewer, lo que más se echa en falta en el nivel gratuito son: libreta sincronizada/cuentas, auto-update, WoL completo, impresión multiplataforma y USB redirect.
- En español la conversación es mayoritariamente positiva (huida de AnyDesk/TeamViewer por licencias); las quejas concretas son seguridad/estafas, detección por antivirus y curva de configuración para usuario doméstico.
