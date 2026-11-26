"""Name-hero thumbnail (1280x720): huge name on top, departure-board row, small document excerpt with one highlighted line.
Usage: python thumb_hero.py OUT.png "NAME" "BOARD WORD" "highlighted line" "doc header"
"""
import sys
from PIL import Image, ImageDraw
from render import F, paper, WHITE, RED, AMBER, MUTED, PAPER_INK

def main(out, name, board, hl, header):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(12 + 6 * t), int(22 - 8 * t), int(48 - 30 * t)))
    # name: two stacked lines on the left, block >= 40% of height
    parts = name.split(" ", 1) if " " in name else [name]
    size = 200
    while max(d.textlength(p_, font=F("head", size)) for p_ in parts) > 740: size -= 4
    y = 0
    for p_ in parts:
        for dx in (6, 4): d.text((40 + dx, y + dx), p_, font=F("head", size), fill=(0, 0, 0))
        d.text((40, y), p_, font=F("head", size), fill=WHITE); y += int(size * 1.0)
    # departure board row
    by = 470; d.rectangle([40, by, 760, by + 150], fill=(16, 16, 18))
    cf = F("monob", 96); x = 64
    for ch in board:
        d.rectangle([x - 6, by + 18, x + 58, by + 132], fill=(34, 34, 38))
        d.line([(x - 6, by + 75), (x + 58, by + 75)], fill=(10, 10, 12), width=3)
        d.text((x, by + 18), ch, font=cf, fill=AMBER); x += 72
    # document excerpt bottom-right
    x0, y0, x1, y1 = 810, 150, 1240, 520
    d = paper(img, (x0, y0, x1, y1), seed=5, tilt=0)
    d.text((x0 + 26, y0 + 24), header.upper(), font=F("monob", 22), fill=(110, 110, 115))
    for i, w in enumerate([360, 330, 380]):
        d.rectangle([x0 + 26, y0 + 80 + i * 40, x0 + 26 + w, y0 + 96 + i * 40], fill=(200, 195, 185))
    hf = 46
    while d.textlength(hl, font=F("serif", hf)) > 390: hf -= 2
    yy = y0 + 210
    d.rectangle([x0 + 20, yy - 6, x0 + 32 + d.textlength(hl, font=F("serif", hf)), yy + hf + 14], fill=(255, 214, 102))
    d.text((x0 + 26, yy), hl, font=F("serif", hf), fill=PAPER_INK)
    d.rectangle([x0 + 26, yy + 90, x0 + 300, yy + 106], fill=(200, 195, 185))
    d.rectangle([40, 690, 200, 698], fill=RED)
    img.save(out)

if __name__ == "__main__":
    main(*sys.argv[1:6])
