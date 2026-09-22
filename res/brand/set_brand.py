#!/usr/bin/env python3
"""Cambia el nombre, el repositorio de GitHub y la web de VeloDesk en todos los
archivos que los contienen.

    python res/brand/set_brand.py --repo miusuario/velodesk
    python res/brand/set_brand.py --name OtroNombre --repo miusuario/otronombre --site https://otronombre.pages.dev

Solo modifica lo que se pasa por parámetro. Lee los valores actuales de
`src/brand.rs`, así que se puede ejecutar tantas veces como haga falta.
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BRAND_RS = ROOT / "src" / "brand.rs"


def read(p):
    return p.read_text(encoding="utf-8")


def write(p, s):
    p.write_text(s, encoding="utf-8", newline="\n")
    print("  actualizado", p.relative_to(ROOT))


def current():
    s = read(BRAND_RS)
    get = lambda k: re.search(r'pub const %s: &str = "([^"]*)";' % k, s).group(1)
    return {
        "name": get("APP_NAME"),
        "owner": get("GITHUB_OWNER"),
        "repo": get("GITHUB_REPO"),
        "site": get("WEBSITE"),
    }


def replace_all(paths, pairs):
    for rel in paths:
        p = ROOT / rel
        if not p.exists():
            print("  (no existe)", rel)
            continue
        s = read(p)
        new = s
        for old, repl in pairs:
            if old:
                new = new.replace(old, repl)
        if new != s:
            write(p, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", help="Nombre de la app (letras, números y guiones)")
    ap.add_argument("--repo", help="usuario/repositorio de GitHub")
    ap.add_argument("--site", help="URL de la web, sin barra final")
    a = ap.parse_args()
    if not (a.name or a.repo or a.site):
        ap.error("indica al menos --name, --repo o --site")

    cur = current()
    new = dict(cur)
    if a.name:
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]{1,30}", a.name):
            sys.exit("El nombre solo puede tener letras, números y guiones y empezar por letra.")
        new["name"] = a.name
    if a.repo:
        if "/" not in a.repo:
            sys.exit("--repo debe ser usuario/repositorio")
        new["owner"], new["repo"] = a.repo.split("/", 1)
    if a.site:
        new["site"] = a.site.rstrip("/")

    print("Antes :", cur)
    print("Después:", new)

    # 1. Constantes Rust y Dart
    replace_all(["src/brand.rs"], [
        ('pub const APP_NAME: &str = "%s";' % cur["name"], 'pub const APP_NAME: &str = "%s";' % new["name"]),
        ('pub const GITHUB_OWNER: &str = "%s";' % cur["owner"], 'pub const GITHUB_OWNER: &str = "%s";' % new["owner"]),
        ('pub const GITHUB_REPO: &str = "%s";' % cur["repo"], 'pub const GITHUB_REPO: &str = "%s";' % new["repo"]),
        ('pub const WEBSITE: &str = "%s";' % cur["site"], 'pub const WEBSITE: &str = "%s";' % new["site"]),
    ])
    replace_all(["flutter/lib/brand.dart"], [
        ("const String kBrandName = '%s';" % cur["name"], "const String kBrandName = '%s';" % new["name"]),
        ("const String kBrandGithubOwner = '%s';" % cur["owner"], "const String kBrandGithubOwner = '%s';" % new["owner"]),
        ("const String kBrandGithubRepo = '%s';" % cur["repo"], "const String kBrandGithubRepo = '%s';" % new["repo"]),
        ("const String kBrandWebsite = '%s';" % cur["site"], "const String kBrandWebsite = '%s';" % new["site"]),
    ])

    # 2. Repositorio en web, servidor y documentación
    old_repo = "%s/%s" % (cur["owner"], cur["repo"])
    new_repo = "%s/%s" % (new["owner"], new["repo"])
    if old_repo != new_repo:
        replace_all([
            "website/index.html", "website/_redirects", "website/servidor.html",
            "server/README.md", "server/instalar-servidor.sh", "README-VELODESK.md",
            "docs/velodesk/GUIA-PUBLICACION.md",
        ], [(old_repo, new_repo)])

    # 3. Nombre visible en cada plataforma y en los artefactos de la compilación
    if cur["name"] != new["name"]:
        o, n = cur["name"], new["name"]
        replace_all([
            "flutter/android/app/src/main/AndroidManifest.xml",
            "flutter/windows/runner/Runner.rc",
            "flutter/ios/Runner/Info.plist",
            "flutter/macos/Runner/Configs/AppInfo.xcconfig",
            ".github/workflows/flutter-build.yml",
            "website/index.html", "website/privacidad.html", "website/servidor.html", "website/_redirects",
            "server/README.md", "server/instalar-servidor.sh", "server/docker-compose.yml",
            "README-VELODESK.md",
        ], [(o, n)])

    # 4. Web
    if cur["site"] != new["site"]:
        replace_all(["README-VELODESK.md", "docs/velodesk/GUIA-PUBLICACION.md"], [(cur["site"], new["site"])])

    print("Hecho. Revisa `git diff` y publica una versión nueva para aplicar el cambio.")


if __name__ == "__main__":
    main()
