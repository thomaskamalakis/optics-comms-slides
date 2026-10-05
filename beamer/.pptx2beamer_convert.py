#!/usr/bin/env python3
"""pptx -> Beamer converter for optics_comms2.pptx.

Reads slide XML directly, emits beamer .tex preserving:
- Greek text (xelatex + babel greek)
- run baseline (sub/superscripts) from PowerPoint
- bullet structure with levels
- images (png/jpeg + wmf pre-converted to png) with size/position heuristics
- text labels over images -> overlaid with picture environment
"""
import json, os, re, shutil, zipfile
from xml.etree import ElementTree as ET

PPTX = "/home/thomas/code/optics-slides/optics_comms2.pptx"
OUT_DIR = "/home/thomas/code/optics-slides/beamer"
MEDIA = "/tmp/pptx2beamer/media/ppt/media"
CONV = "/tmp/pptx2beamer/conv"  # wmf->png, gif->png conversions

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"a": A, "p": P, "r": R}

SYM = {
    "\uf050": r"\ensuremath{\rightarrow}",
    "\uf0ae": r"\ensuremath{\Rightarrow}",
    "\uf0c5": r"\ensuremath{\times}",
    "\uf0e5": r"\ensuremath{\infty}",
    "\uf0a5": r"\ensuremath{\infty}",
    "\uf040": r"\ensuremath{>}",
    "\uf0b4": r"\ensuremath{\times}",
    "\uf0d8": r"\ensuremath{\neq}",
    "\uf0b1": r"\ensuremath{\pm}",
    "\uf0b7": r"\ensuremath{\bullet}",
    "\uf0e0": r"\ensuremath{\Rightarrow}",
    "«": "“", "»": "”",
    "×": r"\ensuremath{\times}",
    "−": r"\ensuremath{-}",
    "≅": r"\ensuremath{\cong}",
    "≥": r"\ensuremath{\ge}",
    "≤": r"\ensuremath{\le}",
    "≠": r"\ensuremath{\neq}",
    "→": r"\ensuremath{\rightarrow}",
    "±": r"\ensuremath{\pm}",
    "∑": r"\ensuremath{\sum}",
    "∫": r"\ensuremath{\int}",
    "½": r"\ensuremath{\tfrac{1}{2}}",
    "µ": r"\ensuremath{\mu}",
    "š": r"\v{s}",
    "Ῑ": "Ι",
    # Greek letters -> math where meaningful in formulas; but keep text natural:
    # we do NOT map Greek letters globally (text is Greek prose).
}

GREEK_LETTER_FORMS = set("αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ")

def esc(s):
    s = s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%") \
        .replace("$", r"\$").replace("#", r"\#").replace("_", r"\_") \
        .replace("{", r"\{").replace("}", r"\}").replace("~", r"\textasciitilde{}") \
        .replace("^", r"\textasciicircum{}")
    for ch, rep in SYM.items():
        s = s.replace(ch, rep)
    return s

def txt_of_run(run):
    return "".join(t.text or "" for t in run.findall(f"{{{A}}}t"))

def run_latex(run):
    rPr = run.find(f"{{{A}}}rPr")
    t = txt_of_run(run)
    if not t:
        return ""
    baseline = 0
    b = i = False
    if rPr is not None:
        if rPr.get("baseline"):
            baseline = int(rPr.get("baseline"))
        b = rPr.get("b") == "1"
        i = rPr.get("i") == "1"
    core = esc(t)
    if b:
        core = r"\textbf{" + core + "}"
    if i:
        core = r"\textit{" + core + "}"
    if baseline < -12500:
        return r"$_{\text{" + core + "}}$"
    if baseline > 12500:
        return r"$^{\text{" + core + "}}$"
    return core

def merge_runs(runs):
    """Merge adjacent runs with identical effective formatting."""
    out = []
    for r in runs:
        rPr = r.find(f"{{{A}}}rPr")
        key = (rPr.get("b") if rPr is not None else None,
               rPr.get("i") if rPr is not None else None,
               rPr.get("baseline") if rPr is not None else None)
        if out and out[-1][0] == key:
            out[-1][1].append(r)
        else:
            out.append((key, [r]))
    return out

def para_latex(p):
    runs = p.findall(f"{{{A}}}r")
    parts = []
    for key, group in merge_runs(runs):
        txt = "".join(txt_of_run(r) for r in group)
        if not txt:
            continue
        b, i, baseline = key
        core = esc(txt)
        if b == "1":
            core = r"\textbf{" + core + "}"
        if i == "1":
            core = r"\textit{" + core + "}"
        if baseline:
            bl = int(baseline)
            if bl < -12500:
                core = r"$_{\text{" + core + "}}$"
            elif bl > 12500:
                core = r"$^{\text{" + core + "}}$"
        parts.append(core)
    s = "".join(parts).strip()
    s = smart_math(s)
    return s

def smart_math(s):
    # 10 + superscript(-n) produced by baseline runs
    s = re.sub(r"10\$\^\{\\text\{-(\d+)\}\}\$", r"10$^{-\1}$", s)
    s = re.sub(r"10\$\^\{\\text\{(\d+)\}\}\$", r"10$^{\1}$", s)
    # plain-text exponents
    s = re.sub(r"(?<![\w$\\])10-(\d+)\b", r"10$^{-\1}$", s)
    s = re.sub(r"(?<![\w$\\])2-(\d+)\b", r"2$^{-\1}$", s)
    s = re.sub(r"(?<![\w$\\])e-(\d+)\b", r"e$^{-\1}$", s)
    s = re.sub(r"(?<![\w$\\])3dB", r"3~dB", s)
    return s

def para_latex(p):
    parts = [run_latex(r) for r in p.findall(f"{{{A}}}r")]
    s = "".join(parts).strip()
    s = smart_math(s)
    return s

def para_level(p):
    pPr = p.find(f"{{{A}}}pPr")
    if pPr is None:
        return 0
    try:
        return int(pPr.get("lvl", "0") or 0)
    except ValueError:
        return 0

def para_has_bullet(p):
    """True if paragraph carries a visible bullet in pptx (buChar/buAutoNum,
    no buNone)."""
    pPr = p.find(f"{{{A}}}pPr")
    if pPr is None:
        return False
    if pPr.find(f"{{{A}}}buNone") is not None:
        return False
    return pPr.find(f"{{{A}}}buChar") is not None or pPr.find(f"{{{A}}}buAutoNum") is not None

z = zipfile.ZipFile(PPTX)
SLIDE_RE = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
slide_names = sorted((n for n in z.namelist() if SLIDE_RE.match(n)),
                     key=lambda n: int(SLIDE_RE.match(n).group(1)))

# pre-converted LaTeX for OLE equations (wmf name -> latex)
import json as _json
try:
    EQ_LATEX = _json.load(open("/tmp/pptx2beamer/eq_latex.json", encoding="utf-8"))
except FileNotFoundError:
    EQ_LATEX = {}

# ---- OLE equation objects: spid -> media file per slide (via vmlDrawing) ----
V = "urn:schemas-microsoft-com:vml"
O = "urn:schemas-microsoft-com:office:office"

def ole_map_for_slide(idx0):
    """Map graphicFrame spid -> media image name for OLE equation objects."""
    try:
        rels_xml = z.read(f"ppt/slides/_rels/slide{idx0+1}.xml.rels").decode("utf-8")
    except KeyError:
        return {}
    m = re.search(r'Target="\.\./drawings/(vmlDrawing\d+\.vml)"', rels_xml)
    if not m:
        return {}
    vml_name = m.group(1)
    # vml rels: rId -> media
    try:
        drels = z.read(f"ppt/drawings/_rels/{vml_name}.rels").decode("utf-8")
    except KeyError:
        return {}
    rid2media = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="\.\./media/([^"]+)"', drels))
    # vml shapes: spid -> (media, left_pt, top_pt, w_pt, h_pt)
    vml = z.read(f"ppt/drawings/{vml_name}").decode("utf-8")
    out = []
    for sm in re.finditer(r'<v:shape [^>]*id="(_x0000_s\d+)"[^>]*>(.*?)</v:shape>', vml, re.S):
        spid, body = sm.group(1), sm.group(2)
        rm = re.search(r'<v:imagedata[^>]*o:relid="(rId\d+)"', body)
        if not rm or rm.group(1) not in rid2media:
            continue
        st = re.search(r"style='([^']*)'", sm.group(0))
        left = top = w = h = None
        if st:
            for kv in st.group(1).split(";"):
                if ":" not in kv:
                    continue
                k, v = kv.split(":", 1)
                v = v.replace("pt", "")
                try:
                    if k == "left": left = float(v)
                    elif k == "top": top = float(v)
                    elif k == "width": w = float(v)
                    elif k == "height": h = float(v)
                except ValueError:
                    pass
        out.append({"spid": spid, "media": rid2media[rm.group(1)],
                    "left": left, "top": top, "w": w, "h": h})
    return out

def rels_map(idx0):
    rels = ET.fromstring(z.read(f"ppt/slides/_rels/slide{idx0+1}.xml.rels"))
    m = {}
    for rel in rels:
        m[rel.get("Id")] = rel.get("Target").replace("../media/", "")
    return m

def media_path(name):
    """Map media file name to usable image path (converted wmf/gif -> png)."""
    base, ext = os.path.splitext(name)
    if ext.lower() in (".wmf", ".gif"):
        cand = os.path.join(CONV, base + ".png")
        if os.path.exists(cand):
            return base + ".png"
    return name

def copy_media(name):
    """Copy media into OUT_DIR/images; return filename to use in tex."""
    base, ext = os.path.splitext(name)
    if ext.lower() in (".wmf", ".gif"):
        src = os.path.join(CONV, base + ".png")
        dst_name = base + ".png"
    else:
        src = os.path.join(MEDIA, name)
        dst_name = name
    dst = os.path.join(OUT_DIR, "images", dst_name)
    if not os.path.exists(dst):
        shutil.copy(src, dst)
    return dst_name

def xfrm_box(xfrm):
    off = xfrm.find(f"{{{A}}}off")
    ext = xfrm.find(f"{{{A}}}ext")
    return (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")))

EMU_PER_PT = 12700.0
SLIDE_W_EMU = 9144000
SLIDE_H_EMU = 6858000

def pct_width(cx):
    return 100.0 * cx / SLIDE_W_EMU

# ------------------------------------------------------------------ slide walk
def collect(idx0):
    root = ET.fromstring(z.read(f"ppt/slides/slide{idx0+1}.xml"))
    rels = rels_map(idx0)
    ole = ole_map_for_slide(idx0)
    title = None
    body_frames = []   # dicts: paras [(lvl, has_bullet, latex)], left, width
    images = []        # dicts: file, x, y, cx, cy
    eqs = []           # OLE equations: dicts: file, x, y, cx, cy, latex
    # document order via iter over spTree children
    tree = root.find(f"{{{P}}}cSld/{{{P}}}spTree")
    for el in tree:
        tag = el.tag
        if tag == f"{{{P}}}graphicFrame":
            # OLE equation object: spid -> media via vmlDrawing
            oleobj = el.find(f".//{{{P}}}oleObj")
            if oleobj is None:
                continue
            spid = oleobj.get("spid")
            media = None
            for cand in ole:
                if cand["spid"] == spid:
                    media = cand["media"]
                    break
            if media is None:
                continue
            xfrm = el.find(f"{{{P}}}xfrm")
            if xfrm is None:
                continue
            x, y, cx, cy = xfrm_box(xfrm)
            latex = EQ_LATEX.get(media)
            if latex:
                eqs.append({"file": None, "latex": latex,
                            "x": x, "y": y, "cx": cx, "cy": cy})
            else:
                fn = copy_media(media)
                eqs.append({"file": fn, "latex": None,
                            "x": x, "y": y, "cx": cx, "cy": cy})
            continue
        if tag == f"{{{P}}}sp":
            ph = el.find(f"{{{P}}}nvSpPr/{{{P}}}nvPr/{{{P}}}ph")
            ph_type = ph.get("type") if ph is not None else None
            tx = el.find(f"{{{P}}}txBody")
            xfrm = el.find(f".//{{{A}}}xfrm")
            box = xfrm_box(xfrm) if xfrm is not None else None
            paras = []
            if tx is not None:
                for p in tx.findall(f"{{{A}}}p"):
                    s = para_latex(p)
                    paras.append((para_level(p), para_has_bullet(p), s))
            if ph_type in ("title", "ctrTitle"):
                t = re.sub(r"\s+", " ", " ".join(s for _, _, s in paras if s)).strip()
                if not title:
                    title = t
                elif t:
                    body_frames.append({"paras": paras, "box": box, "label": True})
                continue
            if paras and any(s.strip() for _, _, s in paras):
                body_frames.append({"paras": paras, "box": box, "label": False})
        elif tag == f"{{{P}}}pic":
            blip = el.find(f".//{{{A}}}blip")
            xfrm = el.find(f".//{{{A}}}xfrm")
            embed = blip.get(f"{{{R}}}embed") if blip is not None else None
            if embed is None or xfrm is None:
                continue
            name = rels.get(embed)
            if not name:
                continue
            x, y, cx, cy = xfrm_box(xfrm)
            fn = copy_media(name)
            images.append({"file": fn, "x": x, "y": y, "cx": cx, "cy": cy})
    return title, body_frames, images, eqs

def classify(body_frames, images):
    """Split frames into main text vs overlay labels."""
    if not images:
        return body_frames, []
    main, labels = [], []
    for bf in body_frames:
        box = bf["box"]
        if box is None:
            main.append(bf)
            continue
        x, y, cx, cy = box
        # a label: narrow frame or overlapping image area substantially
        overlaps = any(not (x + cx < im["x"] or im["x"] + im["cx"] < x or
                            y + cy < im["y"] or im["y"] + im["cy"] < y) for im in images)
        small = cx < 0.35 * SLIDE_W_EMU and cy < 0.12 * SLIDE_H_EMU
        if (overlaps or small) and len(bf["paras"]) <= 3 and \
           sum(len(s) for _, _, s in bf["paras"]) < 220:
            labels.append(bf)
        else:
            main.append(bf)
    return main, labels

# ------------------------------------------------------------------ emit
def emit_itemgroup(paras, out):
    out.append(r"\begin{itemize}")
    for lvl, has_bullet, s in paras:
        if not s:
            continue
        env = "itemize" if has_bullet or lvl > 0 else "itemize"
        if lvl == 0 and not has_bullet and False:
            pass
        if lvl == 1:
            out.append(r"\item[] " + s if not has_bullet else r"\item " + s)
            # nested handled below
        out.append(r"\item " + s)
    out.append(r"\end{itemize}")

def emit_paras(paras, out):
    """Emit paragraphs as nested itemize lists following pptx levels.

    Simple recursive grouping: at each level, consecutive same-level
    paragraphs each become an \\item; a deeper-level run right after an
    item becomes its nested sub-list.
    """
    def emit(lo, hi, level, out):
        out.append(r"\begin{itemize}")
        k = lo
        while k < hi:
            if paras[k][0] != level:
                # deeper paragraph without a preceding same-level item:
                # emit as item at this level anyway (safety)
                out.append(r"\item " + paras[k][2])
                k += 1
                continue
            # the item itself
            out.append(r"\item " + paras[k][2])
            k += 1
            # gather the deeper-level run that follows this item
            sub_hi = k
            while sub_hi < hi and paras[sub_hi][0] > level:
                sub_hi += 1
            if sub_hi > k:
                # find the deepest starting level in the run (often level+1,
                # but pptx sometimes skips levels)
                run_lvls = [paras[j][0] for j in range(k, sub_hi)]
                start = min(run_lvls)
                emit(k, sub_hi, start, out)
                k = sub_hi
        out.append(r"\end{itemize}")

    i = 0
    n = len(paras)
    while i < n:
        lvl, hb, s = paras[i]
        if not s:
            i += 1
            continue
        if lvl <= 1:
            j = i
            while j < n and paras[j][0] <= 1 and paras[j][2]:
                j += 1
            emit(i, j, 0, out)
            i = j
        else:
            out.append(s + r"\par")
            i += 1

def fmt_dim(emu):
    return f"{emu / EMU_PER_PT:.1f}pt"

def image_height_pt(im):
    """Rendered height in pt for the width we'd assign (approx)."""
    return 0

def emit_image_block(images, labels, out, with_text=False):
    """Emit images sized to fit; when sharing the frame with text, bound height."""
    out.append(r"\begin{center}")
    # usable text width in pt (beamer 16:9, 11pt) ~ 398pt; height for images
    avail_h = 150.0 if with_text else 195.0
    avail_w = 398.0 * (0.95 if not with_text else 0.85)
    if len(images) == 1:
        im = images[0]
        ar = im["cx"] / max(im["cy"], 1)
        w = min(avail_w, avail_h * ar)
        out.append(r"\includegraphics[width=%.1fpt]{images/%s}" % (w, im["file"]))
    else:
        # lay out in a row, total width bounded, each also height-bounded
        ws = []
        total_ar = sum(im["cx"] / max(im["cy"], 1) for im in images)
        for im in images:
            ar = im["cx"] / max(im["cy"], 1)
            w = min(avail_w * ar / total_ar, avail_h * ar)
            ws.append(w)
        row = [r"\includegraphics[width=%.1fpt]{images/%s}" % (w, im["file"])
               for w, im in zip(ws, images)]
        out.append(" ".join(row))
    out.append(r"\end{center}")
    for lb in labels:
        for _, _, s in lb["paras"]:
            if s:
                out.append(r"\centering\footnotesize " + s + r"\par")

def overlay_labels(labels, images, out, with_text=False):
    """Place label texts over the image via a picture environment, height-bounded.
    Long captions (>55 chars) go below the image as centered text instead —
    absolute \put placement would overflow the right edge."""
    if not labels or not images:
        return
    base = max(images, key=lambda im: im["cx"] * im["cy"])
    bx0, by0 = base["x"], base["y"]
    avail_h = 150.0 if with_text else 182.0
    ar = base["cx"] / max(base["cy"], 1)
    target_pt = min(0.9 * 398.0, avail_h * ar)
    short_labels, captions = [], []
    for lb in labels:
        txt_len = sum(len(s) for _, _, s in lb["paras"] if s)
        (captions if txt_len > 55 else short_labels).append(lb)
    out.append(r"\begin{center}")
    out.append(r"\setlength{\unitlength}{%.6fpt}" % (target_pt / base["cx"]))
    out.append(r"\begin{picture}(%d,%d)" % (base["cx"], base["cy"]))
    out.append(r"\put(0,0){\includegraphics[width=%.1fpt]{images/%s}}" % (target_pt, base["file"]))
    for lb in short_labels:
        box = lb["box"]
        if box is None:
            continue
        x, y, cx, cy = box
        # center the label horizontally on its pptx box center
        center = x - bx0 + cx / 2.0
        # approximate rendered width: 0.55 * font-size per char, footnotesize ~8pt
        # in picture units: text width pt / unitlength
        unit = target_pt / base["cx"]
        est_w_units = (0.5 * 8.0 * sum(len(s) for _, _, s in lb["paras"] if s)) / unit
        px = max(0, min(int(base["cx"] - est_w_units), int(center - est_w_units / 2)))
        py = max(0, min(base["cy"], base["cy"] - (y + cy - by0)))
        txt = r"\shortstack{%s}" % r"\\".join(s for _, _, s in lb["paras"] if s)
        out.append(r"\put(%d,%d){\footnotesize %s}" % (px, py, txt))
    out.append(r"\end{picture}")
    out.append(r"\end{center}")
    for lb in captions:
        joined = " ".join(s for _, _, s in lb["paras"] if s)
        if joined:
            out.append(r"\centering\footnotesize " + joined + r"\par")

def build():
    os.makedirs(f"{OUT_DIR}/images", exist_ok=True)
    tex = []
    tex.append(r"""% Generated from optics_comms2.pptx
\documentclass[11pt,aspectratio=169]{beamer}
% --- format matched to ~/code/quantum-computing-slides (Libertinus + polyglossia)
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainfont{LibertinusSerif}[Extension=.otf, UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic, BoldItalicFont=*-BoldItalic]
\setmainlanguage{greek}
\setotherlanguage{english}
\usepackage{amsmath,amssymb}
\usepackage{bm}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usetheme{Madrid}
\usecolortheme{seahorse}
\usefonttheme{serif}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{blocks}[rounded][shadow=true]
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamerfont{title}{size=\Large,series=\bfseries}
\setbeamertemplate{itemize item}[triangle]
\setbeamertemplate{itemize subitem}[circle]
% tcolorbox style from the quantum lecture notes
\newtcolorbox{definitionbox}{
    enhanced, breakable, colback=gray!8, colframe=gray!60,
    fonttitle=\bfseries, boxrule=0.5pt, arc=2mm,
    left=2mm, right=2mm, top=1mm, bottom=1mm
}
\newtcolorbox{resultbox}{
    enhanced, breakable, colback=blue!5, colframe=blue!70!black,
    fonttitle=\bfseries, boxrule=0.8pt, arc=2mm,
    left=2mm, right=2mm, top=1mm, bottom=1mm
}
% top-align frames so sparse slides fill from the top
\AtBeginSection[]{\begin{frame}<beamer>\frametitle{Περιεχόμενα}\tableofcontents[currentsection]\end{frame}}

\title[Οπτικές Επικοινωνίες]{ΟΠΤΙΚΕΣ ΕΠΙΚΟΙΝΩΝΙΕΣ}
\author[Θ. Καμαλάκης]{Θωμάς Καμαλάκης}
\institute[ΧΠΑ]{Τμήμα Πληροφορικής και Τηλεματικής, Χαροκόπειο Πανεπιστήμιο}
\date{}

\begin{document}

\begin{frame}
\titlepage
\end{frame}
""")
    sections = 0
    for idx0 in range(len(slide_names)):
        title, body_frames, images, eqs = collect(idx0)
        # skip the duplicated title text on the cover slide (frame 0)
        if idx0 == 0:
            continue
        # section-header slides: Title Slide layout -> detect via first slide of deck & parts
        is_part = (idx0 in SECTION_IDX)
        if is_part:
            t = title or ""
            tex.append("")
            tex.append(r"\section{%s}" % t)
            tex.append(r"\begin{frame}")
            tex.append(r"\vfill")
            tex.append(r"\begin{center}")
            tex.append(r"{\Large\structure{%s}}" % t)
            tex.append(r"\end{center}")
            tex.append(r"\vfill")
            tex.append(r"\end{frame}")
            continue
        main, labels = classify(body_frames, images)
        # estimate content volume to pick shrink factor
        n_chars = sum(len(s) for bf in body_frames for _, _, s in bf["paras"])
        n_items = sum(1 for bf in body_frames for _, _, s in bf["paras"] if s)
        shrink = ""
        if n_chars > 700 or n_items > 11 or (images and n_chars > 200):
            shrink = "[shrink=20]"
        elif n_chars > 450 or n_items > 8 or images:
            shrink = "[shrink=10]"
        # equation stacks sharing the frame with images/text need more room
        if eqs and (images or n_chars > 100):
            shrink = "[shrink=20]"
        tex.append("")
        tex.append(r"\begin{frame}[%s%s]{%s}" % (shrink[1:-1] + "," if shrink else "", "t", title or ""))
        if main:
            # choose primary frame: most text
            prim = max(main, key=lambda bf: sum(len(s) for _, _, s in bf["paras"]))
            emit_paras(prim["paras"], tex)
            for bf in main:
                if bf is prim:
                    continue
                tex.append(r"\medskip")
                emit_paras(bf["paras"], tex)
        if images:
            has_text = bool(main and any(s for bf in main for _, _, s in bf["paras"]))
            if labels:
                overlay_labels(labels, images, tex, with_text=has_text)
            else:
                emit_image_block(images, labels, tex, with_text=has_text)
        if eqs:
            # OLE equations: arrange by vertical position (top-to-bottom rows)
            eqs_sorted = sorted(eqs, key=lambda e: (e["y"], e["x"]))
            tex.append(r"\begin{center}")
            # total rendered height estimate; cap each equation's height
            total_h = sum(e["cy"] for e in eqs_sorted) / EMU_PER_PT
            hcap = min(1.0, 185.0 / max(total_h, 1.0))
            # group into rows by y proximity
            rows = []
            for e in eqs_sorted:
                if rows and abs(e["y"] - rows[-1][0]["y"]) < 300000:
                    rows[-1].append(e)
                else:
                    rows.append([e])
            for row in rows:
                row_sorted = sorted(row, key=lambda e: e["x"])
                parts = []
                for e in row_sorted:
                    if e.get("latex"):
                        parts.append("$\\displaystyle %s$" % e["latex"])
                    else:
                        # scale equation to its pptx size (cx in pt), capped + hcap
                        wpt = min(e["cx"] / EMU_PER_PT, 180.0) * hcap
                        parts.append(r"\includegraphics[width=%.1fpt]{images/%s}" % (wpt, e["file"]))
                if parts:
                    tex.append(" ".join(parts) + r"\\[0.6ex]")
            tex.append(r"\end{center}")
        tex.append(r"\end{frame}")
    tex.append("")
    tex.append(r"\end{document}")
    with open(f"{OUT_DIR}/optics_comms2.tex", "w", encoding="utf-8") as f:
        f.write("\n".join(tex) + "\n")
    print("wrote", f"{OUT_DIR}/optics_comms2.tex", "slides:", len(slide_names))

# find Title Slide layout slides (section headers)
from pptx import Presentation
prs = Presentation(PPTX)
SECTION_IDX = [i for i, s in enumerate(prs.slides)
               if s.slide_layout.name == "Title Slide" and i > 0]
SECTION_IDX = set(SECTION_IDX)

if __name__ == "__main__":
    build()
