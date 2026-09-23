#!/usr/bin/env python3
"""Genera el icono de VeloDesk en todos los formatos y tamaños que usa el proyecto.

    pip install pillow
    python res/brand/gen_icons.py

Diseño: cuadrado redondeado con degradado índigo → cian, una "V" blanca de trazo
grueso y tres líneas de velocidad. La misma geometría está en los SVG
(flutter/assets/icon.svg, res/logo.svg, res/logo-header.svg, website/icon.svg).

Archivos que escribe:
  res/icon.png, res/icon.ico, res/tray-icon.ico, res/mac-icon.png
  flutter/windows/runner/resources/app_icon.ico
  flutter/macos/Runner/AppIcon.icns
  flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset/*.png
  flutter/android/.../mipmap-*/ic_launcher*.png, ic_stat_logo.png, ic_launcher_background.xml
  flutter/assets/icon.png, logo.png, logo_light.png, logo_dark.png
  fastlane/metadata/android/en-US/images/icon.png
  website/icon.svg, website/icon-512.png
"""
import json
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
S = 4                      # supermuestreo para bordes suaves
N = 1024                   # tamaño base del icono
GRAD_A = (0x43, 0x38, 0xCA)  # índigo (arriba-izquierda)
GRAD_B = (0x06, 0xB6, 0xD4)  # cian (abajo-derecha)
BG_COLOR_HEX = "#3f5ae0"     # fondo del icono adaptativo de Android
NAME = "VeloDesk"


def gradient(size):
    """Degradado diagonal con un brillo suave arriba."""
    small = 256
    img = Image.new("RGB", (small, small))
    px = img.load()
    for y in range(small):
        for x in range(small):
            t = (x + y) / (2 * (small - 1))
            r = GRAD_A[0] + (GRAD_B[0] - GRAD_A[0]) * t
            g = GRAD_A[1] + (GRAD_B[1] - GRAD_A[1]) * t
            b = GRAD_A[2] + (GRAD_B[2] - GRAD_A[2]) * t
            glow = max(0.0, 1 - ((x - 60) ** 2 + (y - 40) ** 2) / (150 ** 2)) * 0.18
            px[x, y] = (int(min(255, r + 255 * glow)), int(min(255, g + 255 * glow)), int(min(255, b + 255 * glow)))
    return img.resize((size, size), Image.BICUBIC)


def rounded_mask(size, radius):
    m = Image.new("L", (size * S, size * S), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size * S - 1, size * S - 1], radius=radius * S, fill=255)
    return m.resize((size, size), Image.LANCZOS)


def draw_glyph(draw, scale=1.0, dx=0, dy=0, color=(255, 255, 255, 255), lines=True):
    """La V y las líneas de velocidad, en coordenadas de 1024 (se multiplican por S)."""
    def P(x, y):
        return ((x - 512) * scale + 512 + dx) * S, ((y - 512) * scale + 512 + dy) * S

    w = 118 * scale * S
    pts = [P(296, 318), P(512, 742), P(728, 318)]
    draw.line(pts, fill=color, width=int(w), joint="curve")
    for x, y in [(296, 318), (728, 318), (512, 742)]:
        cx, cy = P(x, y)
        r = w / 2
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    if lines:
        lw = 46 * scale * S
        c2 = (color[0], color[1], color[2], int(color[3] * 0.78))
        for y, x2 in [(380, 238), (470, 200), (560, 162)]:
            (ax, ay), (bx, by) = P(118, y), P(x2, y)
            draw.line([(ax, ay), (bx, by)], fill=c2, width=int(lw))
            for cx in (ax, bx):
                draw.ellipse([cx - lw / 2, ay - lw / 2, cx + lw / 2, ay + lw / 2], fill=c2)


def glyph_layer(scale=1.0, dx=0, dy=0, color=(255, 255, 255, 255), lines=True):
    layer = Image.new("RGBA", (N * S, N * S), (0, 0, 0, 0))
    draw_glyph(ImageDraw.Draw(layer), scale, dx, dy, color, lines)
    return layer.resize((N, N), Image.LANCZOS)


SOURCE = ROOT / "res/brand/icon-source.png"   # composición final (con el sello de Casara)


def full_icon(margin=0.0):
    """Icono completo. Si existe res/brand/icon-source.png se usa tal cual (recortado
    con esquinas redondeadas); si no, se dibuja el diseño procedural. margin = fracción
    transparente alrededor."""
    inner = int(N * (1 - 2 * margin))
    if SOURCE.exists():
        bg = Image.open(SOURCE).convert("RGBA").resize((inner, inner), Image.LANCZOS)
        bg.putalpha(rounded_mask(inner, int(inner * 0.219)))
    else:
        bg = gradient(inner).convert("RGBA")
        bg.putalpha(rounded_mask(inner, int(inner * 0.219)))
        g = glyph_layer().resize((inner, inner), Image.LANCZOS)
        bg.alpha_composite(g)
    out = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    off = (N - inner) // 2
    out.paste(bg, (off, off))
    return out


def circle_crop(img):
    m = Image.new("L", (img.width * S, img.height * S), 0)
    ImageDraw.Draw(m).ellipse([0, 0, img.width * S - 1, img.height * S - 1], fill=255)
    out = img.copy()
    out.putalpha(m.resize(img.size, Image.LANCZOS))
    return out


def save(img, rel, **kw):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p, **kw)
    print("  ", rel, img.size)


def wordmark(text_color, bg=None):
    """Logo horizontal: icono + 'VeloDesk'. 900x180 (la app lo muestra a 300x60 máx.)."""
    W, H = 900, 180
    img = Image.new("RGBA", (W * 2, H * 2), bg or (0, 0, 0, 0))
    icon = full_icon().resize((300, 300), Image.LANCZOS)
    img.paste(icon, (30, 30), icon)
    font = None
    for cand in [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if pathlib.Path(cand).exists():
            font = ImageFont.truetype(cand, 200)
            break
    if font is None:
        font = ImageFont.load_default()
    d = ImageDraw.Draw(img)
    x = 370
    d.text((x, 62), "Velo", font=font, fill=text_color)
    velo_w = d.textlength("Velo", font=font)
    d.text((x + velo_w, 62), "Desk", font=font, fill=(0x22, 0xB8, 0xD6, 255))
    return img.resize((W, H), Image.LANCZOS)


def main():
    print("Generando iconos de", NAME)
    icon = full_icon()
    mac = full_icon(margin=0.09)
    glyph = glyph_layer()

    # Fuentes principales
    save(icon, "res/icon.png")
    save(mac, "res/mac-icon.png")
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    save(icon, "res/icon.ico", format="ICO", sizes=sizes)
    save(icon, "flutter/windows/runner/resources/app_icon.ico", format="ICO", sizes=sizes)
    save(icon.resize((32, 32), Image.LANCZOS), "res/tray-icon.ico", format="ICO", sizes=[(32, 32)])

    # macOS
    save(mac, "flutter/macos/Runner/AppIcon.icns", format="ICNS")

    # iOS (sin transparencia)
    ios_dir = "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset"
    contents = json.loads((ROOT / ios_dir / "Contents.json").read_text())
    done = set()
    for entry in contents["images"]:
        fn = entry.get("filename")
        if not fn or fn in done:
            continue
        done.add(fn)
        pt = float(entry["size"].split("x")[0])
        px = int(round(pt * int(entry["scale"].rstrip("x"))))
        rgb = Image.new("RGB", (px, px), GRAD_A)
        rgb.paste(icon.resize((px, px), Image.LANCZOS), (0, 0), icon.resize((px, px), Image.LANCZOS))
        save(rgb, f"{ios_dir}/{fn}")

    # Android
    dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
    # Icono adaptativo: el icono completo dentro de la zona segura (66/108), así el sello se ve también en Android.
    fg = full_icon(margin=0.19)
    stat = glyph_layer(scale=1.0, lines=True)
    for d, k in dens.items():
        base = f"flutter/android/app/src/main/res/mipmap-{d}"
        s48 = int(48 * k)
        legacy = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        inner = full_icon(margin=0.04)
        legacy.alpha_composite(inner)
        save(legacy.resize((s48, s48), Image.LANCZOS), f"{base}/ic_launcher.png")
        save(circle_crop(full_icon()).resize((s48, s48), Image.LANCZOS), f"{base}/ic_launcher_round.png")
        s108 = int(108 * k)
        save(fg.resize((s108, s108), Image.LANCZOS), f"{base}/ic_launcher_foreground.png")
        s24 = int(24 * k)
        save(stat.resize((s24, s24), Image.LANCZOS).convert("LA"), f"{base}/ic_stat_logo.png")
    bgxml = ROOT / "flutter/android/app/src/main/res/values/ic_launcher_background.xml"
    bgxml.write_text(f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">{BG_COLOR_HEX}</color>\n</resources>\n', encoding="utf-8")
    print("  ", bgxml.relative_to(ROOT))

    # App Flutter (icono en la interfaz + logo horizontal)
    save(icon.resize((512, 512), Image.LANCZOS), "flutter/assets/icon.png")
    save(wordmark((0x0F, 0x17, 0x2A, 255)), "flutter/assets/logo.png")
    save(wordmark((0x0F, 0x17, 0x2A, 255)), "flutter/assets/logo_light.png")
    save(wordmark((255, 255, 255, 255)), "flutter/assets/logo_dark.png")

    # F-Droid / tiendas y web
    save(icon.resize((256, 256), Image.LANCZOS), "fastlane/metadata/android/en-US/images/icon.png")
    save(icon.resize((512, 512), Image.LANCZOS), "website/icon-512.png")
    save(wordmark((255, 255, 255, 255)), "website/logo-dark.png")
    save(wordmark((0x33, 0x41, 0x55, 255)), "res/logo-header.png")

    # SVG (misma geometría)
    svg_icon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4338ca"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>
<rect width="1024" height="1024" rx="224" fill="url(#g)"/>
<path d="M296 318 L512 742 L728 318" fill="none" stroke="#fff" stroke-width="118" stroke-linecap="round" stroke-linejoin="round"/>
<g stroke="#fff" stroke-opacity=".78" stroke-width="46" stroke-linecap="round"><path d="M118 380H238"/><path d="M118 470H200"/><path d="M118 560H162"/></g>
</svg>
"""
    for rel in ["flutter/assets/icon.svg", "res/logo.svg", "website/icon.svg"]:
        (ROOT / rel).write_text(svg_icon, encoding="utf-8")
        print("  ", rel)
    svg_header = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180" width="450" height="90">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4338ca"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>
<g transform="translate(15 15) scale(0.146484375)">
<rect width="1024" height="1024" rx="224" fill="url(#g)"/>
<path d="M296 318 L512 742 L728 318" fill="none" stroke="#fff" stroke-width="118" stroke-linecap="round" stroke-linejoin="round"/>
<g stroke="#fff" stroke-opacity=".78" stroke-width="46" stroke-linecap="round"><path d="M118 380H238"/><path d="M118 470H200"/><path d="M118 560H162"/></g>
</g>
<text x="190" y="128" font-family="Segoe UI, Inter, Roboto, Helvetica, Arial, sans-serif" font-weight="700" font-size="112"><tspan fill="#334155">Velo</tspan><tspan fill="#22b8d6">Desk</tspan></text>
</svg>
"""
    (ROOT / "res/logo-header.svg").write_text(svg_header, encoding="utf-8")
    print("   res/logo-header.svg")
    print("Listo.")


if __name__ == "__main__":
    main()
