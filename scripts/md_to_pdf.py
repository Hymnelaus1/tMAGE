#!/usr/bin/env python3
"""Minimal Markdown -> PDF (headings, paragraphs, bullets, tables, code blocks, bold/inline code). Needs Python >= 3.10 and reportlab (pip install --target DIR reportlab; MD2PDF_LIB=DIR).
Usage: MD2PDF_LIB=DIR python3 scripts/md_to_pdf.py out.pdf "Title" a.md b.md ..."""
import os
import re
import sys
from xml.sax.saxutils import escape

if os.environ.get("MD2PDF_LIB"):          # directory with reportlab (pip install --target)
    sys.path.insert(0, os.environ["MD2PDF_LIB"])

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", "/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DV", boldItalic="DVB")
BODY = ParagraphStyle("b", fontName="DV", fontSize=8.5, leading=11.5, spaceAfter=4)
CELL = ParagraphStyle("c", parent=BODY, fontSize=7, leading=8.8, spaceAfter=0)
H = {1: ParagraphStyle("h1", fontName="DVB", fontSize=15, leading=19, spaceBefore=6, spaceAfter=8, textColor=colors.HexColor("#0d3b36")),
     2: ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#1c7c74")),
     3: ParagraphStyle("h3", fontName="DVB", fontSize=9.5, leading=12, spaceBefore=6, spaceAfter=3)}
CODE = ParagraphStyle("k", fontName="DVM", fontSize=6.8, leading=8.4, backColor=colors.HexColor("#eef5f3"), borderPadding=4, spaceAfter=6)


def inline(t):
    t = escape(t)
    t = re.sub(r"`([^`]+)`", r'<font name="DVM" size="7">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<font color="#1c7c74">\1</font>', t)
    return t


def convert(md, story):
    lines, i = md.splitlines(), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            story.append(Preformatted("\n".join(lines[i + 1:j])[:6000], CODE))
            i = j + 1
        elif ln.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in lines[i:j] if not re.match(r"^\|[\s\-|:]+\|$", r)]
            n = max(len(r) for r in rows)
            data = [[Paragraph(inline(c), CELL) for c in r + [""] * (n - len(r))] for r in rows]
            t = Table(data, repeatRows=1, colWidths=[(A4[0] - 30 * mm) / n] * n)
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dcefe9")), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#9fc4bb")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 6)]
            i = j
        elif re.match(r"^#{1,3} ", ln):
            lv = len(ln) - len(ln.lstrip("#"))
            story.append(Paragraph(inline(ln[lv + 1:]), H[lv]))
            i += 1
        elif re.match(r"^\s*([*\-]|\d+\.) ", ln):
            story.append(Paragraph(inline(re.sub(r"^\s*([*\-]|\d+\.) ", "• ", ln, count=1) if not re.match(r"^\s*\d+\.", ln) else ln.strip()), ParagraphStyle("l", parent=BODY, leftIndent=10)))
            i += 1
        elif ln.strip():
            story.append(Paragraph(inline(ln), BODY))
            i += 1
        else:
            i += 1


def main():
    out, title, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    story = [Paragraph(escape(title), H[1]), Spacer(1, 4)]
    for k, f in enumerate(files):
        if k:
            story.append(PageBreak())
        convert(open(f, encoding="utf-8").read(), story)
    SimpleDocTemplate(out, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=14 * mm, bottomMargin=14 * mm, title=title).build(story)
    print("wrote", out)


if __name__ == "__main__":
    main()
