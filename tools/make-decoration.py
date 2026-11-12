#!/usr/bin/env python3
"""Make Devium's window decoration (KDE Aurorae theme): pastel macOS-style round buttons on the
left (close, minimise, maximise), a clean title bar in the Devium colours, rounded top corners.

Writes profile/airootfs/usr/share/aurorae/themes/Devium and Devium-Light."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "profile/airootfs/usr/share/aurorae/themes")

# pastel button colours: close, minimise, maximise
PASTEL = {"close": "#f4a7a7", "minimize": "#f6d8a2", "maximize": "#b9e2b9", "restore": "#b9e2b9"}
DARKER = {"close": "#e48888", "minimize": "#e9c480", "maximize": "#98cf98", "restore": "#98cf98"}
GLYPH = {   # small symbol shown on hover, drawn in a 16x16 box
    "close": '<path d="M5.2 5.2 L10.8 10.8 M10.8 5.2 L5.2 10.8" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/>',
    "minimize": '<path d="M4.8 8 L11.2 8" stroke="{c}" stroke-width="1.4" stroke-linecap="round"/>',
    "maximize": '<path d="M5 5 L5 9.5 L9.5 5 Z M11 11 L11 6.5 L6.5 11 Z" fill="{c}"/>',
    "restore": '<path d="M8 3.8 L8 8 L3.8 8 Z M8 12.2 L8 8 L12.2 8 Z" fill="{c}"/>',
}

THEMES = {
    "Devium": {"bar": "#2b323b", "bar_in": "#262c34", "edge": "#3a434e", "text": "220,227,234",
               "text_in": "130,140,152", "off": "#4a535e", "glyph": "#5a2e2e"},
    "Devium-Light": {"bar": "#eceff4", "bar_in": "#e4e8ee", "edge": "#cfd6df", "text": "20,24,29",
                     "text_in": "120,128,138", "off": "#c9d0d9", "glyph": "#5a2e2e"},
}


def button_svg(kind, t):
    """Aurorae button: one 16x16 element per state."""
    def circle(eid, fill, glyph="", ring=None):
        g = GLYPH[kind].format(c=t["glyph"]) if glyph else ""
        r = f' stroke="{ring}" stroke-width="0.6"' if ring else ""
        return (f'<g id="{eid}"><rect x="0" y="0" width="16" height="16" fill="none"/>'
                f'<circle cx="8" cy="8" r="6.2" fill="{fill}"{r}/>{g}</g>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">'
            + circle("active", PASTEL[kind], ring=DARKER[kind])
            + circle("hover", PASTEL[kind], glyph=True, ring=DARKER[kind])
            + circle("pressed", DARKER[kind], glyph=True)
            + circle("inactive", t["off"])
            + circle("deactivated", t["off"])
            + circle("hover-inactive", PASTEL[kind], glyph=True, ring=DARKER[kind])
            + circle("pressed-inactive", DARKER[kind], glyph=True)
            + '</svg>\n')


def decoration_svg(t):
    """Frame pieces (Plasma FrameSvg 'decoration' prefix): rounded top corners, thin edges."""
    R = 10   # corner radius
    def pieces(prefix, bar):
        e = t["edge"]
        return f'''
  <path id="{prefix}-topleft" d="M0 {R} A{R} {R} 0 0 1 {R} 0 L{R} 30 L0 30 Z" fill="{bar}"/>
  <rect id="{prefix}-top" x="{R}" y="0" width="10" height="30" fill="{bar}"/>
  <path id="{prefix}-topright" d="M{R + 10} 0 A{R} {R} 0 0 1 {2 * R + 10} {R} L{2 * R + 10} 30 L{R + 10} 30 Z" fill="{bar}"/>
  <rect id="{prefix}-left" x="0" y="30" width="1" height="10" fill="{e}"/>
  <rect id="{prefix}-center" x="1" y="30" width="28" height="10" fill="{bar}"/>
  <rect id="{prefix}-right" x="29" y="30" width="1" height="10" fill="{e}"/>
  <rect id="{prefix}-bottomleft" x="0" y="40" width="1" height="1" fill="{e}"/>
  <rect id="{prefix}-bottom" x="1" y="40" width="28" height="1" fill="{e}"/>
  <rect id="{prefix}-bottomright" x="29" y="40" width="1" height="1" fill="{e}"/>'''
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="30" height="82" viewBox="0 0 30 82">'
            + pieces("decoration", t["bar"])
            + pieces("decoration-inactive", t["bar_in"]).replace('y="30"', 'y="30"')
            + '\n</svg>\n')


RC = """[General]
ActiveTextColor={text}
InactiveTextColor={text_in}
TitleAlignment=Center
TitleVerticalAlignment=Center
Animation=120
UseTextShadow=false
HaloActive=false
HaloInactive=false

[Layout]
BorderLeft=1
BorderRight=1
BorderBottom=1
TitleEdgeTop=7
TitleEdgeBottom=7
TitleEdgeLeft=12
TitleEdgeRight=12
TitleBorderLeft=8
TitleBorderRight=8
TitleHeight=16
ButtonWidth=16
ButtonHeight=16
ButtonSpacing=8
ButtonMarginTop=0
ExplicitButtonSpacer=8
PaddingTop=0
PaddingBottom=0
PaddingLeft=0
PaddingRight=0
"""

META = """[Desktop Entry]
Name={name}
Comment=Pastel macOS-style window buttons in the Devium colours
X-KDE-PluginInfo-Author=Devium
X-KDE-PluginInfo-Name={name}
X-KDE-PluginInfo-Version=1.0
X-KDE-PluginInfo-License=GPL-3.0-or-later
X-KDE-PluginInfo-Website=https://github.com/yeeboein/devium-linux
"""


def main():
    for name, t in THEMES.items():
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "decoration.svg"), "w") as f:
            f.write(decoration_svg(t))
        for kind in ("close", "minimize", "maximize", "restore"):
            with open(os.path.join(d, f"{kind}.svg"), "w") as f:
                f.write(button_svg(kind, t))
        with open(os.path.join(d, f"{name}rc"), "w") as f:
            f.write(RC.format(**t))
        with open(os.path.join(d, "metadata.desktop"), "w") as f:
            f.write(META.format(name=name))
        print("made", d)


if __name__ == "__main__":
    main()
