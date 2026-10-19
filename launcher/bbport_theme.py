"""Colours, type and the small vector drawings the launcher window is built from.

Everything here is presentation only: no settings, no files.  Keeping it in its
own module means the window code stays readable and the maths below can be
tested without opening a window.
"""

import math
import tkinter.font as tkfont

# Palette.  Names are kept from the first version of the window so the rest of
# the launcher (and its tests) can keep importing them.
BG = '#07060a'
PANEL = '#0f0d13'
CARD = '#191520'
CARD_HI = '#221c2b'
LINE = '#2a2431'
HAIRLINE = '#241f2b'
TEXT = '#ece5d8'
MUTED = '#8e8695'
GOLD = '#d8b46a'
GOLD_HI = '#f2d79c'
BLOOD = '#8a1a1a'
BLOOD_HI = '#c23a2f'
EMBER = '#d9743f'
NAV_HOVER = '#151119'
OK = '#8bbf9f'
WARN = '#d9a441'
BAD = '#d36b5c'

DISPLAY_FAMILIES = ('Cinzel', 'Trajan Pro', 'Constantia', 'Georgia', 'Times New Roman')
LATIN_FAMILIES = ('Segoe UI Variable Text', 'Segoe UI', 'Bahnschrift', 'Tahoma')
CJK_FAMILIES = ('Microsoft YaHei UI', 'Microsoft YaHei', 'SimHei', 'SimSun')
MONO_FAMILIES = ('Cascadia Mono', 'Consolas', 'Courier New')

CJK_LANGUAGES = ('zh', 'zh-hant', 'ja', 'ko')


# --- colours ---------------------------------------------------------------

def clamp(value, low=0.0, high=1.0):
    return low if value < low else high if value > high else value


def _parts(colour):
    colour = colour.lstrip('#')
    return [int(colour[i:i + 2], 16) for i in (0, 2, 4)]


def blend(first, second, t):
    """Colour `t` of the way from `first` to `second` (both `#rrggbb`)."""
    t = clamp(t)
    a, b = _parts(first), _parts(second)
    return '#%02x%02x%02x' % tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient(top, bottom, steps):
    """`steps` colours from `top` to `bottom`, both ends included."""
    steps = max(1, int(steps))
    if steps == 1:
        return [top]
    return [blend(top, bottom, i / (steps - 1)) for i in range(steps)]


def vertical(master, width, height, top, bottom):
    """A `width` x `height` PhotoImage fading from `top` to `bottom`.

    The fade is built as a one pixel wide column and then zoomed sideways,
    which is a hundred times cheaper than putting every pixel.
    """
    import tkinter

    width, height = max(1, int(width)), max(1, int(height))
    column = tkinter.PhotoImage(master=master, width=1, height=height)
    colours = gradient(top, bottom, height)
    for y, colour in enumerate(colours):
        column.put(colour, to=(0, y, 1, y + 1))
    return column.zoom(width, 1) if width > 1 else column


def tracked(text, gap=1):
    """Letters spaced out, because Tk has no letter-spacing."""
    if len(text) < 2:
        return text
    return (' ' * gap).join(text)


# --- type ------------------------------------------------------------------

def pick_family(available, candidates, fallback):
    for name in candidates:
        if name in available:
            return name
    return fallback


def fonts(tk, language='en', available=None):
    """Font families for this machine, preferring engraved serifs for display."""
    if available is None:
        try:
            available = set(tkfont.families(tk))
        except Exception:  # no window yet, or a stub in tests
            available = set()
    cjk = language in CJK_LANGUAGES
    body = pick_family(available, CJK_FAMILIES if cjk else LATIN_FAMILIES, 'TkDefaultFont')
    return {
        'display': pick_family(available, DISPLAY_FAMILIES, body),
        'body': body,
        'bold': body,
        'mono': pick_family(available, MONO_FAMILIES, 'TkFixedFont'),
        'cjk': cjk,
    }


# --- glyphs ----------------------------------------------------------------

def _line(canvas, x1, y1, x2, y2, colour, width):
    canvas.create_line(x1, y1, x2, y2, fill=colour, width=width, capstyle='round')


def _box(canvas, x, y, w, h, colour, width):
    canvas.create_rectangle(x, y, x + w, y + h, outline=colour, width=width)


def draw_glyph(canvas, name, x, y, size, colour, width=1):
    """Draw `name` inside the square at (x, y, size).  Returns the item ids."""
    s = size
    half = s / 2.0
    cx, cy = x + half, y + half
    items = []

    if name == 'play':
        items.append(canvas.create_polygon(
            x + s * 0.18, y + s * 0.10, x + s * 0.18, y + s * 0.90,
            x + s * 0.88, y + s * 0.50, fill=colour, outline=colour))
    elif name == 'graphics':
        items.append(canvas.create_oval(x + s * 0.18, y + s * 0.18,
                                        x + s * 0.82, y + s * 0.82,
                                        outline=colour, width=width))
        for i in range(8):
            angle = math.pi * 2 * i / 8
            items.append(canvas.create_line(
                cx + math.cos(angle) * s * 0.41, cy + math.sin(angle) * s * 0.41,
                cx + math.cos(angle) * s * 0.50, cy + math.sin(angle) * s * 0.50,
                fill=colour, width=width, capstyle='round'))
    elif name == 'display':
        items.append(_box(canvas, x + s * 0.10, y + s * 0.18, s * 0.80, s * 0.52, colour, width))
        _line(canvas, cx, y + s * 0.70, cx, y + s * 0.86, colour, width)
        _line(canvas, x + s * 0.30, y + s * 0.86, x + s * 0.70, y + s * 0.86, colour, width)
    elif name == 'game':
        items.append(canvas.create_oval(x + s * 0.16, y + s * 0.10,
                                        x + s * 0.84, y + s * 0.70,
                                        outline=colour, width=width))
        items.append(canvas.create_oval(x + s * 0.30, y + s * 0.32,
                                        x + s * 0.42, y + s * 0.44, fill=colour, outline=''))
        items.append(canvas.create_oval(x + s * 0.58, y + s * 0.32,
                                        x + s * 0.70, y + s * 0.44, fill=colour, outline=''))
        _line(canvas, x + s * 0.34, y + s * 0.70, x + s * 0.34, y + s * 0.84, colour, width)
        _line(canvas, x + s * 0.66, y + s * 0.70, x + s * 0.66, y + s * 0.84, colour, width)
    elif name == 'cheats':
        items.append(canvas.create_polygon(
            cx, y + s * 0.08,
            x + s * 0.80, y + s * 0.62,
            x + s * 0.62, y + s * 0.90,
            cx, y + s * 0.74,
            x + s * 0.38, y + s * 0.90,
            x + s * 0.20, y + s * 0.62,
            fill='', outline=colour, width=width))
    elif name == 'online':
        for dx, dy in ((0.50, 0.16), (0.20, 0.78), (0.80, 0.78)):
            items.append(canvas.create_oval(
                x + s * dx - s * 0.09, y + s * dy - s * 0.09,
                x + s * dx + s * 0.09, y + s * dy + s * 0.09,
                outline=colour, width=width))
        _line(canvas, x + s * 0.46, y + s * 0.26, x + s * 0.27, y + s * 0.68, colour, width)
        _line(canvas, x + s * 0.54, y + s * 0.26, x + s * 0.73, y + s * 0.68, colour, width)
        _line(canvas, x + s * 0.30, y + s * 0.78, x + s * 0.70, y + s * 0.78, colour, width)
    elif name == 'mods':
        items.append(canvas.create_polygon(
            cx, y + s * 0.10, x + s * 0.86, y + s * 0.30,
            x + s * 0.86, y + s * 0.70, cx, y + s * 0.90,
            x + s * 0.14, y + s * 0.70, x + s * 0.14, y + s * 0.30,
            fill='', outline=colour, width=width))
        _line(canvas, x + s * 0.14, y + s * 0.30, cx, y + s * 0.50, colour, width)
        _line(canvas, x + s * 0.86, y + s * 0.30, cx, y + s * 0.50, colour, width)
        _line(canvas, cx, y + s * 0.50, cx, y + s * 0.90, colour, width)
    elif name == 'trophies':
        # A cup: tapered body, two handles, stem and foot.  A plain arc read as a bow tie at 18 px.
        items.append(canvas.create_polygon(
            x + s * 0.28, y + s * 0.15, x + s * 0.72, y + s * 0.15,
            x + s * 0.66, y + s * 0.52, cx, y + s * 0.62,
            x + s * 0.34, y + s * 0.52, fill='', outline=colour, width=width, smooth=True))
        items.append(canvas.create_arc(x + s * 0.11, y + s * 0.20, x + s * 0.35, y + s * 0.46,
                                       start=95, extent=170, style='arc', outline=colour, width=width))
        items.append(canvas.create_arc(x + s * 0.65, y + s * 0.20, x + s * 0.89, y + s * 0.46,
                                       start=275, extent=170, style='arc', outline=colour, width=width))
        _line(canvas, cx, y + s * 0.62, cx, y + s * 0.79, colour, width)
        _line(canvas, x + s * 0.32, y + s * 0.85, x + s * 0.68, y + s * 0.85, colour, width)
        _line(canvas, cx, y + s * 0.79, cx, y + s * 0.85, colour, width)
    elif name == 'controls':
        items.append(canvas.create_rectangle(
            x + s * 0.08, y + s * 0.28, x + s * 0.92, y + s * 0.74,
            outline=colour, width=width))
        _line(canvas, x + s * 0.28, y + s * 0.51, x + s * 0.42, y + s * 0.51, colour, width)
        _line(canvas, x + s * 0.35, y + s * 0.44, x + s * 0.35, y + s * 0.58, colour, width)
        items.append(canvas.create_oval(x + s * 0.62, y + s * 0.44,
                                        x + s * 0.70, y + s * 0.52, fill=colour, outline=''))
        items.append(canvas.create_oval(x + s * 0.74, y + s * 0.54,
                                        x + s * 0.82, y + s * 0.62, fill=colour, outline=''))
    elif name == 'advanced':
        for i, knob in enumerate((0.34, 0.66, 0.46)):
            top = y + s * (0.28 + i * 0.22)
            _line(canvas, x + s * 0.10, top, x + s * 0.90, top, colour, width)
            items.append(canvas.create_oval(
                x + s * knob - s * 0.08, top - s * 0.08,
                x + s * knob + s * 0.08, top + s * 0.08,
                outline=colour, width=width))
    elif name == 'about':
        items.append(canvas.create_oval(x + s * 0.12, y + s * 0.12,
                                        x + s * 0.88, y + s * 0.88,
                                        outline=colour, width=width))
        items.append(canvas.create_oval(cx - s * 0.04, y + s * 0.26,
                                        cx + s * 0.04, y + s * 0.34,
                                        fill=colour, outline=''))
        _line(canvas, cx, y + s * 0.44, cx, y + s * 0.70, colour, width)
    elif name == 'log':
        items.append(canvas.create_rectangle(
            x + s * 0.20, y + s * 0.10, x + s * 0.80, y + s * 0.90,
            outline=colour, width=width))
        for row in (0.30, 0.46, 0.62, 0.78):
            _line(canvas, x + s * 0.30, y + s * row, x + s * 0.70, y + s * row, colour, width)
    else:
        items.append(canvas.create_oval(x + s * 0.20, y + s * 0.20,
                                        x + s * 0.80, y + s * 0.80,
                                        outline=colour, width=width))
    return items
