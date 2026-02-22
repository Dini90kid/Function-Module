import re
from pathlib import Path

EDGE_RE = re.compile(r"^(?P<p>[^-]+)->\s*(?P<c>[^\[]+)\[(?P<k>[^\]]+)\]", re.IGNORECASE)
SKIP_RE = re.compile(r"^SKIPPED:\s*(?P<p>[^-]+)->\s*(?P<c>[^\[]+)\[", re.IGNORECASE)

def load_edges(lineage_path):
    rows = []
    for raw in Path(lineage_path).read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            continue
        m_skip = SKIP_RE.search(line)
        if m_skip:
            rows.append((m_skip.group("p").strip(), m_skip.group("c").strip(), "FM", True))
            continue
        m = EDGE_RE.search(line.replace("  "," ").replace(" -","-"))
        if m:
            rows.append((m.group("p").strip(), m.group("c").strip(), m.group("k").strip().upper(), False))
    return rows

def topo_layers(edges):
    from collections import defaultdict, deque
    out = defaultdict(set); indeg = defaultdict(int); nodes = set()
    for p,c,_,_ in edges:
        nodes.add(p); nodes.add(c)
        if c not in out[p]:
            out[p].add(c); indeg[c]+=1; indeg.setdefault(p, indeg.get(p,0))
    q = deque([n for n in nodes if indeg.get(n,0)==0])
    layers, seen = [], set()
    while q:
        layer = []
        for _ in range(len(q)):
            n = q.popleft(); layer.append(n); seen.add(n)
            for m in list(out.get(n, [])):
                indeg[m]-=1
                if indeg[m]==0:
                    q.append(m)
        layers.append(layer)
    remaining = [n for n in nodes if n not in seen]
    if remaining: layers.append(remaining)
    return layers
