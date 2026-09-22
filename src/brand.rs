//! Identidad de marca de VeloDesk.
//!
//! Este es el único sitio del código Rust donde se define el nombre de la app,
//! el repositorio de GitHub desde el que se descargan las actualizaciones y los
//! ajustes por defecto que diferencian a VeloDesk de RustDesk.
//!
//! Para renombrar la app o cambiar de repositorio ejecuta:
//!   python res/brand/set_brand.py --name NOMBRE --repo usuario/repositorio --site https://...
//! que actualiza este archivo y el resto de sitios (Flutter, Android, Windows, web).

/// Nombre visible de la app. Solo letras, números y guiones: se usa como nombre
/// de servicio de Windows, carpeta de instalación y esquema de URL (`velodesk://`).
pub const APP_NAME: &str = "VeloDesk";

/// Usuario u organización de GitHub que aloja el repositorio.
pub const GITHUB_OWNER: &str = "CAMBIAR-USUARIO";

/// Nombre del repositorio de GitHub. Las versiones se publican en sus "Releases".
pub const GITHUB_REPO: &str = "velodesk";

/// Web pública (Cloudflare Pages) con las descargas y la ayuda.
pub const WEBSITE: &str = "https://velodesk.pages.dev";

/// Ajustes por defecto que se aplican si el usuario no ha elegido otro valor.
/// Mismo formato que la sección `default-settings` de un cliente personalizado
/// de RustDesk; las claves están en `libs/base/src/config/keys.rs`.
pub const DEFAULT_SETTINGS: &str = r#"{
    "enable-check-update": "Y",
    "allow-auto-update": "Y",
    "hide-powered-by-me": "Y",
    "keep-awake-during-incoming-sessions": "Y"
}"#;

/// Ajustes forzados que el usuario no puede cambiar. Vacío a propósito: VeloDesk
/// no impone nada, solo cambia valores por defecto.
pub const OVERRIDE_SETTINGS: &str = "{}";

pub fn github_repo_url() -> String {
    format!("https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
}

pub fn latest_release_api_url() -> String {
    format!("https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest")
}

pub fn release_tag_url(tag: &str) -> String {
    format!("{}/releases/tag/{}", github_repo_url(), tag)
}

pub fn website_download_url() -> String {
    format!("{WEBSITE}/#descargar")
}

/// `true` cuando la app se ejecuta con la marca definida aquí (y no como un
/// cliente personalizado de RustDesk cargado desde `custom.txt`).
pub fn is_brand_app() -> bool {
    crate::get_app_name() == APP_NAME
}
