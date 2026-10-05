#!/usr/bin/env python3
"""MathType WMF equations -> LaTeX. v4

WMF -> SVG (wmf2svg) -> glyphs -> recursive spatial reconstruction:
  * Symbol font (Adobe Symbol encoding) -> LaTeX macros
  * script detection: small glyphs shifted up/down from the local baseline
    become ^{} / _{} attached to the nearest left token (or next big-op)
  * fraction bars -> \\frac with RECURSIVE num/den assembly
  * big bracket pairs ([ { ( ) } ]) -> bmatrix/cases/pmatrix, cells split
    by x-gaps, rows by y-clusters
"""
import re, os, subprocess, sys
from collections import defaultdict

SYMBOL_HIGH = {
    0xA5: r'\infty', 0xD6: r'\sqrt', 0xE5: r'\sum', 0xF2: r'\int',
    0xB1: r'\pm', 0xB4: r'\times', 0xB7: r'\cdot', 0xB8: r'*',
    0xCE: r'\in', 0xCF: r'\notin', 0xD1: r'\nabla', 0xB6: r'\partial',
    0xD9: r'\neq', 0xDB: r'\equiv', 0xDC: r'\approx', 0xDD: r'\cong',
    0xDE: r'\sim', 0xC3: r'\le', 0xC2: r'\ge', 0xAB: r'\leftarrow',
    0xA8: r'\uparrow', 0xAC: r'\rightarrow', 0xAD: r'\downarrow',
    0xAE: r'\leftrightarrow', 0xD8: r'\Leftrightarrow',
    0xDF: r'\Leftarrow', 0xE0: r'\Rightarrow',
    0xE1: r'\forall', 0xE2: r'\exists', 0xE3: r'\Re', 0xE4: r'\Im',
    0xEF: r'\angle', 0xF4: r'\langle', 0xF5: r'\rangle', 0xF7: r'\dots',
    0xA9: r'\cdot', 0xB0: r'\circ', 0xB9: r'\bullet',
    0xAA: r'\propto', 0xBC: r'\div', 0xBD: r'\diamond',
    0xBE: r'\neg', 0xBF: r'\wedge', 0xBB: r'\div',
    0xD7: r'\cdot', 0xA3: r'\le', 0xA2: r'\prime', 0x40: r'\cong',
}
SYMBOL_ASCII = {
    'a': r'\alpha', 'b': r'\beta', 'g': r'\gamma', 'd': r'\delta',
    'e': r'\epsilon', 'z': r'\zeta', 'h': r'\eta', 'q': r'\theta',
    'i': r'\iota', 'k': r'\kappa', 'l': r'\lambda', 'm': r'\mu',
    'n': r'\nu', 'x': r'\xi', 'p': r'\pi', 'r': r'\rho',
    's': r'\sigma', 't': r'\tau', 'u': r'\upsilon', 'f': r'\phi',
    'c': r'\chi', 'y': r'\psi', 'w': r'\omega',
    'G': r'\Gamma', 'D': r'\Delta', 'Q': r'\Theta', 'L': r'\Lambda',
    'X': r'\Xi', 'P': r'\Pi', 'S': r'\Sigma', 'U': r'\Upsilon',
    'F': r'\Phi', 'C': r'\Psi', 'W': r'\Omega',
    'j': r'\varphi', 'V': r'\varsigma',
}
BIG_OPS = {r'\int', r'\sum', r'\prod'}

LEFT_PIECES = {0xE9, 0xEA, 0xEB}
RIGHT_PIECES = {0xF9, 0xFA, 0xFB}
BLEFT_PIECES = {0xEC, 0xED, 0xEE}
BRIGHT_PIECES = {0xFC, 0xFD, 0xFE}
PLEFT_PIECES = {0xE5, 0xE6, 0xE7, 0xE8}
PRIGHT_PIECES = {0xF5, 0xF6, 0xF7, 0xF8}
ALL_BRACKETS = (LEFT_PIECES | RIGHT_PIECES | BLEFT_PIECES | BRIGHT_PIECES |
                PLEFT_PIECES | PRIGHT_PIECES)

def sym_char(ch):
    o = ord(ch)
    if o in ALL_BRACKETS:
        return ('BRACKET', o)
    if 0x20 <= o < 0x80:
        if ch in SYMBOL_ASCII:
            return SYMBOL_ASCII[ch]
        return ch
    return SYMBOL_HIGH.get(o, ch)

def glyph_latex(g):
    if 'Symbol' in g['font']:
        return ''.join(sym_char(c) for c in g['text'])
    return g['text']

def parse_svg(path):
    svg = open(path, 'rb').read().decode('latin1')
    glyphs = []
    pat = re.compile(
        r'<text x="0" y="0" style="font-family:([^;]+); font-style:([^;]+);'
        r' font-weight:([^;]+); font-size:([\d.]+)[^"]*"'
        r'[^>]*transform="matrix\(([-\d.eE]+) ([-\d.eE]+) ([-\d.eE]+) ([-\d.eE]+) '
        r'([-\d.eE]+) ([-\d.eE]+)\)"\s*>(.*?)</text>', re.S)
    for m in pat.finditer(svg):
        fam, fstyle, weight, size = m.group(1), m.group(2), m.group(3), float(m.group(4))
        tx, ty = float(m.group(9)), float(m.group(10))
        glyphs.append({'font': fam.strip(), 'style': fstyle.strip(),
                       'size': size, 'x': tx, 'y': ty, 'text': m.group(11)})
    bars = []
    for m in re.finditer(r'<line x1="([-\d.eE]+)" y1="([-\d.eE]+)" '
                         r'x2="([-\d.eE]+)" y2="([-\d.eE]+)"', svg):
        x1, y1, x2, y2 = map(float, m.groups())
        if abs(y1 - y2) < 3 and (x2 - x1) > 8:
            bars.append({'x1': x1, 'y': (y1 + y2) / 2, 'x2': x2})
    return glyphs, bars

def glyph_width(g):
    return g['size'] * 0.55 * max(1, len(g['text']))

def cluster_rows(glyphs, tol=0.30):
    rows = []
    for g in sorted(glyphs, key=lambda g: (g['y'], g['x'])):
        placed = False
        for row in rows:
            if abs(g['y'] - row['y']) < max(4, g['size'] * tol):
                row['glyphs'].append(g)
                placed = True
                break
        if not placed:
            rows.append({'y': g['y'], 'glyphs': [g]})
    for row in rows:
        ys = sorted(g['y'] for g in row['glyphs'])
        row['y'] = ys[len(ys) // 2]
    rows.sort(key=lambda r: r['y'])
    return rows

def space_macros(s):
    toks = re.split(r'(\\[A-Za-z]+)', s)
    out = []
    for i, t in enumerate(toks):
        if t.startswith('\\') and len(t) > 1 and t[1].isalpha():
            prev = out[-1][-1:] if out else ''
            if prev.isalnum():
                out.append(' ')
            out.append(t)
            nxt = toks[i + 1] if i + 1 < len(toks) else ''
            if nxt[:1].isalnum():
                out.append(' ')
        else:
            out.append(t)
    return ''.join(out)

def assemble(glyphs, bars, depth=0):
    """Recursively assemble a glyph set into LaTeX."""
    if not glyphs or depth > 4:
        return ''

    bset = [g for g in glyphs if g['text'] and all(ord(c) in ALL_BRACKETS
                                                   for c in g['text'])]
    b_ids = {id(g) for g in bset}
    normal = [g for g in glyphs if id(g) not in b_ids]
    if not normal:
        return ''

    sizes = [g['size'] for g in normal]
    smax = max(sizes)
    # main size: mode among the larger glyphs (ignore tiny script glyphs)
    big_sizes = [s for s in sizes if s >= smax * 0.75]
    main_size = max(set(big_sizes), key=big_sizes.count) if big_sizes else smax
    rows = cluster_rows(normal)

    big = lambda g: g['size'] >= main_size * 0.85
    main_row = max(rows, key=lambda r: (sum(1 for g in r['glyphs'] if big(g)),
                                        len(r['glyphs'])))
    main_y = main_row['y']

    roles = {}
    for row in rows:
        if row is main_row:
            roles[id(row)] = 'main'
            continue
        dy = row['y'] - main_y
        small = all(gg['size'] < main_size * 0.80 for gg in row['glyphs'])
        if small and dy < -main_size * 0.10:
            roles[id(row)] = 'sup'
        elif small and dy > main_size * 0.10:
            roles[id(row)] = 'sub'
        else:
            roles[id(row)] = 'main'

    # fractions (recurse into num/den)
    consumed = set()
    fracs = []
    for bar in bars:
        above = [g for g in normal if g['y'] < bar['y'] - 3 and
                 bar['x1'] - 30 <= g['x'] <= bar['x2'] + 30]
        below = [g for g in normal if g['y'] > bar['y'] + 3 and
                 bar['x1'] - 30 <= g['x'] <= bar['x2'] + 30]
        if not above or not below:
            continue
        num = assemble(above, [b for b in bars if b is not bar], depth + 1)
        den = assemble(below, [b for b in bars if b is not bar], depth + 1)
        if not num or not den:
            continue
        fracs.append(((bar['x1'] + bar['x2']) / 2, r'\frac{%s}{%s}' % (num, den)))
        for g in above + below:
            consumed.add(id(g))
    normal_left = [g for g in normal if id(g) not in consumed]

    # token stream
    stream = []  # (x, kind, latex, glyph)
    for row in rows:
        role = roles[id(row)]
        for g in sorted(row['glyphs'], key=lambda g: g['x']):
            if id(g) not in {id(x) for x in normal_left}:
                continue
            stream.append((g['x'], role, glyph_latex(g), g))
    for fx, flatex in fracs:
        stream.append((fx, 'frac', flatex, None))

    # bracket environments
    pairs = find_bracket_pairs(bset)
    for p in pairs:
        inner = [g for g in normal_left
                 if p['lx'] < g['x'] < p['rx']
                 and p['ymin'] - 30 <= g['y'] <= p['ymax'] + 10]
        if not inner:
            continue
        irows = cluster_rows(inner, tol=0.45)
        if len(irows) <= 1 and p['type'] == 'pmat':
            continue  # plain parenthesized group
        xs = sorted(g['x'] for g in inner)
        boundaries = [(a + b) / 2 for a, b in zip(xs, xs[1:]) if b - a > 45]
        rows_tex = []
        for row in irows:
            cells = defaultdict(str)
            for g in sorted(row['glyphs'], key=lambda g: g['x']):
                col = sum(1 for bd in boundaries if g['x'] > bd)
                cells[col] += glyph_latex(g)
            if cells:
                rows_tex.append(' & '.join(cells[k] for k in sorted(cells)))
        body = r' \\ '.join(rows_tex)
        env = {'bmat': 'bmatrix', 'cases': 'cases', 'pmat': 'pmatrix'}[p['type']]
        stream.append((p['lx'], 'env',
                       r'\begin{%s}%s\end{%s}' % (env, body, env), None))
        for g in inner:
            consumed.add(id(g))
    stream = [t for t in stream
              if t[3] is None or id(t[3]) not in consumed]
    stream.sort(key=lambda t: t[0])

    # attach scripts
    mains = [i for i, t in enumerate(stream) if t[1] in ('main', 'env', 'frac')]
    pending = defaultdict(list)
    for i, t in enumerate(stream):
        if t[1] not in ('sup', 'sub'):
            continue
        # 1) big-op overlap: script near a big operator's bbox attaches to it
        bigop = None
        for j, t2 in enumerate(stream):
            if t2[3] is None or t2[2].strip() not in BIG_OPS:
                continue
            w2 = glyph_width(t2[3])
            if t2[3]['x'] - w2 * 0.3 <= t[0] <= t2[3]['x'] + w2 * 1.3:
                bigop = j
                break
        if bigop is not None:
            pending[bigop].append((t[1], t[2]))
            stream[i] = (t[0], 'dead', '', None)
            continue
        best = None
        for j in mains:
            if j >= i:
                continue
            gj = stream[j][3]
            if gj is not None:
                right = gj['x'] + glyph_width(gj)
                if right <= t[0] + main_size * 0.9:
                    if best is None or stream[j][0] > stream[best][0]:
                        best = j
            else:
                if stream[j][0] <= t[0]:
                    if best is None or stream[j][0] > stream[best][0]:
                        best = j
        if best is None:
            # script LEFT of all tokens: attach to the NEXT big-op if any
            for j, t2 in enumerate(stream):
                if j > i and t2[1] in ('main', 'frac', 'env') and \
                   t2[2].strip() in BIG_OPS:
                    pending[j].append((t[1], t[2]))
                    stream[i] = (t[0], 'dead', '', None)
                    break
            else:
                stream[i] = (t[0], 'dead', t[2], None)  # drop orphan
        else:
            pending[best].append((t[1], t[2]))
            stream[i] = (t[0], 'dead', '', None)

    out = []
    for i, (x, kind, txt, g) in enumerate(stream):
        if kind == 'dead':
            if txt:
                out.append(txt)
            continue
        out.append(txt)
        scripts = pending.get(i)
        if scripts:
            sup = ''.join(s for k, s in scripts if k == 'sup').strip()
            sub = ''.join(s for k, s in scripts if k == 'sub').strip()
            is_big = txt.strip() in BIG_OPS or (
                kind == 'env' and any(op in txt for op in BIG_OPS))
            lim = r'\limits' if is_big else ''
            if sup:
                out.append('%s^{%s}' % (lim, sup))
            if sub:
                out.append('%s_{%s}' % (lim, sub))
    s = ''.join(out)
    s = space_macros(s)
    s = fix_macros(s)
    s = s.replace(' }', '}').replace('{ ', '{')
    s = re.sub(r'[ \t]+', ' ', s).strip()
    return s

def find_bracket_pairs(bset):
    lefts = [g for g in bset if ord(g['text'][0]) in
             LEFT_PIECES | BLEFT_PIECES | PLEFT_PIECES]
    rights = [g for g in bset if ord(g['text'][0]) in
              RIGHT_PIECES | BRIGHT_PIECES | PRIGHT_PIECES]
    pairs = []
    used_r = set()
    for lg in sorted(lefts, key=lambda g: -g['x']):
        best = None
        for rg in rights:
            if id(rg) in used_r or rg['x'] <= lg['x']:
                continue
            if abs(rg['y'] - lg['y']) < 60 and (best is None or rg['x'] < best['x']):
                best = rg
        if best is not None:
            used_r.add(id(best))
            o = ord(lg['text'][0])
            if o in LEFT_PIECES:
                btype = 'bmat'
            elif o in BLEFT_PIECES:
                btype = 'cases'
            else:
                btype = 'pmat'
            pairs.append({'lx': lg['x'], 'rx': best['x'],
                          'ymin': min(lg['y'], best['y']),
                          'ymax': max(lg['y'], best['y']) + lg['size'],
                          'type': btype})
    return pairs


KNOWN_MACROS = set("""alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta
iota kappa lambda mu nu xi pi varpi rho varrho sigma varsigma tau upsilon phi
varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega
frac sqrt sum int prod pm times cdot div neq le ge leq geq equiv approx cong
sim propto infty partial nabla left right begin end limits displaystyle
cos sin tan log ln exp det dim deg arg min max sup inf lim langle rangle
Rightarrow Leftarrow rightarrow leftarrow Leftrightarrow forall exists
Re Im angle dots ldots cdots vdots wedge vee neg bullet pm mp hbar
""".split())

def fix_macros(s):
    def repl(m):
        word = m.group(1)
        for L in range(len(word), 0, -1):
            if word[:L] in KNOWN_MACROS:
                rest = word[L:]
                return '\\' + word[:L] + (' ' + rest if rest else '')
        return m.group(0)
    return re.sub(r'\\([A-Za-z]+)', repl, s)

def wmf_to_latex(wmf_path, workdir='/tmp/pptx2beamer/eq_svg'):
    os.makedirs(workdir, exist_ok=True)
    svg_path = os.path.join(workdir, os.path.basename(wmf_path) + '.svg')
    if not os.path.exists(svg_path):
        r = subprocess.run(['wmf2svg', '-o', svg_path, wmf_path], capture_output=True)
        if r.returncode != 0:
            return None
    glyphs, bars = parse_svg(svg_path)
    if not glyphs:
        return None
    return assemble(glyphs, bars)

if __name__ == '__main__':
    print(wmf_to_latex(sys.argv[1]))
