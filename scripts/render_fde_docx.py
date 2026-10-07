#!/usr/bin/env python3
"""Render a harness Markdown deliverable into a Factorial-branded .docx.

Usage:
    python3 scripts/render_fde_docx.py <content.md> <out.docx> [--base <any FDE-branded .docx>]

The base is any document on the FDE brand — by default the committed Feasibility Assessment
template, `templates/docx/2026MMDD_FDE-Feasibility-Assessment-IntegrationName_ClientName_Factorial.docx`,
which is itself rendered from `templates/feasibility-assessment.md`. Only its styles, embedded fonts,
numbering definitions, cover/page layout, header and footer are kept; its body is discarded and
replaced by the Markdown content, so the base's own text never leaks into the output.
Supported Markdown subset (see docs/branding.md §4):

  front matter (--- ... ---)   title, subtitle, prepared_for, external_system (fills the running header),
                               confidentiality (footer label), cover rows ("cover: Label :: line || line")
  <!-- toc -->                 table of contents (static entries; Word refreshes them with F9)
  # / ## / ###                 numbered Heading 1 / Heading 2, bold run-in Heading 3
  #! / ##!                     unnumbered Heading 1 / Heading 2 (appendices)
  paragraph                    body text; inline **bold**, _italic_, `mono`
  _whole line in italics_      author guidance (grey italic, to be deleted before sending)
  > **Title.** body            callout box (Radical Red rule, Glacier fill); several '>' lines join
  - item / 1. item             bullet / numbered list
  | a | b |  +  |---|---|      table; first row = header (Radical Red); write a literal pipe as a backslash followed by |. Optional directive line before it:
  <!-- widths: 500,1500,… size: 16 -->   column widths in DXA (sum 8730) and body font size (half-points)
  ---                          page break
"""
import argparse, os, re, shutil, sys, tempfile, zipfile
from xml.sax.saxutils import escape

MIDNIGHT, RED, GUIDE, FROST = "25253d", "ff355e", "666666", "f0f4f9"
TOTAL = 8730  # usable table width (DXA) between the base file's margins

# ----------------------------------------------------------------- inline
def _run(text, bold=False, italic=False, mono=False, color=MIDNIGHT, size=None):
    rpr = ""
    if mono:
        rpr += '<w:rFonts w:ascii="Roboto Mono" w:cs="Roboto Mono" w:eastAsia="Roboto Mono" w:hAnsi="Roboto Mono"/>'
    if bold:
        rpr += '<w:b w:val="1"/><w:bCs w:val="1"/>'
    if italic:
        rpr += '<w:i w:val="1"/><w:iCs w:val="1"/>'
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    return f'<w:r><w:rPr>{rpr}<w:rtl w:val="0"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'

INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`|(?<![\w{])_(?!_)[^_\n]+?_(?![\w}]))')

def inline(text, color=MIDNIGHT, size=None, italic=False):
    out = []
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(_run(part[2:-2], bold=True, italic=italic, color=color, size=size))
        elif part.startswith("`") and part.endswith("`"):
            out.append(_run(part[1:-1], mono=True, italic=italic, color=color, size=size))
        elif part.startswith("_") and part.endswith("_") and len(part) > 2:
            out.append(_run(part[1:-1], italic=True, color=color, size=size))
        else:
            out.append(_run(part, italic=italic, color=color, size=size))
    return "".join(out)

# ----------------------------------------------------------------- blocks
def para(text, after=200, color=MIDNIGHT, size=None, italic=False, line=276):
    return (f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="{line}" w:lineRule="auto"/><w:ind w:firstLine="0"/>'
            f'<w:jc w:val="left"/><w:rPr/></w:pPr>{inline(text, color=color, size=size, italic=italic)}</w:p>')

def guide(text):
    return para(text, after=160, color=GUIDE, size=20, italic=True)

def h1(text, numbered=True):
    num = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>' if numbered else '<w:ind w:left="0" w:firstLine="0"/>'
    return f'<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:widowControl w:val="1"/>{num}</w:pPr>{_run(text, color=None)}</w:p>'

def h2(text, numbered=True):
    num = ('<w:numPr><w:ilvl w:val="1"/><w:numId w:val="2"/></w:numPr><w:ind w:firstLine="450"/>' if numbered
           else '<w:ind w:left="0" w:firstLine="0"/>')
    return f'<w:p><w:pPr><w:pStyle w:val="Heading2"/>{num}<w:rPr/></w:pPr>{_run(text, color=None)}</w:p>'

def h3(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading3"/><w:rPr/></w:pPr>{_run(text, bold=True)}</w:p>'

NUM_LISTS = []  # numIds of numbered lists (each restarts at 1); registered in numbering.xml

def list_item(text, numbered=False, num_id=1):
    return (f'<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_id}"/></w:numPr>'
            f'<w:spacing w:after="80" w:line="276" w:lineRule="auto"/><w:rPr/></w:pPr>{inline(text)}</w:p>')

def _borders(color=MIDNIGHT, sz=4, sides=("top", "left", "bottom", "right")):
    return "".join(f'<w:{s} w:color="{color}" w:space="0" w:sz="{sz}" w:val="single"/>' for s in sides)

def _cell(xml, width, fill=None, sz=4):
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/><w:tcBorders>{_borders(sz=sz)}</w:tcBorders>'
    if fill:
        tcpr += f'<w:shd w:fill="{fill}" w:val="clear"/>'
    tcpr += ('<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
             '<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>')
    return f'<w:tc><w:tcPr>{tcpr}</w:tcPr>{xml}</w:tc>'

def cell_para(text, color=MIDNIGHT, size=18, italic=False):
    return (f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/><w:rPr/></w:pPr>'
            f'{inline(text, color=color, size=size, italic=italic)}</w:p>')

def table(header, rows, widths, size=18):
    n = len(header)
    if not widths:
        widths = [TOTAL // n] * n
        widths[-1] += TOTAL - sum(widths)
    if sum(widths) != TOTAL:
        raise SystemExit(f"table widths must sum to {TOTAL}, got {sum(widths)}: {header}")
    if len(widths) != n:
        raise SystemExit(f"table has {n} columns but {len(widths)} widths: {header}")
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    tblpr = (f'<w:tblPr><w:tblW w:w="{TOTAL}" w:type="dxa"/><w:jc w:val="left"/><w:tblInd w:w="0" w:type="dxa"/>'
             f'<w:tblBorders>{_borders()}{_borders(sides=("insideH", "insideV"))}</w:tblBorders>'
             '<w:tblLayout w:type="fixed"/><w:tblLook w:val="0600"/></w:tblPr>')
    out = [f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>',
           '<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="1"/></w:trPr>']
    out += [_cell(cell_para(f"**{h}**", color="ffffff", size=size), w, fill=RED) for h, w in zip(header, widths)]
    out.append('</w:tr>')
    for r in rows:
        r = (r + [""] * n)[:n]
        out.append('<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>')
        out += [_cell(cell_para(c, size=size), w) for c, w in zip(r, widths)]
        out.append('</w:tr>')
    out.append('</w:tbl>' + para("", after=120))
    return "".join(out)

def callout(title, body):
    tcpr = (f'<w:tcW w:w="{TOTAL}" w:type="dxa"/><w:tcBorders><w:top w:val="nil"/>'
            f'<w:left w:color="{RED}" w:space="0" w:sz="24" w:val="single"/><w:bottom w:val="nil"/><w:right w:val="nil"/></w:tcBorders>'
            f'<w:shd w:fill="{FROST}" w:val="clear"/><w:tcMar><w:top w:w="120" w:type="dxa"/><w:left w:w="200" w:type="dxa"/>'
            '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>')
    inner = ""
    if title:
        inner += f'<w:p><w:pPr><w:spacing w:after="60" w:line="259" w:lineRule="auto"/><w:rPr/></w:pPr>{_run(title, bold=True, size=20)}</w:p>'
    inner += f'<w:p><w:pPr><w:spacing w:after="0" w:line="259" w:lineRule="auto"/><w:rPr/></w:pPr>{inline(body, size=20)}</w:p>'
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{TOTAL}" w:type="dxa"/><w:jc w:val="left"/><w:tblInd w:w="0" w:type="dxa"/>'
            '<w:tblBorders><w:top w:val="nil"/><w:left w:val="nil"/><w:bottom w:val="nil"/><w:right w:val="nil"/>'
            '<w:insideH w:val="nil"/><w:insideV w:val="nil"/></w:tblBorders><w:tblLayout w:type="fixed"/><w:tblLook w:val="0000"/></w:tblPr>'
            f'<w:tblGrid><w:gridCol w:w="{TOTAL}"/></w:tblGrid><w:tr><w:tc><w:tcPr>{tcpr}</w:tcPr>{inner}</w:tc></w:tr></w:tbl>'
            + para("", after=120))

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def toc(entries):
    out = ['<w:sdt><w:sdtPr><w:docPartObj><w:docPartGallery w:val="Table of Contents"/><w:docPartUnique w:val="1"/></w:docPartObj></w:sdtPr><w:sdtContent>']
    first = True
    for lvl, text in entries:
        p = ('<w:p><w:pPr><w:widowControl w:val="0"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8640"/></w:tabs>'
             f'<w:spacing w:after="0" w:before="{80 if lvl == 1 else 40}" w:line="240" w:lineRule="auto"/>'
             f'<w:ind w:left="{0 if lvl == 1 else 360}"/><w:jc w:val="left"/><w:rPr/></w:pPr>')
        if first:
            p += ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\h \\u \\z \\t '
                  '&quot;Heading 1,1,Heading 2,2&quot;</w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>')
            first = False
        p += _run(text, bold=(lvl == 1), size=20 if lvl == 1 else 18) + '<w:r><w:tab/></w:r></w:p>'
        out.append(p)
    out.append('<w:p><w:pPr><w:spacing w:after="0"/><w:rPr/></w:pPr><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>')
    return "".join(out)

# ----------------------------------------------------------------- cover
SECT = ('<w:sectPr><w:headerReference r:id="rId6" w:type="default"/><w:headerReference r:id="rId7" w:type="first"/>'
        '<w:footerReference r:id="rId8" w:type="default"/><w:footerReference r:id="rId9" w:type="first"/>'
        '<w:pgSz w:h="16834" w:w="11909" w:orient="portrait"/>'
        '<w:pgMar w:bottom="1699" w:top="2260" w:left="1526" w:right="1584" w:header="566" w:footer="720"/>'
        '<w:pgNumType w:start="1"/><w:titlePg w:val="1"/></w:sectPr>')

def cover(meta):
    x = [('<w:p><w:pPr><w:pStyle w:val="Title"/><w:spacing w:after="0" w:lineRule="auto"/><w:ind w:left="0" w:right="384" w:firstLine="0"/>'
          f'<w:jc w:val="left"/><w:rPr/></w:pPr>{inline(meta.get("title", "Untitled"))}</w:p>')]
    if meta.get("subtitle"):
        x.append('<w:p><w:pPr><w:pStyle w:val="Subtitle"/><w:ind w:left="0" w:firstLine="0"/><w:rPr><w:b w:val="1"/><w:bCs w:val="1"/>'
                 f'<w:color w:val="25253d"/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr></w:pPr>{_run(meta["subtitle"], color=None)}</w:p>')
    if meta.get("prepared_for"):
        x.append(f'<w:p><w:pPr><w:rPr/></w:pPr>{_run("Prepared for:", bold=True, size=36)}</w:p>')
        x.append(f'<w:p><w:pPr><w:rPr/></w:pPr>{_run(meta["prepared_for"] + " ", size=36)}</w:p>')
    rows = meta.get("cover", [])
    if rows:
        tbl = (f'<w:tbl><w:tblPr><w:tblW w:w="{TOTAL}" w:type="dxa"/><w:jc w:val="left"/><w:tblInd w:w="21" w:type="dxa"/>'
               f'<w:tblBorders>{_borders(sz=8)}{_borders(sz=8, sides=("insideH", "insideV"))}</w:tblBorders>'
               '<w:tblLayout w:type="fixed"/><w:tblLook w:val="0600"/></w:tblPr><w:tblGrid><w:gridCol w:w="2775"/><w:gridCol w:w="5955"/></w:tblGrid>')
        for label, lines in rows:
            c1 = _cell(cell_para(f"**{label}**", size=20), 2775, sz=8)
            body = "".join(f'<w:p><w:pPr><w:spacing w:after="100" w:line="276" w:lineRule="auto"/><w:jc w:val="left"/><w:rPr/></w:pPr>'
                           f'{inline(l, size=20)}</w:p>' for l in lines)
            c2 = f'<w:tc><w:tcPr><w:tcW w:w="5955" w:type="dxa"/><w:tcBorders>{_borders(sz=8)}</w:tcBorders></w:tcPr>{body}</w:tc>'
            tbl += f'<w:tr><w:trPr><w:cantSplit w:val="0"/><w:tblHeader w:val="0"/></w:trPr>{c1}{c2}</w:tr>'
        x.append(tbl + '</w:tbl>')
    x.append(f'<w:p><w:pPr><w:jc w:val="left"/><w:rPr/>{SECT}</w:pPr><w:r><w:rPr><w:rtl w:val="0"/></w:rPr></w:r></w:p>')
    return "".join(x)

# ----------------------------------------------------------------- parser
def parse(md):
    meta, body_lines = {}, md.splitlines()
    if body_lines and body_lines[0].strip() == "---":
        end = body_lines.index("---", 1)
        for line in body_lines[1:end]:
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "cover":
                label, _, rest = v.partition("::")
                meta.setdefault("cover", []).append((label.strip(), [s.strip() for s in rest.split("||")]))
            else:
                meta[k] = v
        body_lines = body_lines[end + 1:]
    blocks, toc_entries, i, n = [], [], 0, len(body_lines)
    h1n = h2n = 0
    pending = {}
    next_num = [900000]  # provisional numIds, remapped above the base file's own ids at assembly time

    def push(block):
        nonlocal pending
        if block[0] != "table" and not (block[0] == "li" and block[1][1]):
            pending = {}  # a widths directive applies only to the table that immediately follows it
        blocks.append(block)
    while i < n:
        line = body_lines[i].rstrip()
        s = line.strip()
        if not s:
            i += 1; continue
        if s == "<!-- toc -->":
            push(("toc", None)); i += 1; continue
        m = re.match(r'<!--\s*widths:\s*([\d,\s]+?)\s*(?:size:\s*(\d+))?\s*-->', s)
        if m:
            pending = {"widths": [int(w) for w in m.group(1).split(",")], "size": int(m.group(2) or 18)}
            i += 1; continue
        if s == "---":
            push(("pb", None)); i += 1; continue
        m = re.match(r'(#{1,6})(!?)\s+(.*)', s) if s.startswith("#") else None
        if m:
            level, unnumbered, text = min(len(m.group(1)), 3), bool(m.group(2)), m.group(3).strip()
            if level == 1:
                if unnumbered:
                    toc_entries.append((1, text))
                else:
                    h1n += 1; h2n = 0; toc_entries.append((1, f"{h1n}. {text}"))
                push(("h1", (text, not unnumbered)))
            elif level == 2:
                if unnumbered:
                    toc_entries.append((2, text))
                else:
                    h2n += 1; toc_entries.append((2, f"{h1n}.{h2n} {text}"))
                push(("h2", (text, not unnumbered)))
            else:
                push(("h3", text))
            i += 1; continue
        if s.startswith(">"):
            parts = []
            while i < n and body_lines[i].strip().startswith(">"):
                parts.append(body_lines[i].strip()[1:].strip()); i += 1
            text = " ".join(p for p in parts if p)
            m = re.match(r'\*\*(.+?)\*\*\s*(.*)', text, re.S)
            push(("callout", (m.group(1), m.group(2)) if m else ("", text)))
            continue
        if s.startswith("|"):
            rows = []
            while i < n and body_lines[i].strip().startswith("|"):
                row = body_lines[i].strip().strip("|")
                cells = [c.strip().replace("\x00", "|") for c in row.replace("\\|", "\x00").split("|")]
                rows.append(cells); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c or '-') for c in r)]
            push(("table", (rows[0], rows[1:], pending.get("widths"), pending.get("size", 18))))
            pending = {}
            continue
        if re.match(r'[-*]\s+', s):
            push(("li", (s[2:].strip(), False, 1))); i += 1; continue
        if re.match(r'\d+[.)]\s+', s):
            if not (blocks and blocks[-1][0] == "li" and blocks[-1][1][1]):
                next_num[0] += 1; NUM_LISTS.append(next_num[0])
            push(("li", (re.sub(r'^\d+[.)]\s+', '', s), True, next_num[0]))); i += 1; continue
        # paragraph: join continuation lines
        parts = [s]
        i += 1
        while i < n and body_lines[i].strip() and not re.match(r'(#|>|\||[-*]\s|\d+[.)]\s|<!--|---$)', body_lines[i].strip()):
            parts.append(body_lines[i].strip()); i += 1
        text = " ".join(parts)
        if re.fullmatch(r'_[^_].*[^_]_', text) and "**" not in text:
            push(("guide", text[1:-1]))
        else:
            push(("p", text))
    return meta, blocks, toc_entries

def render(meta, blocks, toc_entries):
    out = []
    for kind, v in blocks:
        if kind == "toc":
            out.append('<w:p><w:pPr><w:pStyle w:val="Title"/><w:ind w:left="0" w:firstLine="0"/><w:rPr><w:color w:val="25253d"/></w:rPr></w:pPr>'
                       + _run("Table of Contents") + '</w:p>')
            out.append(guide("Right-click the table → Update field (or select it and press F9) to refresh the entries and page numbers after editing."))
            out.append(toc(toc_entries))
        elif kind == "pb": out.append(page_break())
        elif kind == "h1": out.append(h1(v[0], v[1]))
        elif kind == "h2": out.append(h2(v[0], v[1]))
        elif kind == "h3": out.append(h3(v))
        elif kind == "callout": out.append(callout(*v))
        elif kind == "table": out.append(table(*v))
        elif kind == "li": out.append(list_item(v[0], v[1], v[2]))
        elif kind == "guide": out.append(guide(v))
        else: out.append(para(v))
    return "".join(out)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("content"); ap.add_argument("out")
    ap.add_argument("--base", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates", "docx",
                                                  "2026MMDD_FDE-Feasibility-Assessment-IntegrationName_ClientName_Factorial.docx"))
    a = ap.parse_args()
    meta, blocks, toc_entries = parse(open(a.content, encoding="utf-8").read())
    work = tempfile.mkdtemp()
    with zipfile.ZipFile(a.base) as z:
        z.extractall(work)
    docxml = os.path.join(work, "word", "document.xml")
    d = open(docxml, encoding="utf-8").read()
    head = d[:d.find("<w:body>") + len("<w:body>")]
    final = re.search(r'<w:sectPr>(?:(?!<w:sectPr>).)*</w:sectPr>\s*</w:body>', d, re.S).group(0)
    open(docxml, "w", encoding="utf-8").write(head + cover(meta) + render(meta, blocks, toc_entries) + final + "</w:document>")
    if NUM_LISTS:  # each numbered list gets its own w:num on the base file's decimal abstractNum 3, restarting at 1;
        # ids are allocated above whatever the base already defines, so a rendered document can serve as base again
        np = os.path.join(work, "word", "numbering.xml"); nx = open(np, encoding="utf-8").read()
        # drop the list instances a previous render added to this base (ids >= 100 with a start override), then reallocate
        nx = re.sub(r'<w:num w:numId="(?:[1-9]\d{2,})"><w:abstractNumId w:val="3"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>', '', nx)
        existing = [int(i) for i in re.findall(r'<w:num w:numId="(\d+)"', nx)]
        base_id = max(existing + [99])
        body_xml = open(docxml, encoding="utf-8").read()
        for k, placeholder in enumerate(NUM_LISTS, start=1):
            body_xml = body_xml.replace(f'<w:numId w:val="{placeholder}"/>', f'<w:numId w:val="{base_id + k}"/>')
        open(docxml, "w", encoding="utf-8").write(body_xml)
        extra = "".join(f'<w:num w:numId="{base_id + k}"><w:abstractNumId w:val="3"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
                        for k in range(1, len(NUM_LISTS) + 1))
        open(np, "w", encoding="utf-8").write(nx.replace("</w:numbering>", extra + "</w:numbering>"))
    # header / footer placeholders: "{{External System}}" in the running header is replaced when the
    # front matter names the system (external_system: …); the confidentiality label likewise (confidentiality: …).
    for name in os.listdir(os.path.join(work, "word")):
        if name.startswith(("header", "footer")) and name.endswith(".xml"):
            fp = os.path.join(work, "word", name); x = open(fp, encoding="utf-8").read()
            if meta.get("external_system"):
                x = x.replace("{{External System}}", escape(meta["external_system"]))
            if meta.get("confidentiality"):
                x = x.replace("Internal/Client Restricted", escape(meta["confidentiality"]))
            open(fp, "w", encoding="utf-8").write(x)
    if os.path.exists(a.out):
        os.remove(a.out)
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(work):
            for f in files:
                p = os.path.join(root, f); z.write(p, os.path.relpath(p, work))
    shutil.rmtree(work)
    print(f"wrote {a.out}: {len(blocks)} blocks, {len(toc_entries)} TOC entries")

if __name__ == "__main__":
    main()
