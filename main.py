# The World Today — Sunday, 22 November 2026.
# A one-page newspaper front page drawn from scratch with Python's
# standard library only. No files are read, no network, no randomness:
# two runs write byte-identical PNGs.
#
# Stories (all verified against live reporting on 22 Nov 2026):
#  1. COP31 final draft goes to a vote in Antalya with no mention of
#     fossil fuels; 35% electrification goal for 2035; the $120bn
#     adaptation-finance target dropped; first COP text to admit the
#     world will overshoot 1.5C.
#  2. Russia fired 148 drones and 3 ballistic missiles at Ukraine
#     overnight 21-22 Nov: 2 killed, 83 wounded; Kryvyi Rih worst hit.
#  3. Ukrainian drones struck the Russian cargo ship Sparta II in the
#     Gulf of Finland; it drifted into Finnish waters.
#  4. Trump presses for a Ukraine deal by early January 2027 and is
#     preparing what he calls a large-scale ceasefire.
#  5. ATP Finals final tonight in Turin: Zverev v Alcaraz, 18:00 CET.
#  6. Also today: 4 killed in Gaza ceasefire breaches; US sanctions
#     14 Iranians over oil sales; tanker hit near Oman.

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (178, 34, 34)
SKY = (38, 52, 84)
GOLD = (201, 162, 39)
GREY = (120, 116, 108)
LIGHT = (232, 226, 214)

# ---------------------------------------------------------------- font
# A hand-drawn 5x7 bitmap font. Each glyph is 7 rows of 5 cells;
# '#' is ink, '.' is blank. Only the characters the page needs.

FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#..##", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '-': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".....", ".....", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '%': ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    '&': (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '$': ("..#..", ".####", "#.#.#", ".###.", "..#.#", "####.", "..#.."),
    'v': (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    '•': (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
    '—': (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}


def glyph(ch):
    return FONT.get(ch, FONT[' '])

# ---------------------------------------------------------------- canvas

class Page:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = col

    def rect(self, x, y, w, h, col):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, col)

    def frame(self, x, y, w, h, col, t=2):
        self.rect(x, y, w, t, col)
        self.rect(x, y + h - t, w, t, col)
        self.rect(x, y, t, h, col)
        self.rect(x + w - t, y, t, h, col)

    def hline(self, x, y, w, col, t=1):
        self.rect(x, y, w, t, col)

    def vline(self, x, y, h, col, t=1):
        self.rect(x, y, t, h, col)

    def disc(self, cx, cy, r, col):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.put(xx, yy, col)

    def ring(self, cx, cy, r, col, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d <= r * r:
                    self.put(xx, yy, col)

    def star(self, cx, cy, r, col):
        # An 8-point burst: a disc plus four long spikes.
        self.disc(cx, cy, r // 2, col)
        for k in range(8):
            import math
            a = k * math.pi / 4
            for s in range(r):
                xx = int(cx + s * math.cos(a))
                yy = int(cy + s * math.sin(a))
                self.put(xx, yy, col)
                self.put(xx + 1, yy, col)

    def text(self, x, y, s, scale, col):
        cx = x
        for ch in s:
            g = glyph(ch)
            for row in range(7):
                for bit in range(5):
                    if g[row][bit] == '#':
                        self.rect(cx + bit * scale, y + row * scale,
                                  scale, scale, col)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def centre(self, y, s, scale, col, x0=0, x1=None):
        x1 = self.w if x1 is None else x1
        w = self.text_w(s, scale)
        self.text(x0 + (x1 - x0 - w) // 2, y, s, scale, col)

    def para(self, x, y, w, lines, scale, col, gap=6):
        # lines: already-wrapped strings.
        for ln in lines:
            self.text(x, y, ln, scale, col)
            y += 7 * scale + gap
        return y


def wrap(s, max_chars):
    words = s.split(' ')
    lines, cur = [], ''
    for wd in words:
        trial = wd if not cur else cur + ' ' + wd
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- png

def write_png(page, path):
    raw = bytearray()
    stride = page.w * 3
    for y in range(page.h):
        raw.append(0)
        raw += page.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack('>I', len(data)) + tag + data
        return out + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', page.w, page.h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- layout

def draw_sun_factory(p, x, y, w, h):
    # A low sun over factory roofs, small smoke puffs from two stacks.
    # Everything stays inside the (x, y, w, h) panel: stacks and smoke
    # rise at most 50 px above the panel's base line.
    p.rect(x, y, w, h, LIGHT)
    p.disc(x + w - 52, y + 34, 26, GOLD)
    p.ring(x + w - 52, y + 34, 32, GOLD, 2)
    base = y + h - 26
    p.rect(x + 18, base - 24, 74, 24, INK)
    p.rect(x + 100, base - 34, 60, 34, INK)
    p.rect(x + 168, base - 18, 88, 18, INK)
    p.rect(x + 104, base - 46, 10, 12, INK)
    p.rect(x + 142, base - 42, 10, 8, INK)
    p.disc(x + 109, base - 44, 6, GREY)
    p.disc(x + 121, base - 44, 6, GREY)
    p.disc(x + 147, base - 42, 5, GREY)
    p.disc(x + 156, base - 44, 6, GREY)
    for wx in (34, 58, 116, 140, 186, 214):
        p.rect(x + wx, base - 16, 6, 6, PAPER)
    p.hline(x, base, w, INK, 3)


def draw_night_sky(p, x, y, w, h):
    # Dark sky, drone lights in a row, a burst over blocky rooftops.
    p.rect(x, y, w, h, SKY)
    for i in range(9):
        dx = x + 16 + i * 30
        dy = y + 22 + (i % 3) * 12
        p.disc(dx, dy, 3, GOLD)
        p.disc(dx, dy, 1, PAPER)
    p.star(x + w - 62, y + 62, 26, GOLD)
    p.star(x + w - 62, y + 62, 12, RED)
    base = y + h - 30
    for bx, bw, bh in ((8, 46, 30), (62, 38, 22), (108, 52, 30),
                       (168, 40, 20), (216, 46, 28)):
        p.rect(x + bx, base - bh, bw, bh, INK)
        p.rect(x + bx + 8, base - bh + 6, 6, 6, GOLD)
        p.rect(x + bx + bw - 16, base - bh + 6, 6, 6, GOLD)
    p.hline(x, base, w, INK, 3)


def draw_ship(p, x, y, w, h):
    # A compact cargo ship on the sea, with a red burst where it was
    # hit amidships. Everything stays inside the (x, y, w, h) panel.
    p.rect(x, y, w, h, LIGHT)
    sea = y + h - 16
    p.rect(x, sea, w, h - (sea - y), (90, 130, 170))
    p.rect(x + 24, sea - 12, 200, 12, INK)
    p.rect(x + 52, sea - 24, 30, 12, INK)
    p.rect(x + 56, sea - 21, 5, 5, PAPER)
    p.rect(x + 66, sea - 21, 5, 5, PAPER)
    p.rect(x + 140, sea - 20, 26, 8, INK)
    p.rect(x + 96, sea - 10, 6, 6, PAPER)
    p.star(x + 118, sea - 8, 12, RED)
    for wx in range(x + 12, x + w - 12, 34):
        p.hline(wx, sea + 6, 20, PAPER, 2)


def draw_ball(p, cx, cy, r):
    p.disc(cx, cy, r, (210, 220, 60))
    p.ring(cx, cy, r, INK, 2)
    for sgn in (-1, 1):
        for t in range(-r + 4, r - 3):
            xx = cx + sgn * (r - 8)
            yy = cy + t
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= (r - 3) ** 2:
                p.put(xx + (t * t) // (r * 2) * sgn, yy, PAPER)
                p.put(xx + (t * t) // (r * 2) * sgn + sgn, yy, PAPER)


def build():
    p = Page(W, H, PAPER)
    # Outer frame.
    p.frame(14, 14, W - 28, H - 28, INK, 3)

    # Masthead.
    p.centre(34, "THE WORLD TODAY", 6, INK)
    p.hline(34, 92, W - 68, INK, 2)
    p.text(34, 102, "WORLD EDITION", 2, INK)
    p.centre(102, "SUNDAY, 22 NOVEMBER 2026", 2, RED)
    p.text(W - 34 - p.text_w("ONE DAY, ONE PAGE", 2), 102,
           "ONE DAY, ONE PAGE", 2, INK)
    p.hline(34, 122, W - 68, INK, 5)

    # ---- Lead story: COP31, left column.
    lx, lw = 34, 622
    p.text(lx, 140, "CLIMATE SUMMIT  •  ANTALYA, TURKIYE", 2, RED)
    y = 166
    for ln in ("COP31 DEAL GOES", "TO VOTE WITHOUT", "A WORD ON", "FOSSIL FUELS"):
        p.text(lx, y, ln, 4, INK)
        y += 36
    y += 6
    deck = ("AFTER TWO DAYS IN OVERTIME, NEGOTIATORS WERE HANDED A "
            "FINAL TEXT IN THE EARLY HOURS OF SUNDAY. IT SETS A 35% "
            "ELECTRIFICATION GOAL FOR 2035, DROPS THE $120BN "
            "TARGET - AND NEVER NAMES FOSSIL FUELS. "
            "DELEGATES VOTE TODAY.")
    y = p.para(lx, y, lw, wrap(deck, 52), 2, INK, gap=5)
    y += 6
    draw_sun_factory(p, lx, y, lw, 76)

    # ---- Right column: Ukraine overnight.
    rx, rw = 682, 308
    p.vline(668, 140, 330, INK, 2)
    p.text(rx, 140, "WAR IN UKRAINE", 2, RED)
    y = 166
    for ln in ("NIGHT OF", "DRONES OVER", "UKRAINE"):
        p.text(rx, y, ln, 3, INK)
        y += 28
    y += 4
    deck2 = ("RUSSIA FIRED 148 DRONES AND 3 BALLISTIC MISSILES "
             "OVERNIGHT. AT LEAST 2 PEOPLE WERE KILLED AND 83 "
             "WOUNDED. KRYVYI RIH WAS HIT HARDEST: A BOY OF 7 "
             "AND A PARAMEDIC DIED THERE.")
    y = p.para(rx, y, rw, wrap(deck2, 25), 2, INK, gap=5)
    y += 4
    draw_night_sky(p, rx, y, rw, 96)

    # ---- Middle band: two stories.
    p.hline(34, 496, W - 68, INK, 3)
    my = 512
    # Left: Trump peace deadline.
    p.text(34, my, "PEACE TALKS", 2, RED)
    y = my + 26
    for ln in ("TRUMP PRESSES FOR", "UKRAINE DEAL BY", "EARLY JANUARY"):
        p.text(34, y, ln, 3, INK)
        y += 28
    y += 4
    deck3 = ("THE US PRESIDENT IS PREPARING WHAT HE CALLS A "
             "LARGE-SCALE CEASEFIRE, AS KYIV FORMS A EUROPEAN "
             "NEGOTIATING GROUP WITH POLAND, BRITAIN, GERMANY, "
             "FRANCE AND ITALY.")
    p.para(34, y, 440, wrap(deck3, 38), 2, INK, gap=5)
    # Right: Baltic ship.
    p.vline(512, 512, 200, INK, 2)
    p.text(530, my, "THE BALTIC SEA", 2, RED)
    y = my + 26
    for ln in ("SHIP HIT IN", "THE BALTIC"):
        p.text(530, y, ln, 3, INK)
        y += 28
    y += 4
    deck4 = ("UKRAINIAN DRONES HIT THE RUSSIAN CARGO SHIP "
             "SPARTA II IN THE GULF OF FINLAND. IT DRIFTED "
             "INTO FINNISH WATERS, HELSINKI SAID.")
    y = p.para(530, y, 440, wrap(deck4, 36), 2, INK, gap=5)
    y += 4
    draw_ship(p, 530, y, 440, 42)

    # ---- Sport band.
    p.hline(34, 748, W - 68, INK, 3)
    sy = 764
    p.text(34, sy, "SPORT  •  TURIN", 2, RED)
    p.text(34, sy + 26, "FINAL TONIGHT: ZVEREV v ALCARAZ", 3, INK)
    deck5 = ("WORLD NO. 1 ALEXANDER ZVEREV MEETS CARLOS ALCARAZ IN THE "
             "ATP FINALS TITLE MATCH AT 18:00 CET. ALCARAZ CHASES A "
             "FIRST TITLE ON A 13-MATCH WINNING RUN; ZVEREV CHASES "
             "A THIRD CROWN.")
    p.para(34, sy + 62, 800, wrap(deck5, 70), 2, INK, gap=5)
    draw_ball(p, 946, sy + 62, 40)

    # ---- Also today strip.
    p.hline(34, 896, W - 68, INK, 2)
    p.text(34, 910, "ALSO TODAY", 2, RED)
    strip = ("GAZA: 4 KILLED, 14 HURT IN CEASEFIRE BREACHES  •  "
             "US SANCTIONS 14 IRANIANS OVER OIL SALES  •  "
             "TANKER HIT BY PROJECTILE NEAR OMAN")
    p.para(34, 936, W - 68, wrap(strip, 76), 2, INK, gap=5)

    # Footer.
    p.hline(34, 972, W - 68, INK, 2)
    p.centre(982, "SUNDAY, 22 NOVEMBER 2026  —  THE WORLD TODAY", 2, INK)
    return p


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out_dir, exist_ok=True)
    page = build()
    path = os.path.join(out_dir, 'entry.png')
    n = write_png(page, path)
    print(f'wrote {path} {n} bytes {W}x{H}')


if __name__ == '__main__':
    main()
