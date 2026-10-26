#!/usr/bin/env python3
"""Draws the README figures as SVG (docs/images/*.svg). Render to PNG with:
   rsvg-convert -w 1800 docs/images/pipeline.svg -o docs/images/pipeline.png
Standard library only."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"
FONT = "DejaVu Sans, Arial, sans-serif"
C = {  # fill, stroke
    "ui": ("#EEF2F7", "#8A9BB0"), "script": ("#DCE9F8", "#3B6FB6"), "llm": ("#FBE6CC", "#D9822B"),
    "sim": ("#D9F0DF", "#3E9A5A"), "vote": ("#E4DDF4", "#6B52B3"), "out": ("#F3F3F3", "#777777"),
}


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.p = w, h, []
        self.p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">')
        self.p.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                      '<path d="M0,0 L10,5 L0,10 z" fill="#44505F"/></marker></defs>')
        self.p.append(f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>')
        self.text(w / 2, 46, title, 28, "#1F2A37", "middle", True)

    def text(self, x, y, s, size=16, fill="#1F2A37", anchor="start", bold=False):
        weight = ' font-weight="bold"' if bold else ""
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{weight}>{s}</text>')

    def box(self, x, y, w, h, kind, title, sub=""):
        f, s = C[kind]
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{f}" stroke="{s}" stroke-width="2.5"/>')
        cy = y + h / 2 + (0 if sub else 6)
        self.text(x + w / 2, cy - (6 if sub else 0), title, 19, "#1F2A37", "middle", True)
        for i, line in enumerate(sub.split("|") if sub else []):
            self.text(x + w / 2, cy + 17 + 18 * i, line, 14, "#44505F", "middle")

    def group(self, x, y, w, h, label):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none" stroke="#9AA5B1" stroke-width="2" stroke-dasharray="9 7"/>')
        self.text(x + 18, y + 28, label, 16, "#44505F", "start", True)

    def arrow(self, pts, label="", lx=0, ly=0, both=False):
        d = "M" + " L".join(f"{a},{b}" for a, b in pts)
        start = ' marker-start="url(#a)"' if both else ""
        self.p.append(f'<path d="{d}" fill="none" stroke="#44505F" stroke-width="2.5"{start} marker-end="url(#a)"/>')
        if label:
            self.text(lx, ly, label, 14, "#44505F", "middle")

    def legend(self, y, items):
        x = 60
        for kind, name in items:
            f, s = C[kind]
            self.p.append(f'<rect x="{x}" y="{y}" width="26" height="18" rx="4" fill="{f}" stroke="{s}" stroke-width="2"/>')
            self.text(x + 36, y + 15, name, 15)
            x += 40 + 9 * len(name) + 40

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.p + ["</svg>"]))


def architecture():
    g = Svg(1500, 520, "tMAGE: system overview")
    g.box(50, 150, 250, 100, "ui", "Web UI", "circuit, topology,|technology, analyses")
    g.box(380, 150, 250, 100, "script", "Pipeline", "engine/pipeline.py|runs/&lt;id&gt;/ + logs")
    g.box(730, 70, 300, 100, "llm", "LLM agents", "Ollama on Jetson Orin Nano|models of 4B or more")
    g.box(730, 230, 300, 100, "sim", "HSPICE", "SAED 90 nm, X-2025.06|testbench + .meas")
    g.box(1130, 230, 320, 100, "out", "University license server", "reachable through VPN only|(split tunnel)")
    g.box(380, 360, 250, 100, "out", "Report + logs", "report.md, full LLM prompts,|HSPICE output")
    g.arrow([(300, 200), (380, 200)], "job.json", 340, 188)
    g.arrow([(630, 185), (730, 135)], "", 0, 0, True)
    g.text(640, 140, "prompts / JSON", 14, "#44505F", "middle")
    g.arrow([(630, 215), (730, 265)], "", 0, 0, True)
    g.text(640, 262, "testbench / results", 14, "#44505F", "middle")
    g.arrow([(1030, 280), (1130, 280)], "license", 1080, 268)
    g.arrow([(505, 250), (505, 360)])
    g.arrow([(380, 410), (175, 410), (175, 250)], "shown in the UI", 275, 398)
    g.legend(490, [("ui", "User"), ("script", "Script"), ("llm", "LLM"), ("sim", "Simulator"), ("out", "Output / external")])
    g.save("architecture.svg")


def pipeline():
    g = Svg(1500, 860, "tMAGE: pipeline and verification")
    g.box(40, 90, 250, 90, "ui", "Web UI", "circuit, topology, analyses")
    g.box(340, 90, 250, 90, "ui", "context.json", "standard English summary|given to every agent")
    g.box(640, 90, 210, 90, "script", "Spec", "script: port roles")
    g.box(900, 90, 250, 90, "script", "Scenario", "script: one test|per selected analysis")
    g.box(1200, 90, 260, 90, "vote", "DUT precheck", "script AC run:|gain &gt; 0 dB?")
    for a, b in [(290, 340), (590, 640), (850, 900), (1150, 1200)]:
        g.arrow([(a, 135), (b, 135)])
    g.arrow([(1330, 180), (1330, 235)], "yes", 1352, 212)
    g.text(1470, 135, "", 1)
    g.group(40, 235, 1420, 300, "N candidates, each written by a different voter model")
    g.box(80, 290, 300, 100, "llm", "Stimulus", "LLM refines a script draft|+ matching RAG examples")
    g.box(470, 290, 300, 100, "llm", "Measure", "LLM refines the .meas draft|+ expected ranges")
    g.box(860, 290, 270, 100, "sim", "HSPICE", "testbench to|.ms0 / .mt0 results")
    g.box(1190, 290, 240, 100, "script", "Draft fallback", "script draft is used|and flagged")
    g.arrow([(380, 340), (470, 340)])
    g.arrow([(770, 340), (860, 340)])
    g.arrow([(1130, 340), (1190, 340)], "fails", 1160, 328)
    g.arrow([(1310, 390), (1310, 430), (995, 430), (995, 390)], "re-run", 1150, 450)
    g.text(80, 495, "Missing or failing tests never stop the vote: the run goes on with the script draft and the report shows the model's own contribution.", 14, "#44505F")
    g.arrow([(260, 535), (260, 600)])
    g.box(120, 600, 280, 100, "vote", "Sanity rules", "per candidate: value ranges,|no failed .meas")
    g.box(500, 600, 300, 100, "vote", "Majority vote", "cluster by metric tolerance (5 %)|largest cluster wins")
    g.box(900, 600, 250, 100, "script", "Report", "numbers only from|the winning candidate")
    g.box(1230, 600, 230, 100, "out", "Flags", "no majority, fallbacks,|spec violations")
    g.arrow([(400, 650), (500, 650)], "passed", 450, 638)
    g.arrow([(800, 650), (900, 650)], "winner", 850, 638)
    g.arrow([(1150, 650), (1230, 650)], "includes", 1190, 638)
    g.text(260, 735, "failed candidates are dropped from the vote", 14, "#44505F", "middle")
    g.legend(790, [("ui", "Input"), ("script", "Script"), ("llm", "LLM"), ("sim", "Simulator"), ("vote", "Verification"), ("out", "Output")])
    g.save("pipeline.svg")


if __name__ == "__main__":
    architecture()
    pipeline()
    print("wrote", OUT)
