// Identidad de marca de VeloDesk para la interfaz Flutter.
//
// Debe coincidir con `src/brand.rs`. Para cambiar nombre, repositorio o web
// ejecuta `python res/brand/set_brand.py`, que actualiza ambos archivos.

const String kBrandName = 'VeloDesk';
const String kBrandGithubOwner = 'CAMBIAR-USUARIO';
const String kBrandGithubRepo = 'velodesk';
const String kBrandWebsite = 'https://velodesk.pages.dev';

const String kBrandRepoUrl =
    'https://github.com/$kBrandGithubOwner/$kBrandGithubRepo';
const String kBrandDownloadUrl = '$kBrandWebsite/#descargar';
const String kBrandPrivacyUrl = '$kBrandWebsite/privacidad.html';
const String kBrandServerHelpUrl = '$kBrandWebsite/servidor.html';

String brandReleaseUrl(String version) => '$kBrandRepoUrl/releases/tag/$version';
