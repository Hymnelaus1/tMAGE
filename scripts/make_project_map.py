#!/usr/bin/env python3
"""Draws the project node map from ONE description (GROUPS + EDGES below).

Outputs
  docs/26_Project_Map.canvas       Obsidian Canvas (open docs/ as a vault; nodes can be moved and edited)
  docs/images/project_map.svg/png  the same map as an image (png: rsvg-convert -w 2600)
Edit GROUPS/EDGES when a script, module or connection is added, then re-run. Standard library only.
"""
import json
import subprocess
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
W, H, GAP, PAD, HEAD = 340, 160, 30, 30, 56
COLORS = {"1": ("#FBE0E0", "#C0504D"), "2": ("#FBE6CC", "#D9822B"), "3": ("#FFF6C9", "#B8A000"), "4": ("#D9F0DF", "#3E9A5A"),
          "5": ("#D6EEF5", "#2E8FA8"), "6": ("#E4DDF4", "#6B52B3")}

# group: (label, x, y, columns, color, [(id, title, role, [capabilities])])
GROUPS = [
    ("User interface", 0, 0, 2, "4", [
        ("html", "app/static/index.html", "Web UI in the browser", ["pick netlist, topology, technology, corner", "choose analyses, models, voting N", "live status, report view"]),
        ("server", "app/server.py", "HTTP server, stdlib only", ["parses netlist, guesses topology/technology", "adapts the netlist to SAED 90 nm", "writes job.json, starts the pipeline", "status API, reaper for zombie runs"]),
        ("runsh", "run.sh", "Starts the UI on 127.0.0.1:8765", ["loads config/env.sh and jetson.env"]),
        ("catalog", "config/catalog.json", "Topologies, technologies, analyses", ["metrics and parameters per analysis", "UI labels (still partly Turkish)"]),
    ]),
    ("External systems", 0, 520, 2, "6", [
        ("ollama", "Jetson Orin Nano / Ollama", "LLM server, port 11434", ["models of 4B or more only", "temp 0.2, num_ctx 8192"]),
        ("hspice", "HSPICE X-2025.06 + SAED 90 nm", "Circuit simulator", ["runs each testbench", "writes .lis .ms0 .mt0 .ma0"]),
        ("lic", "University license server", "Reached through the split-tunnel VPN", ["scripts/vpn.sh (local only)", "pipeline pre-checks the port"]),
        ("github", "GitHub Hymnelaus1/tMAGE", "Private repository", ["tags v0.1.0 to v0.3.1", "no Synopsys material, no secrets"]),
    ]),
    ("Engine (engine/)", 850, 0, 3, "1", [
        ("pipeline", "engine/pipeline.py", "Pipeline class: the whole flow", ["spec, scenario, DUT precheck", "N candidates: stimulus, measure, HSPICE", "script-draft fallback, sanity rules", "5 % cluster vote, spec checks, report"]),
        ("handoff", "engine/handoff.py", "Data hand-off between agents", ["builds context.json", "stage files and JSON schemas", "builds the messages and system prompt"]),
        ("rag", "engine/rag.py", "Knowledge base and script drafts", ["retrieves matching kit examples", "drafts: testbench and .meas per analysis"]),
        ("llm", "engine/llm.py", "Ollama chat call", ["JSON mode or schema", "JSON parse and repair"]),
        ("sim", "engine/sim.py", "HSPICE runner and output reader", ["parse_measure_file: failed is not a value", "lis_problems: errors and warnings"]),
        ("log", "engine/log.py", "Per-run logger", ["run.log, trace.jsonl, status.json", "full prompts and HSPICE output"]),
        ("batch", "engine/batch.py", "Batch runner through the UI API", ["REPS runs per circuit, --voters --agent", "summary.json and SUMMARY.md"]),
        ("bench", "engine/bench.py", "Older per-agent model test", ["scores each model per stage"]),
    ]),
    ("Prompts and knowledge", 2090, 0, 2, "3", [
        ("prompts", "config/agent_prompts.json", "Common prompt, rules and pitfalls per stage", ["spec, scenario, stimulus, measure, report", "pitfalls = observed errors and fixes"]),
        ("stages", "config/stages.json", "Stage goals and output schemas", ["JSON schema per stage"]),
        ("pv", "config/prompt_versions/", "Old prompt sets for rollback", ["v1_old, v2_manual, v3_pitfalls"]),
        ("kin", "knowledge/inputs/", "Kit netlists, parameter files", ["SkyWater models (Apache-2.0)", "vendor models are git-ignored"]),
        ("kex", "knowledge/examples + ref_da.json", "RAG examples and the hand reference", ["DA 42.58 dB, FCO 29.7 dB, TSO 43.2 dB"]),
        ("envf", "config/env.sh, jetson.env", "Local settings (not in git)", ["tool paths, license server, Ollama address"]),
    ]),
    ("Experiment and analysis scripts (scripts/)", 850, 760, 3, "5", [
        ("mbench", "model_bench.sh", "Each model alone on DA, FCO, TSO", ["3 runs x 3 candidates"]),
        ("mixed", "mixed_vote.sh", "Mixed-model voting", ["one model per candidate"]),
        ("rank", "rank_models.py", "Top 3 models per circuit", ["clean majority, accuracy, speed"]),
        ("recomp", "recompute_scores.py", "Offline re-scoring", ["re-parses .ms0/.mt0, re-clusters", "writes docs/23"]),
        ("scan", "scan_findings.py, scan_loop.sh", "Read-only findings scan", ["writes docs/22"]),
        ("collect", "collect_logs.py", "All run logs in one place", ["writes docs/24 and the raw log archive"]),
        ("figs", "make_figures.py, make_project_map.py", "README figures and this map", ["SVG, PNG, Obsidian Canvas"]),
        ("backup", "backup.sh, install_backup.sh", "Automatic backup", ["post-commit hook + 2-hourly timer", "local snapshot, then push"]),
        ("vpn", "vpn.sh", "University VPN service (local only)", ["always-on split tunnel"]),
    ]),
    ("Data and documents", 2090, 760, 2, "2", [
        ("runs", "runs/<id>/", "One folder per run", ["context.json, stages/, work/cand*", "run.log, trace.jsonl, report.md"]),
        ("batchd", "batch/<name>/", "Benchmark and mixed-vote results", ["model x circuit x rep, summary.json"]),
        ("docs", "docs/ (Obsidian vault)", "Notes, reports, change log", ["17 hand-off, 18 change log, 20 errors", "22 to 25 generated reports, session notes"]),
        ("snap", "/data/tmage_backups/", "Local snapshots and git bundles", ["keeps 48"]),
        ("test", "~/tmage_teste/", "Test and backup copy of everything", ["no remote, no hook"]),
        ("road", "README.md, ROADMAP.md", "Project status and plan", ["checklist, versions, known issues"]),
    ]),
]

EDGES = [
    ("html", "server", "job.json, /api"), ("catalog", "server", "labels"), ("runsh", "server", "starts"), ("server", "pipeline", "spawns run"),
    ("server", "runs", "creates, reads status"), ("server", "sim", "adapt PDK path"),
    ("pipeline", "handoff", "context, stages"), ("pipeline", "rag", "drafts, examples"), ("pipeline", "llm", "chat per stage"),
    ("pipeline", "sim", "run testbenches"), ("pipeline", "log", "events"), ("llm", "ollama", "prompts, JSON"), ("sim", "hspice", "hspice -i"),
    ("hspice", "lic", "checkout"), ("pipeline", "lic", "port pre-check"),
    ("handoff", "prompts", "reads rules"), ("handoff", "stages", "schemas"), ("prompts", "pv", "versions"), ("rag", "kin", "kit netlists"), ("rag", "kex", "examples"),
    ("pipeline", "runs", "writes"), ("log", "runs", "run.log"), ("bench", "llm", "model test"),
    ("batch", "server", "POST jobs"), ("batch", "batchd", "summary"), ("mbench", "batch", "per model"), ("mixed", "batch", "voters"),
    ("batchd", "rank", ""), ("batchd", "recomp", ""), ("batchd", "scan", ""), ("runs", "collect", ""),
    ("recomp", "docs", "docs/23"), ("scan", "docs", "docs/22"), ("collect", "docs", "docs/24"), ("figs", "docs", "images, canvas"),
    ("backup", "snap", "snapshot"), ("backup", "github", "push"), ("vpn", "lic", "tunnel"), ("backup", "test", "manual copy"),
    ("docs", "road", ""),
]


def layout():
    pos, boxes = {}, []
    for label, gx, gy, cols, color, nodes in GROUPS:
        rows = -(-len(nodes) // cols)
        gw, gh = 2 * PAD + cols * W + (cols - 1) * GAP, HEAD + PAD + rows * H + (rows - 1) * GAP
        boxes.append((label, gx, gy, gw, gh, color))
        for i, (nid, title, role, caps) in enumerate(nodes):
            r, c = divmod(i, cols)
            pos[nid] = (gx + PAD + c * (W + GAP), gy + HEAD + r * (H + GAP), color, title, role, caps)
    return pos, boxes


def sides(a, b):
    ax, ay = a[0] + W / 2, a[1] + H / 2
    bx, by = b[0] + W / 2, b[1] + H / 2
    if abs(bx - ax) >= abs(by - ay):
        return ("right", "left") if bx > ax else ("left", "right")
    return ("bottom", "top") if by > ay else ("top", "bottom")


def anchor(p, side):
    return {"right": (p[0] + W, p[1] + H / 2), "left": (p[0], p[1] + H / 2), "top": (p[0] + W / 2, p[1]), "bottom": (p[0] + W / 2, p[1] + H)}[side]


def canvas(pos, boxes):
    items = []
    for label, gx, gy, gw, gh, color in boxes:
        items.append({"id": "g_" + label[:6], "type": "group", "label": label, "x": gx, "y": gy, "width": gw, "height": gh, "color": color})
    for nid, p in pos.items():
        text = f"### {p[3]}\n**{p[4]}**\n\n" + "\n".join(f"- {c}" for c in p[5])
        items.append({"id": nid, "type": "text", "text": text, "x": p[0], "y": p[1], "width": W, "height": H, "color": p[2]})
    edges = []
    for i, (a, b, lab) in enumerate(EDGES):
        sa, sb = sides(pos[a], pos[b])
        e = {"id": f"e{i}", "fromNode": a, "fromSide": sa, "toNode": b, "toSide": sb, "toEnd": "arrow"}
        if lab:
            e["label"] = lab
        edges.append(e)
    (ROOT / "docs" / "26_Project_Map.canvas").write_text(json.dumps({"nodes": items, "edges": edges}, indent=1, ensure_ascii=False))


def svg(pos, boxes):
    xs = [b[1] + b[3] for b in boxes]
    ys = [b[2] + b[4] for b in boxes]
    w, h = max(xs) + 40, max(ys) + 90
    P = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -70 {w + 20} {h + 70}" width="{w + 20}" height="{h + 70}" font-family="DejaVu Sans, Arial, sans-serif">',
         '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#44505F"/></marker></defs>',
         f'<rect x="-20" y="-70" width="{w + 20}" height="{h + 70}" fill="#FFFFFF"/>',
         '<text x="0" y="-25" font-size="34" font-weight="bold" fill="#1F2A37">tMAGE: project node map (scripts, pipeline, LLM and tool connections)</text>']
    for label, gx, gy, gw, gh, color in boxes:
        f, s = COLORS[color]
        P.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="18" fill="{f}" fill-opacity="0.35" stroke="{s}" stroke-width="2.5" stroke-dasharray="10 7"/>')
        P.append(f'<text x="{gx + 22}" y="{gy + 36}" font-size="24" font-weight="bold" fill="#1F2A37">{label}</text>')
    lab = []
    for a, b, text in EDGES:
        sa, sb = sides(pos[a], pos[b])
        (x1, y1), (x2, y2) = anchor(pos[a], sa), anchor(pos[b], sb)
        horiz = sa in ("left", "right")
        k = 0.35
        c1 = (x1 + (x2 - x1) * k, y1) if horiz else (x1, y1 + (y2 - y1) * k)
        c2 = (x2 - (x2 - x1) * k, y2) if horiz else (x2, y2 - (y2 - y1) * k)
        P.append(f'<path d="M{x1},{y1} C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {x2},{y2}" stroke="#44505F" stroke-width="2" stroke-opacity="0.6" fill="none" marker-end="url(#a)"/>')
        if text:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            tw = 7.6 * len(text) + 10
            lab.append(f'<rect x="{mx - tw / 2}" y="{my - 17}" width="{tw}" height="22" rx="5" fill="#FFFFFF" fill-opacity="0.92" stroke="#C5CCD6"/>')
            lab.append(f'<text x="{mx}" y="{my - 1}" font-size="14" fill="#1F2A37" text-anchor="middle">{text}</text>')
    for nid, p in pos.items():
        f, s = COLORS[p[2]]
        x, y = p[0], p[1]
        P.append(f'<rect x="{x}" y="{y}" width="{W}" height="{H}" rx="12" fill="{f}" stroke="{s}" stroke-width="2.5"/>')
        P.append(f'<text x="{x + W / 2}" y="{y + 30}" font-size="{min(19, round((W - 24) / (0.62 * len(p[3])), 1))}" font-weight="bold" fill="#1F2A37" text-anchor="middle">{p[3].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</text>')
        P.append(f'<text x="{x + W / 2}" y="{y + 54}" font-size="14.5" fill="#44505F" text-anchor="middle" font-style="italic">{p[4]}</text>')
        for k, c in enumerate(p[5][:4]):
            P.append(f'<text x="{x + 16}" y="{y + 82 + 20 * k}" font-size="13.5" fill="#1F2A37">• {textwrap.shorten(c, 46, placeholder="…")}</text>')
    P += lab + ["</svg>"]
    out = ROOT / "docs" / "images" / "project_map.svg"
    out.write_text("\n".join(P))
    try:
        subprocess.run(["rsvg-convert", "-w", "2600", str(out), "-o", str(out.with_suffix(".png"))], check=True)
    except (OSError, subprocess.CalledProcessError):
        print("rsvg-convert not available: PNG not rendered")


if __name__ == "__main__":
    pos, boxes = layout()
    canvas(pos, boxes)
    svg(pos, boxes)
    print("wrote docs/26_Project_Map.canvas and docs/images/project_map.svg/png:", len(pos), "nodes,", len(EDGES), "edges")
