#!/usr/bin/env python3
"""Usuwa boczne etykiety cenowe Domel ze zdjęć produktów (kadr lewej części)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DIRS = [
    ROOT / "images" / "zdjecia_produktow",
    ROOT / "images" / "promocje",
    ROOT / "images" / "magazyn",
]


def col_brightness(im: Image.Image, x: int, h: int) -> float:
    vals = []
    for y in range(h // 4, 3 * h // 4, 8):
        p = im.getpixel((x, y))
        if isinstance(p, int):
            vals.append(float(p))
        else:
            vals.append(sum(p[:3]) / 3.0)
    return sum(vals) / max(len(vals), 1)


def find_split(im: Image.Image) -> int | None:
    """Szuka pionowego białego paska (etykieta po prawej)."""
    w, h = im.size
    if w < 400 or h < 400:
        return None
    # typowy układ: produkt | biała etykieta
    if w / h < 0.55:
        return None  # już wąskie – prawdopodobnie tylko produkt
    split = None
    for x in range(int(w * 0.35), int(w * 0.78)):
        if col_brightness(im, x, h) > 228 and col_brightness(im, min(x + 30, w - 1), h) > 228:
            split = max(int(w * 0.38), x - 4)
            break
    if split is None:
        return None
    # nie tnij jeśli „etykieta” to większość obrazu
    if split < w * 0.35 or split > w * 0.85:
        return None
    return split


def process_file(path: Path) -> bool:
    try:
        im = Image.open(path).convert("RGB")
    except Exception as e:
        print("  skip open", path.name, e)
        return False
    split = find_split(im)
    if not split:
        return False
    out = im.crop((0, 0, split, im.size[1]))
    # zachowaj rozsądne proporcje – nie zapisuj jeśli wynik absurdalnie wąski
    if out.size[0] < 200:
        return False
    out.save(path, "JPEG", quality=90, optimize=True)
    print(f"  cleaned {path.relative_to(ROOT)} -> {out.size[0]}x{out.size[1]}")
    return True


def main() -> None:
    changed = 0
    for base in DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            if path.name in {"logo.png", "a"}:
                continue
            if process_file(path):
                changed += 1
    print(f"Done. Cleaned {changed} images.")


if __name__ == "__main__":
    main()
