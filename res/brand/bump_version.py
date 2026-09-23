#!/usr/bin/env python3
"""Sube la versión de VeloDesk en todos los archivos que la contienen.

    python res/brand/bump_version.py 1.5.3

Toca Cargo.toml, Cargo.lock (rustdesk y rustdesk-portable-packer), libs/portable/Cargo.toml,
flutter/pubspec.yaml (versión y número de build), los flujos de GitHub y los paquetes Linux.
Después: git commit, git tag <versión>, git push origin master <versión>.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("uso: bump_version.py X.Y.Z")
    new = sys.argv[1]
    cargo = ROOT / "Cargo.toml"
    cur = re.search(r'^version = "(\d+\.\d+\.\d+)"', cargo.read_text(encoding="utf-8"), re.M).group(1)
    if cur == new:
        sys.exit(f"Ya está en {new}")
    print(f"{cur} -> {new}")

    simple = [
        "Cargo.toml", "libs/portable/Cargo.toml",
        ".github/workflows/flutter-build.yml", ".github/workflows/playground.yml",
        "res/rpm-flutter-suse.spec", "res/rpm-flutter.spec", "res/rpm.spec", "res/PKGBUILD",
        "appimage/AppImageBuilder-aarch64.yml", "appimage/AppImageBuilder-x86_64.yml",
    ]
    pat = re.compile(r"\b" + re.escape(cur) + r"\b")
    for rel in simple:
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        n, count = pat.subn(new, s)
        if count:
            p.write_text(n, encoding="utf-8", newline="\n")
            print(f"  {rel}: {count}")

    # Cargo.lock: solo los paquetes del workspace que llevan la versión de la app
    lock = ROOT / "Cargo.lock"
    s = lock.read_text(encoding="utf-8")
    for pkg in ("rustdesk", "rustdesk-portable-packer"):
        old = f'name = "{pkg}"\nversion = "{cur}"\n'
        if old not in s:
            sys.exit(f"No encuentro {pkg} {cur} en Cargo.lock")
        s = s.replace(old, f'name = "{pkg}"\nversion = "{new}"\n')
    lock.write_text(s, encoding="utf-8", newline="\n")
    print("  Cargo.lock: rustdesk, rustdesk-portable-packer")

    # pubspec: versión + número de build incremental
    pub = ROOT / "flutter/pubspec.yaml"
    s = pub.read_text(encoding="utf-8")
    m = re.search(r"^version: (\d+\.\d+\.\d+)\+(\d+)$", s, re.M)
    build = int(m.group(2)) + 1
    s = s[:m.start()] + f"version: {new}+{build}" + s[m.end():]
    pub.write_text(s, encoding="utf-8", newline="\n")
    print(f"  flutter/pubspec.yaml: {new}+{build}")
    print("Listo. Ahora: git commit -am 'Versión", new, "' && git tag", new, "&& git push origin master", new)


if __name__ == "__main__":
    main()
