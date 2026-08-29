#!/usr/bin/env python3
"""Ultimate Diagrams Renderer — Hybrid CLI/HTML-SVG Engine.

Tries fireworks-tech-graph CLI first. Falls back to generating a standalone
HTML file with inline SVG when the CLI is not available.

Usage:
    # CLI path (when fireworks-cli is installed):
    python render_diagram.py --type agent --input spec.json --output diagram.svg
    python render_diagram.py --type sequence --input spec.json --output diagram.svg --theme dark

    # Built-in path (fallback, always works):
    python render_diagram.py --type agent --input spec.json --output diagram.html
    python render_diagram.py --type architecture --input spec.json --output diagram.html --to-pdf
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


# ── CLI Detection ─────────────────────────────────────────────────────────

def _is_cli_available() -> bool:
    """Return True if fireworks-cli is on PATH."""
    return shutil.which("fireworks-cli") is not None or shutil.which("fireworks-cli.exe") is not None


# ── CLI Path ──────────────────────────────────────────────────────────────

def _render_via_cli(args) -> int:
    """Render via fireworks-cli. Returns exit code."""
    cmd = ["fireworks-cli", "render"]
    cmd.extend(["--type", args.type])
    cmd.extend(["--input", args.input])
    cmd.extend(["--output", args.output])
    cmd.extend(["--style", args.style])
    if args.theme:
        cmd.extend(["--theme", args.theme])
    if args.width:
        cmd.extend(["--width", str(args.width)])
    if args.animate:
        cmd.append("--animate")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CLI error: {result.stderr}", file=sys.stderr)
        return 1
    print(result.stdout)
    if args.animate:
        gif = args.output.rsplit(".", 1)[0] + ".gif"
        print(f"Motion sequence: {gif}")
    return 0


# ── Built-in HTML+SVG Path ───────────────────────────────────────────────

def _validate_spec(spec: dict) -> str | None:
    """Validate a JSON spec. Returns error message or None."""
    if "nodes" not in spec and "lifelines" not in spec \
            and "topics" not in spec and "participants" not in spec:
        return "Spec must contain 'nodes', 'lifelines', 'participants', or 'topics'"
    return None


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _make_id(s: str) -> str:
    return s.lower().replace(" ", "-").replace(".", "-").replace("/", "-")


def _render_architecture(spec: dict) -> str:
    """Generate HTML+SVG for system architecture diagrams."""
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])
    title = spec.get("title", "System Architecture")
    description = spec.get("description", "Cloud infrastructure / microservices topology")

    svg_parts = []
    svg_parts.append(_defs_block())

    view_w = 1600
    node_map = {}
    placed = set()

    COL_SIZE = 3          # nodes per row in grid
    NODE_W = 240
    NODE_H = 56
    COL_GAP = 320         # horizontal spacing
    ROW_GAP = 130         # vertical spacing
    GROUP_PAD = 50        # padding around group boundary

    def place_in_grid(idx: int, offset_y: int = 120):
        col = idx % COL_SIZE
        row = idx // COL_SIZE
        x = 100 + col * COL_GAP
        y = offset_y + row * ROW_GAP
        # Ensure no overlap with already placed nodes
        while any(abs(x - px) < COL_GAP and abs(y - py) < ROW_GAP for px, py in placed):
            row += 1
            y = offset_y + row * ROW_GAP
        placed.add((x, y))
        return {"x": x, "y": y, "w": NODE_W, "h": NODE_H}

    # Group nodes if groups exist
    if groups:
        for g in groups:
            gid = _make_id(g.get("id", ""))
            gnodes = []
            for i, n in enumerate(nodes):
                if n["id"] in g.get("nodes", []):
                    pos = place_in_grid(len(placed), 140)
                    node_map[n["id"]] = pos
                    gnodes.append(n)
            
            if gnodes:
                min_x = min(node_map[n["id"]]["x"] for n in gnodes) - GROUP_PAD
                max_x = max(node_map[n["id"]]["x"] + node_map[n["id"]]["w"] for n in gnodes) + GROUP_PAD
                min_y = min(node_map[n["id"]]["y"] for n in gnodes) - GROUP_PAD
                max_y = max(node_map[n["id"]]["y"] + node_map[n["id"]]["h"] for n in gnodes) + GROUP_PAD
                
                svg_parts.append(f'<rect x="{min_x}" y="{min_y}" width="{max_x - min_x}" height="{max_y - min_y}" '
                               f'rx="12" fill="var(--bg-group)" stroke="var(--border-group)" '
                               f'stroke-width="1.5" stroke-dasharray="8,4"/>')
                label = g.get("label", gid)
                # Group label badge
                svg_parts.append(f'<rect x="{min_x + 14}" y="{min_y + 14}" width="{len(label) * 8 + 24}" height="24" '
                               f'rx="6" fill="var(--bg-node)" stroke="var(--border-group)" stroke-width="1"/>')
                svg_parts.append(f'<text x="{min_x + 26}" y="{min_y + 31}" font-size="11" font-weight="700" '
                               f'fill="var(--text-secondary)">{_html_escape(label)}</text>')

    # Ungrouped nodes
    for i, n in enumerate(nodes):
        if n["id"] not in node_map:
            node_map[n["id"]] = place_in_grid(i, 120)

    # Draw nodes
    for n in nodes:
        pos = node_map.get(n["id"])
        if not pos:
            continue
        role = n.get("role", "service")
        label = n.get("label", n["id"])

        if role in ("database", "db", "storage"):
            svg_parts.append(f'<ellipse cx="{pos["x"] + pos["w"] // 2}" cy="{pos["y"]}" '
                           f'rx="{pos["w"] // 2}" ry="10" fill="var(--bg-node)" '
                           f'stroke="var(--cyan)" stroke-width="1.5"/>')
            svg_parts.append(f'<rect x="{pos["x"]}" y="{pos["y"]}" width="{pos["w"]}" height="{pos["h"] - 10}" '
                           f'fill="var(--bg-node)" stroke="var(--cyan)" stroke-width="1.5"/>')
            svg_parts.append(f'<ellipse cx="{pos["x"] + pos["w"] // 2}" cy="{pos["y"] + pos["h"] - 10}" '
                           f'rx="{pos["w"] // 2}" ry="10" fill="var(--bg-node)" '
                           f'stroke="var(--cyan)" stroke-width="1.5"/>')
            svg_parts.append(f'<text x="{pos["x"] + pos["w"] // 2}" y="{pos["y"] + pos["h"] // 2 + 4}" '
                           f'text-anchor="middle" font-size="13" font-weight="600">{_html_escape(label)}</text>')
        elif role in ("queue", "topic", "stream"):
            svg_parts.append(f'<rect x="{pos["x"]}" y="{pos["y"]}" width="{pos["w"]}" height="{pos["h"]}" '
                           f'rx="{pos["h"] // 2}" fill="var(--bg-node)" stroke="var(--rose)" stroke-width="1.5"/>')
            svg_parts.append(f'<text x="{pos["x"] + pos["w"] // 2}" y="{pos["y"] + pos["h"] // 2 + 4}" '
                           f'text-anchor="middle" font-size="13" font-weight="600">{_html_escape(label)}</text>')
        elif role in ("actor", "user", "person"):
            cx = pos["x"] + pos["w"] // 2
            cy = pos["y"] + pos["h"] // 2
            r = 24
            svg_parts.append(f'<circle cx="{cx}" cy="{cy - r}" r="{r}" fill="var(--bg-node)" '
                           f'stroke="var(--amber)" stroke-width="2"/>')
            svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy + r * 1.5}" '
                           f'stroke="var(--amber)" stroke-width="2"/>')
            svg_parts.append(f'<line x1="{cx - r}" y1="{cy - r // 2}" x2="{cx + r}" y2="{cy - r // 2}" '
                           f'stroke="var(--amber)" stroke-width="2"/>')
            svg_parts.append(f'<line x1="{cx}" y1="{cy + r * 1.5}" x2="{cx - r * 1.2}" y2="{cy + r * 2.5}" '
                           f'stroke="var(--amber)" stroke-width="2"/>')
            svg_parts.append(f'<line x1="{cx}" y1="{cy + r * 1.5}" x2="{cx + r * 1.2}" y2="{cy + r * 2.5}" '
                           f'stroke="var(--amber)" stroke-width="2"/>')
            svg_parts.append(f'<text x="{cx}" y="{cy + r * 2.8}" text-anchor="middle" font-size="12" font-weight="600">'
                           f'{_html_escape(label)}</text>')
        elif role in ("reasoning_engine", "llm", "ai"):
            svg_parts.append(f'<rect x="{pos["x"]}" y="{pos["y"]}" width="{pos["w"]}" height="{pos["h"]}" rx="8" '
                           f'fill="#faf5ff" stroke="var(--purple)" stroke-width="2"/>')
            svg_parts.append(f'<rect x="{pos["x"] + 4}" y="{pos["y"] + 4}" width="{pos["w"] - 8}" '
                           f'height="{pos["h"] - 8}" rx="6" fill="none" stroke="var(--purple)" stroke-width="1.5"/>')
            svg_parts.append(f'<text x="{pos["x"] + pos["w"] // 2}" y="{pos["y"] + pos["h"] // 2 + 4}" '
                           f'text-anchor="middle" font-size="13" font-weight="600">{_html_escape(label)}</text>')
        elif role in ("agent", "orchestrator"):
            cx = pos["x"] + pos["w"] // 2
            cy = pos["y"] + pos["h"] // 2
            hw = pos["w"] // 2
            hh = pos["h"] // 2
            pts = f"{cx - hw},{cy} {cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh}"
            svg_parts.append(f'<polygon points="{pts}" fill="var(--bg-node)" '
                           f'stroke="var(--blue)" stroke-width="2"/>')
            svg_parts.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="13" font-weight="600">'
                           f'{_html_escape(label)}</text>')
        else:
            svg_parts.append(f'<rect x="{pos["x"]}" y="{pos["y"]}" width="{pos["w"]}" height="{pos["h"]}" rx="6" '
                           f'fill="var(--bg-node)" stroke="var(--border-node)" stroke-width="1.5"/>')
            svg_parts.append(f'<text x="{pos["x"] + pos["w"] // 2}" y="{pos["y"] + pos["h"] // 2 + 4}" '
                           f'text-anchor="middle" font-size="13" font-weight="600">{_html_escape(label)}</text>')

    # Draw edges
    for e in edges:
        src = node_map.get(e.get("from", ""))
        dst = node_map.get(e.get("to", ""))
        if not src or not dst:
            continue
        kind = e.get("kind", "sync_request")
        
        x1 = src["x"] + src["w"] // 2
        y1 = src["y"] + src["h"]
        x2 = dst["x"] + dst["w"] // 2
        y2 = dst["y"]
        
        if kind in ("async_event", "async"):
            stroke = "var(--line-async)"
            dash = 'stroke-dasharray="6,3"'
            marker = 'marker-end="url(#arrowReturn)"'
        elif kind in ("stream", "data_stream"):
            stroke = "var(--line-stream)"
            dash = ""
            marker = 'marker-end="url(#arrowData)"'
        else:
            stroke = "var(--line-sync)"
            dash = ""
            marker = 'marker-end="url(#arrowSync)"'

        mid_y = (y1 + y2) // 2
        svg_parts.append(f'<path d="M {x1},{y1} C {x1},{mid_y} {x2},{mid_y} {x2},{y2}" '
                       f'fill="none" stroke="{stroke}" stroke-width="2" {dash} {marker}/>')

    return _wrap_html(title, description, "\n".join(svg_parts))


def _render_sequence(spec: dict) -> str:
    """Generate HTML+SVG for UML sequence diagrams."""
    lifelines = spec.get("lifelines", spec.get("participants", []))
    messages = spec.get("messages", spec.get("edges", []))
    title = spec.get("title", "Sequence Diagram")
    description = spec.get("description", "Interaction sequence")

    svg_parts = []
    svg_parts.append(_defs_block())

    view_w = 1600
    n = len(lifelines)
    if n < 2:
        n = 2
    spacing = min(300, (view_w - 200) // n)
    total_w = spacing * (n - 1)
    start_x = (view_w - total_w) // 2

    lifeline_map = {}
    for i, ll in enumerate(lifelines):
        x = start_x + i * spacing
        label = ll.get("label", ll.get("id", f"Participant {i+1}"))
        lifeline_map[ll.get("id", label)] = x

        # Header box with gradient effect (two stacked rects)
        box_w = max(100, len(label) * 8 + 24)
        svg_parts.append(f'<rect x="{x - box_w // 2}" y="80" width="{box_w}" height="38" rx="6" '
                       f'fill="var(--bg-node)" stroke="var(--border-node)" stroke-width="1.5"/>')
        # Top accent stripe
        svg_parts.append(f'<rect x="{x - box_w // 2}" y="80" width="{box_w}" height="4" rx="2" '
                       f'fill="var(--blue)" opacity="0.5"/>')
        svg_parts.append(f'<text x="{x}" y="104" text-anchor="middle" font-size="13" font-weight="600">'
                       f'{_html_escape(label)}</text>')

        # Lifeline (vertical dashed)
        svg_parts.append(f'<line x1="{x}" y1="125" x2="{x}" y2="850" '
                       f'stroke="var(--line)" stroke-width="1.5" stroke-dasharray="8,5"/>')

        # Section markers at top of lifeline
        svg_parts.append(f'<line x1="{x}" y1="80" x2="{x}" y2="125" '
                       f'stroke="var(--blue)" stroke-width="2" opacity="0.4"/>')

    # Messages with activation bars
    y = 180
    msg_gap = 55
    # Track activation spans: {lifeline_x: {start: y, active: bool}}
    activations: dict = {}

    for msg in messages:
        src_id = msg.get("from", "")
        dst_id = msg.get("to", "")
        x1 = lifeline_map.get(src_id)
        x2 = lifeline_map.get(dst_id)
        if x1 is None or x2 is None:
            continue

        label = msg.get("label", "")
        kind = msg.get("kind", "sync_request")
        is_response = kind in ("sync_response", "return")

        if is_response:
            stroke = "var(--line-async)"
            dash = 'stroke-dasharray="8,4"'
            marker = 'marker-end="url(#arrowReturn)"'
        elif kind in ("async_event", "async"):
            stroke = "var(--line-async)"
            dash = 'stroke-dasharray="6,4"'
            marker = 'marker-end="url(#arrowReturn)"'
        else:
            stroke = "var(--line-sync)"
            dash = ""
            marker = 'marker-end="url(#arrowSync)"'

        # Draw message arrow
        svg_parts.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
                       f'stroke="{stroke}" stroke-width="2" {dash} {marker}/>')

        # Label above the arrow
        if label:
            mx = (x1 + x2) // 2
            svg_parts.append(f'<text x="{mx}" y="{y - 8}" text-anchor="middle" font-size="11" '
                           f'fill="var(--text-secondary)" font-weight="500">{_html_escape(label)}</text>')

        # Activation bar on destination (for forward messages)
        if not is_response and x2 in lifeline_map.values():
            bar_w = 14
            bar_x = x2 - bar_w // 2
            if x2 not in activations:
                activations[x2] = {"start": y, "active": True}

        y += msg_gap

    # Draw activation bars
    for ax, span in activations.items():
        if span["active"]:
            bar_w = 14
            bar_x = ax - bar_w // 2
            bar_h = y - span["start"] - msg_gap
            if bar_h > 10:
                svg_parts.append(f'<rect x="{bar_x}" y="{span["start"]}" width="{bar_w}" height="{bar_h}" '
                               f'fill="var(--blue)" opacity="0.15" rx="3"/>')
                svg_parts.append(f'<rect x="{bar_x}" y="{span["start"]}" width="3" height="{bar_h}" '
                               f'fill="var(--blue)" opacity="0.4" rx="1"/>')

    # ViewBox height based on content
    view_h = max(1000, y + 150)
    svg_content = "\n".join(svg_parts)

    # Replace viewBox default with computed size
    html = _wrap_html(title, description, svg_content)
    html = html.replace('viewBox="0 0 1600 1000"', f'viewBox="0 0 1600 {view_h}"')
    return html


def _render_agent(spec: dict) -> str:
    """Generate HTML+SVG for AI/agent workflow diagrams."""
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    title = spec.get("title", "AI / Agent Workflow")
    description = spec.get("description", "RAG / ReAct / multi-agent orchestration")

    svg_parts = []
    svg_parts.append(_defs_block())

    # Auto-layout: center column for LLM, left for user, right for tools/stores
    cols = {"actor": [], "reasoning_engine": [], "tool": [], "vector_db": [], "agent": [], "storage": []}
    for n in nodes:
        role = n.get("role", "service")
        if role in cols:
            cols[role].append(n)
        else:
            cols["tool"].append(n)

    y = 200
    node_map = {}

    # User/actor column (left)
    for n in cols["actor"]:
        node_map[n["id"]] = {"x": 100, "y": y, "w": 140, "h": 50}
        cx, cy = 170, y + 25
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="var(--bg-node)" '
                       f'stroke="var(--amber)" stroke-width="2"/>')
        svg_parts.append(f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="12" font-weight="600">'
                       f'{_html_escape(n.get("label", n["id"]))}</text>')
        y += 100

    y = 200
    # LLM column (center)
    for n in cols["reasoning_engine"]:
        node_map[n["id"]] = {"x": 450, "y": y, "w": 260, "h": 70}
        svg_parts.append(f'<rect x="450" y="{y}" width="260" height="70" rx="8" '
                       f'fill="#faf5ff" stroke="var(--purple)" stroke-width="2"/>')
        svg_parts.append(f'<rect x="454" y="{y + 4}" width="252" height="62" rx="6" '
                       f'fill="none" stroke="var(--purple)" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="580" y="{y + 30}" text-anchor="middle" font-size="14" font-weight="600">'
                       f'{_html_escape(n.get("label", n["id"]))}</text>')
        svg_parts.append(f'<text x="580" y="{y + 50}" text-anchor="middle" font-size="11" '
                       f'fill="var(--text-muted)">{_html_escape(n.get("role", ""))}</text>')
        y += 120

    y = 200
    # Tool column (right)
    for n in cols["tool"] + cols["agent"]:
        is_agent = n.get("role") == "agent"
        node_map[n["id"]] = {"x": 850, "y": y, "w": 180, "h": 50}
        if is_agent:
            cx, cy = 940, y + 25
            hw, hh = 90, 25
            pts = f"{cx - hw},{cy} {cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh}"
            svg_parts.append(f'<polygon points="{pts}" fill="var(--bg-node)" '
                           f'stroke="var(--blue)" stroke-width="2"/>')
        else:
            svg_parts.append(f'<rect x="850" y="{y}" width="180" height="50" rx="6" '
                           f'fill="var(--bg-node)" stroke="var(--teal)" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="940" y="{y + 30}" text-anchor="middle" font-size="13" font-weight="600">'
                       f'{_html_escape(n.get("label", n["id"]))}</text>')
        y += 100

    # Vector store (storage column, right-bottom)
    y = max(y, 400)
    for n in cols["vector_db"] + cols["storage"]:
        node_map[n["id"]] = {"x": 850, "y": y, "w": 180, "h": 60, "c": True}
        svg_parts.append(f'<ellipse cx="940" cy="{y}" rx="90" ry="12" fill="var(--bg-node)" '
                       f'stroke="var(--cyan)" stroke-width="1.5"/>')
        svg_parts.append(f'<rect x="850" y="{y}" width="180" height="48" fill="var(--bg-node)" '
                       f'stroke="var(--cyan)" stroke-width="1.5"/>')
        svg_parts.append(f'<ellipse cx="940" cy="{y + 48}" rx="90" ry="12" fill="var(--bg-node)" '
                       f'stroke="var(--cyan)" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="940" y="{y + 36}" text-anchor="middle" font-size="13" font-weight="600">'
                       f'{_html_escape(n.get("label", n["id"]))}</text>')
        y += 100

    # Draw edges
    for e in edges:
        src = node_map.get(e.get("from", ""))
        dst = node_map.get(e.get("to", ""))
        if not src or not dst:
            continue
        kind = e.get("kind", "sync_request")

        x1 = src["x"] + src["w"] // 2
        y1 = src["y"] + src["h"]
        x2 = dst["x"] + dst["w"] // 2
        y2 = dst["y"]

        if kind in ("async_event", "async"):
            stroke = "var(--line-async)"
            dash = 'stroke-dasharray="6,3"'
            marker = 'marker-end="url(#arrowReturn)"'
        else:
            stroke = "var(--line-sync)"
            dash = ""
            marker = 'marker-end="url(#arrowSync)"'

        mid_y = (y1 + y2) // 2
        svg_parts.append(f'<path d="M {x1},{y1} C {x1},{mid_y} {x2},{mid_y} {x2},{y2}" '
                       f'fill="none" stroke="{stroke}" stroke-width="2" {dash} {marker}/>')

    return _wrap_html(title, description, "\n".join(svg_parts))


def _render_event_transit(spec: dict) -> str:
    """Generate HTML+SVG for event-driven architectures."""
    topics = spec.get("topics", [])
    producers = spec.get("producers", spec.get("sources", []))
    consumers = spec.get("consumers", spec.get("sinks", []))
    title = spec.get("title", "Event-Driven Architecture")
    description = spec.get("description", "Message queues / event streams / pub-sub")

    svg_parts = []
    svg_parts.append(_defs_block())

    # Layout topics in a horizontal rail
    n_topics = len(topics) if topics else 1
    spacing = min(300, 800 // n_topics)
    total_w = spacing * (n_topics - 1)
    start_x = (1200 - total_w) // 2
    topic_center_x = {}

    # Event bus line
    svg_parts.append(f'<line x1="20" y1="350" x2="1180" y2="350" '
                   f'stroke="var(--line)" stroke-width="1" stroke-dasharray="4,4"/>')
    svg_parts.append(f'<text x="30" y="344" font-size="10" fill="var(--text-muted)">Event Bus</text>')

    for i, t in enumerate(topics):
        cx = start_x + i * spacing
        tw = min(240, spacing - 40)
        tx = cx - tw // 2
        label = t.get("label", t.get("id", f"Topic {i+1}"))
        topic_center_x[t.get("id", label)] = cx

        # Topic pill
        svg_parts.append(f'<rect x="{tx}" y="325" width="{tw}" height="50" rx="25" '
                       f'fill="#fdf2f8" stroke="var(--rose)" stroke-width="2"/>')
        svg_parts.append(f'<text x="{cx}" y="355" text-anchor="middle" font-size="13" font-weight="600">'
                       f'{_html_escape(label)}</text>')

    # Producers (above topics)
    y_prod = 180
    for p in producers:
        pid = p.get("id", "")
        label = p.get("label", pid)
        produces = p.get("produces", [])
        cx = topic_center_x.get(produces[0], 600) if produces else 600
        pw = 140
        px = cx - pw // 2

        svg_parts.append(f'<rect x="{px}" y="{y_prod}" width="{pw}" height="44" rx="6" '
                       f'fill="var(--bg-node)" stroke="var(--blue)" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{cx}" y="{y_prod + 27}" text-anchor="middle" font-size="12" font-weight="600">'
                       f'{_html_escape(label)}</text>')

        # Arrow to topic
        svg_parts.append(f'<line x1="{cx}" y1="{y_prod + 44}" x2="{cx}" y2="325" '
                       f'stroke="var(--line-sync)" stroke-width="2" marker-end="url(#arrowSync)"/>')

    # Consumers (below topics)
    y_cons = 420
    consumer_groups = {}
    for c in consumers:
        cid = c.get("id", "")
        label = c.get("label", cid)
        consumes = c.get("consumes", [])
        group = c.get("group", "")
        if group and group not in consumer_groups:
            consumer_groups[group] = []
        cx = topic_center_x.get(consumes[0], 600) if consumes else 600
        cw = 140
        px = cx - cw // 2

        svg_parts.append(f'<rect x="{px}" y="{y_cons}" width="{cw}" height="44" rx="6" '
                       f'fill="var(--bg-node)" stroke="var(--teal)" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{cx}" y="{y_cons + 27}" text-anchor="middle" font-size="12" font-weight="600">'
                       f'{_html_escape(label)}</text>')
        svg_parts.append(f'<text x="{cx}" y="{y_cons + 40}" text-anchor="middle" font-size="9" '
                       f'fill="var(--text-muted)">Group: {group}</text>' if group else '')

        # Arrow from topic
        svg_parts.append(f'<line x1="{cx}" y1="375" x2="{cx}" y2="{y_cons}" '
                       f'stroke="var(--line-sync)" stroke-width="1.5" marker-end="url(#arrowSync)"/>')

        if group:
            if group not in consumer_groups:
                consumer_groups[group] = []
            consumer_groups[group].append({"x": cx - cw // 2, "y": y_cons})

    # Consumer group boundaries
    for gname, members in consumer_groups.items():
        if len(members) > 1:
            min_x = min(m["x"] for m in members) - 20
            max_x = max(m["x"] for m in members) + 160
            svg_parts.append(f'<rect x="{min_x}" y="{y_cons - 20}" width="{max_x - min_x}" '
                           f'height="{len(members) * 44 + 40}" rx="8" fill="var(--bg-group)" '
                           f'stroke="var(--border-group)" stroke-width="1" stroke-dasharray="4,4"/>')
            svg_parts.append(f'<text x="{min_x + 10}" y="{y_cons - 6}" font-size="10" font-weight="600" '
                           f'fill="var(--text-secondary)">Group: {_html_escape(gname)}</text>')

    return _wrap_html(title, description, "\n".join(svg_parts))


def _render_dataflow(spec: dict) -> str:
    """Generate HTML+SVG for data flow / ETL pipelines."""
    sources = spec.get("sources", spec.get("nodes", []))
    transforms = spec.get("transforms", spec.get("processors", []))
    sinks = spec.get("sinks", spec.get("destinations", []))
    flows = spec.get("flows", spec.get("edges", []))
    title = spec.get("title", "Data Flow / ETL Pipeline")
    description = spec.get("description", "Data movement and transformation pipeline")

    svg_parts = []
    svg_parts.append(_defs_block())

    # Build a single node list with type annotation
    all_nodes = []
    node_map = {}
    for s in sources:
        all_nodes.append({**s, "_type": "source"})
    for t in transforms:
        all_nodes.append({**t, "_type": "transform"})
    for s in sinks:
        all_nodes.append({**s, "_type": "sink"})

    # Left-to-right layout
    n = len(all_nodes)
    if n == 0:
        n = 3
    spacing = min(180, 900 // n)
    total_w = spacing * (n - 1)
    start_x = (1200 - total_w) // 2

    for i, node in enumerate(all_nodes):
        x = start_x + i * spacing
        y = 350
        w = 160
        h = 60
        label = node.get("label", node.get("id", f"Node {i+1}"))
        ntype = node.get("_type", "transform")

        node_map[node.get("id", label)] = {"x": x, "y": y, "w": w, "h": h}

        if ntype == "source":
            fill = "#f0fdf4"
            stroke = "var(--green)"
        elif ntype == "sink":
            fill = "#fef3c7"
            stroke = "var(--amber)"
        else:
            fill = "var(--bg-node)"
            stroke = "var(--blue)"

        svg_parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        svg_parts.append(f'<text x="{x + w // 2}" y="{y + 26}" text-anchor="middle" font-size="13" font-weight="600">'
                       f'{_html_escape(label)}</text>')
        sub = node.get("format", node.get("description", ""))
        if sub:
            svg_parts.append(f'<text x="{x + w // 2}" y="{y + 44}" text-anchor="middle" font-size="10" '
                           f'fill="var(--text-muted)">{_html_escape(sub)}</text>')

        # Arrow from previous node
        if i > 0:
            prev = all_nodes[i - 1]
            prev_pos = node_map[prev.get("id", "")]
            px1 = prev_pos["x"] + prev_pos["w"]
            py1 = prev_pos["y"] + prev_pos["h"] // 2
            px2 = x
            py2 = y + h // 2
            svg_parts.append(f'<line x1="{px1}" y1="{py1}" x2="{px2}" y2="{py2}" '
                           f'stroke="var(--line-sync)" stroke-width="2" marker-end="url(#arrowSync)"/>')

    return _wrap_html(title, description, "\n".join(svg_parts))


# ── Dispatch ──────────────────────────────────────────────────────────────

_RENDERERS = {
    "architecture": _render_architecture,
    "dataflow": _render_dataflow,
    "agent": _render_agent,
    "sequence": _render_sequence,
    "event-transit": _render_event_transit,
    "c4-review": _render_architecture,
    "cloud-fabric": _render_architecture,
    "memory-tiering": _render_architecture,
    "comparison": _render_architecture,
    "mindmap": _render_agent,
    "flowchart": _render_architecture,
    "ops-pulse": _render_architecture,
    "network": _render_architecture,
    "uml-class": _render_architecture,
    "uml-state": _render_architecture,
    "uml-activity": _render_dataflow,
}


def _defs_block() -> str:
    return '''<defs>
  <marker id="arrowSync" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-sync)"/>
  </marker>
  <marker id="arrowReturn" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-async)"/>
  </marker>
  <marker id="arrowData" viewBox="0 0 10 10" refX="10" refY="5"
          markerWidth="8" markerHeight="8" orient="auto">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--line-stream)"/>
  </marker>
</defs>'''


def _render_flowchart(spec: dict) -> str:
    """Flowchart layout (top-down decision tree style)."""
    return _render_architecture(spec)


def _wrap_html(title: str, description: str, svg_content: str) -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html_escape(title)}</title>
<style>
  @page {{ size: A4 landscape; margin: 0.4in; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  /* ═══ Catppuccin Latte (Light — Default) ═══ */
  :root {{
    --bg-page:       #eff1f5;
    --bg-node:       #e6e9ef;
    --bg-group:      #dce0e8;
    --border-node:   #bcc0cc;
    --border-group:  #9ca0b0;
    --line-sync:     #1e66f5;
    --line-async:    #9ca0b0;
    --line-stream:   #8839ef;
    --line:          #acb0be;
    --text-primary:  #4c4f69;
    --text-secondary:#6c6f85;
    --text-muted:    #9ca0b0;
    --blue:          #1e66f5;
    --green:         #40a02b;
    --red:           #d20f39;
    --amber:         #df8e1d;
    --purple:        #8839ef;
    --teal:          #179299;
    --rose:          #e64553;
    --cyan:          #04a5e5;
    --peach:         #fe640b;
    --lavender:      #7287fd;
  }}

  body {{ font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
          background: var(--bg-page); color: var(--text-primary); }}
  .page {{ padding: 0.4in; min-height: 100vh; }}
  .title {{ font-size: 26px; font-weight: 800; margin-bottom: 2px;
            letter-spacing: -0.02em; }}
  .subtitle {{ font-size: 14px; color: var(--text-secondary); margin-bottom: 24px; }}
  svg.diagram {{ width: 100%; height: auto; display: block; background: var(--bg-page); border-radius: 8px; }}
  .legend {{ margin-top: 20px; padding: 14px 18px; background: var(--bg-node); border-radius: 10px;
             font-size: 11px; display: flex; gap: 20px; flex-wrap: wrap; color: var(--text-secondary); }}
  .legend-item {{ display: flex; align-items: center; gap: 8px; }}

  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg-page:       #1e1e2e;
      --bg-node:       #313244;
      --bg-group:      #45475a;
      --border-node:   #585b70;
      --border-group:  #6c7086;
      --line-sync:     #89b4fa;
      --line-async:    #6c7086;
      --line-stream:   #cba6f7;
      --line:          #6c7086;
      --text-primary:  #cdd6f4;
      --text-secondary:#a6adc8;
      --text-muted:    #6c7086;
      --blue:          #89b4fa;
      --green:         #a6e3a1;
      --red:           #f38ba8;
      --amber:         #f9e2af;
      --purple:        #cba6f7;
      --teal:          #94e2d5;
      --rose:          #f5c2e7;
      --cyan:          #89dceb;
      --peach:         #fab387;
      --lavender:      #b4befe;
    }}
    body {{ background: var(--bg-page); color: var(--text-primary); }}
    svg.diagram {{ background: var(--bg-page); }}
  }}
</style>
</head>
<body>
<div class="page">
  <div class="title">{_html_escape(title)}</div>
  <div class="subtitle">{_html_escape(description)}</div>
  <svg class="diagram" viewBox="0 0 1600 1000" xmlns="http://www.w3.org/2000/svg">
    {svg_content}
  </svg>
  <div class="legend">
    <div class="legend-item">
      <svg width="28" height="4"><line x1="0" y1="2" x2="28" y2="2" stroke="var(--line-sync)" stroke-width="2"/></svg>
      <span>Sync Request</span>
    </div>
    <div class="legend-item">
      <svg width="28" height="4"><line x1="0" y1="2" x2="28" y2="2" stroke="var(--line-async)" stroke-width="1.5" stroke-dasharray="6,3"/></svg>
      <span>Async Event</span>
    </div>
    <div class="legend-item">
      <svg width="28" height="4"><line x1="0" y1="2" x2="28" y2="2" stroke="var(--line-stream)" stroke-width="3"/></svg>
      <span>Data Stream</span>
    </div>
    <div class="legend-item">
      <svg width="16" height="14"><rect x="0" y="1" width="16" height="12" rx="3" fill="none" stroke="var(--border-node)"/></svg>
      <span>Service</span>
    </div>
    <div class="legend-item">
      <svg width="16" height="14"><rect x="0" y="1" width="16" height="12" rx="6" fill="none" stroke="var(--rose)"/></svg>
      <span>Queue/Topic</span>
    </div>
    <div class="legend-item">
      <svg width="16" height="14"><rect x="0" y="1" width="16" height="12" rx="4" fill="none" stroke="var(--purple)" stroke-width="2"/><rect x="2" y="3" width="12" height="8" rx="2" fill="none" stroke="var(--purple)" stroke-width="1"/></svg>
      <span>LLM/AI</span>
    </div>
    <div class="legend-item">
      <svg width="16" height="14"><polygon points="8,1 15,7 8,13 1,7" fill="none" stroke="var(--cyan)"/></svg>
      <span>Storage/DB</span>
    </div>
  </div>
</div>
</body>
</html>'''


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ultimate Diagrams — Hybrid Renderer (CLI → HTML+SVG fallback)"
    )
    parser.add_argument("--type", required=True,
                        choices=list(_RENDERERS.keys()) + ["uml-class", "uml-state", "uml-activity",
                                                           "agent", "sequence", "architecture",
                                                           "event-transit", "dataflow", "c4-review",
                                                           "cloud-fabric", "memory-tiering",
                                                           "comparison", "mindmap", "flowchart",
                                                           "ops-pulse", "network"],
                        help="Diagram type")
    parser.add_argument("--input", required=True, help="Input JSON spec file")
    parser.add_argument("--output", required=True, help="Output file (.svg, .html, .png)")
    parser.add_argument("--style", default="technical",
                        choices=["technical", "modern", "sketch", "minimal"],
                        help="Visual style (CLI only)")
    parser.add_argument("--theme", default="light", choices=["light", "dark", "hc"],
                        help="Color theme (CLI only)")
    parser.add_argument("--width", type=int, default=None, help="Output width in px")
    parser.add_argument("--animate", action="store_true", help="Generate animated GIF (CLI only)")
    parser.add_argument("--to-pdf", action="store_true",
                        help="Convert HTML output to PDF (built-in only)")
    parser.add_argument("--force-html", action="store_true",
                        help="Force built-in HTML+SVG path even if CLI is available")

    args = parser.parse_args()

    # Validate input
    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r") as f:
        try:
            spec = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Determine output path
    is_svg_output = args.output.lower().endswith(".svg")
    is_html_output = args.output.lower().endswith(".html") or args.output.lower().endswith(".htm")
    is_png_output = args.output.lower().endswith(".png")

    # Try CLI path first (unless --force-html)
    if not args.force_html and _is_cli_available() and not is_html_output:
        print("fireworks-tech-graph CLI detected. Using CLI path...")
        if _render_via_cli(args) == 0:
            return
        print("CLI render failed, falling back to built-in...", file=sys.stderr)

    # Built-in path
    print("Using built-in HTML+SVG renderer...")
    err = _validate_spec(spec)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    dtype = args.type
    renderer = _RENDERERS.get(dtype, _render_architecture)
    html = renderer(spec)

    # Track the HTML path for optional PDF conversion
    html_path = None

    if is_html_output:
        html_path = args.output
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Diagram saved: {os.path.abspath(html_path)} ({os.path.getsize(html_path)} bytes)")
    elif is_svg_output:
        # Extract SVG content from HTML
        svg_start = html.find("<svg")
        svg_end = html.find("</svg>") + 6
        svg_content = html[svg_start:svg_end]
        svg_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{svg_content}'
        out_path = args.output
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        html_path = args.output.rsplit(".", 1)[0] + ".html"
        print(f"✓ SVG saved: {os.path.abspath(out_path)} ({os.path.getsize(out_path)} bytes)")
    elif is_png_output:
        html_path = args.output.rsplit(".", 1)[0] + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ HTML intermediate: {os.path.abspath(html_path)}")
        print(f"  Convert to PNG: open in browser and screenshot, or use Playwright")
    else:
        # Default: save as HTML
        html_path = args.output + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Diagram saved: {os.path.abspath(html_path)} ({os.path.getsize(html_path)} bytes)")

    # Optional: convert to PDF
    if args.to_pdf and html_path:
        pdf_path = args.output.rsplit(".", 1)[0] + ".pdf"
        pdf_script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "..", "..", "..", "scripts", "generate_pdf.py")
        pdf_script = os.path.normpath(pdf_script)
        if os.path.exists(pdf_script):
            print(f"Converting to PDF: {pdf_path}")
            subprocess.run([sys.executable, pdf_script, html_path, pdf_path, "--landscape"])
        else:
            print(f"PDF script not found at {pdf_script}")
            print(f"Manual: python path/to/generate_pdf.py {html_path} {pdf_path} --landscape")


if __name__ == "__main__":
    main()
