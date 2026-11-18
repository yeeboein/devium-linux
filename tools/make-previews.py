#!/usr/bin/env python3
"""Draw the theme previews for Devium Configure's Look and feel page: a little window and dock on the Devium
wallpaper, in each theme's colours.

Usage:  python3 tools/make-previews.py
Writes: profile/airootfs/usr/share/devium/previews/{devium,devium-light,devium-dark,base-kde}.png
Run it again after changing the wallpaper.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(os.path.dirname(HERE), "profile/airootfs")
WALL = os.path.join(A, "usr/share/wallpapers/Devium/contents/images/1920x1080.jpg")
OUT = os.path.join(A, "usr/share/devium/previews")
LOGO = os.path.join(A, "usr/share/devium/logo-white.png")
W, H, S = 320, 200, 3          # drawn 3x bigger, then scaled down for smooth edges

THEMES = {
    #               window     sidebar    text       bars       accent     dock bg         dots
    "devium":       ("#2b323b", "#232a32", "#eef2f7", "#8a93a6", "#8fb4d8", (36, 42, 50, 225), "devium"),
    "devium-light": ("#ecf0f4", "#dfe5ec", "#2b323b", "#4f5966", "#5f8fc0", (236, 240, 244, 225), "devium"),
    "devium-dark":  ("#181c22", "#12161b", "#eef2f7", "#788494", "#8fb4d8", (24, 28, 34, 225), "devium"),
    "base-kde":     ("#202326", "#1a1c1e", "#eef2f7", "#a0a8b0", "#3daee9", None, "kde"),
}
DOCK_ICONS = ["#8fb4d8", "#e8a07a", "#3a4250", "#8fd0d8", "#b4b8e0", "#9fd49a"]


def font(size):
    for f in ("/usr/share/fonts/noto/NotoSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def preview(name, theme):
    win, side, text, bars, accent, dock, kind = theme
    bg = Image.open(WALL).convert("RGB")
    # crop the wallpaper to 16:10 around the middle, like a laptop screen
    bw, bh = bg.size
    cw = int(bh * W / H)
    bg = bg.crop(((bw - cw) // 2, 0, (bw - cw) // 2 + cw, bh)) if cw <= bw else bg
    img = bg.resize((W * S, H * S), Image.LANCZOS).convert("RGBA")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = lambda v: int(v * S)  # noqa: E731

    # window shadow, then the window
    for i in range(6, 0, -1):
        d.rounded_rectangle([s(46 - i), s(26 - i + 4), s(274 + i), s(150 + i + 4)], radius=s(9 + i), fill=(0, 0, 0, 10))
    d.rounded_rectangle([s(46), s(26), s(274), s(150)], radius=s(9), fill=win)
    d.rounded_rectangle([s(52), s(48), s(112), s(144)], radius=s(5), fill=side)
    # title bar buttons
    cols = ["#e88a8a", "#e8c97a", "#9fd49a"] if kind != "kde" else ["#8a8f96", "#8a8f96", "#8a8f96"]
    for i, c in enumerate(cols):
        d.ellipse([s(229 + i * 13), s(31), s(237 + i * 13), s(39)], fill=c)
    # sidebar items, one selected
    for i, y in enumerate((60, 76, 98, 112)):
        if i == 1:
            d.rounded_rectangle([s(54), s(y - 4), s(110), s(y + 7)], radius=s(5), fill=accent)
        else:
            d.rounded_rectangle([s(58), s(y), s(100), s(y + 4)], radius=s(2), fill=bars)
    # text
    d.text((s(122), s(54)), "Hello, Devium", font=font(s(13)), fill=text)
    for i, (y, w) in enumerate(((76, 130), (91, 112), (105, 142), (119, 92))):
        d.rounded_rectangle([s(122), s(y), s(122 + w), s(y + 4)], radius=s(2), fill=bars)
    d.rounded_rectangle([s(212), s(126), s(265), s(140)], radius=s(6), fill=accent)

    if kind == "kde":
        # KDE's standard panel along the bottom
        d.rectangle([0, s(189), s(W), s(H)], fill=(32, 35, 38, 245))
        d.ellipse([s(6), s(191), s(19), s(199)], fill="#3daee9")
        for i, c in enumerate(["#c8ccd0", "#e8a07a", "#7aa8e8"]):
            d.rounded_rectangle([s(28 + i * 18), s(191), s(39 + i * 18), s(199)], radius=s(2), fill=c)
        d.text((s(284), s(190)), "12:00", font=font(s(8)), fill="#eef2f7")
    else:
        # the floating Devium dock: start button and app icons
        dw = 132
        x0 = (W - dw) // 2
        d.rounded_rectangle([s(x0), s(170), s(x0 + dw), s(194)], radius=s(10), fill=dock)
        if os.path.exists(LOGO):
            logo = Image.open(LOGO).convert("RGBA").resize((s(14), s(14)), Image.LANCZOS)
            if name == "devium-light":   # dark logo on the light dock
                r, g, b, a = logo.split()
                logo = Image.merge("RGBA", (r.point(lambda _: 70), g.point(lambda _: 80), b.point(lambda _: 96), a))
            layer.alpha_composite(logo, (s(x0 + 7), s(175)))
        for i, c in enumerate(DOCK_ICONS):
            d.rounded_rectangle([s(x0 + 27 + i * 17), s(175), s(x0 + 40 + i * 17), s(189)], radius=s(4), fill=c)

    img = Image.alpha_composite(img, layer)
    # rounded corners like the cards in Devium Configure
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=s(10), fill=255)
    img.putalpha(mask)
    img.resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name + ".png"), optimize=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, theme in THEMES.items():
        preview(name, theme)
    print("Previews written to", OUT)


if __name__ == "__main__":
    main()
