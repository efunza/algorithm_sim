# app.py  –  AlgoLab: Interactive Algorithm Explorer
# Run:  streamlit run app.py

import random
import time
import timeit
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  Page config (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AlgoLab",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  Global CSS  – dark lab aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root tokens ──────────────────────────── */
:root {
  --bg:        #0d0f14;
  --surface:   #14181f;
  --surface2:  #1c2230;
  --border:    #252d3d;
  --accent:    #00e5ff;
  --accent2:   #ff4f7b;
  --accent3:   #b47cff;
  --gold:      #ffd166;
  --text:      #e4eaf5;
  --muted:     #7a8aa0;
  --success:   #06d6a0;
  --radius:    12px;
  --font:      'Space Grotesk', sans-serif;
  --mono:      'JetBrains Mono', monospace;
}

/* ── Base resets ──────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main            { background: var(--bg) !important; color: var(--text); font-family: var(--font); }
[data-testid="stSidebar"]                { background: var(--surface) !important; }
[data-testid="stHeader"]                 { background: transparent !important; }

/* ── Hide Streamlit chrome ────────────────── */
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"]             { display:none !important; }

/* ── Hero banner ──────────────────────────── */
.hero {
  background: linear-gradient(135deg, #0d1220 0%, #111827 50%, #0a1628 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 280px; height: 280px;
  background: radial-gradient(circle, rgba(0,229,255,.12) 0%, transparent 70%);
  pointer-events: none;
}
.hero::after {
  content: '';
  position: absolute;
  bottom: -40px; left: 30%;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(180,124,255,.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-eyebrow {
  font-family: var(--mono);
  font-size: .72rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: .5rem;
}
.hero h1 {
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  line-height: 1.1;
  margin: 0 0 .75rem;
  background: linear-gradient(90deg, #e4eaf5 0%, var(--accent) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  color: var(--muted);
  font-size: 1rem;
  max-width: 540px;
  line-height: 1.6;
}

/* ── Stat pills on hero ───────────────────── */
.stat-row { display:flex; gap:1.5rem; flex-wrap:wrap; margin-top:1.5rem; }
.stat-pill {
  background: rgba(255,255,255,.04);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: .35rem 1rem;
  font-family: var(--mono);
  font-size: .8rem;
  color: var(--muted);
}
.stat-pill span { color: var(--accent); font-weight:600; }

/* ── Cards ────────────────────────────────── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  margin-bottom: 1rem;
}
.card-accent { border-left: 3px solid var(--accent); }
.card-gold   { border-left: 3px solid var(--gold); }
.card-pink   { border-left: 3px solid var(--accent2); }
.card-purple { border-left: 3px solid var(--accent3); }

/* ── Section label ────────────────────────── */
.section-label {
  font-family: var(--mono);
  font-size: .7rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: .4rem;
}

/* ── Complexity badges ────────────────────── */
.badge {
  display: inline-block;
  font-family: var(--mono);
  font-size: .75rem;
  padding: .2rem .65rem;
  border-radius: 6px;
  font-weight: 600;
  margin: .15rem .1rem;
}
.badge-green  { background: rgba(6,214,160,.15);  color: #06d6a0; border:1px solid rgba(6,214,160,.3); }
.badge-cyan   { background: rgba(0,229,255,.12);  color: #00e5ff; border:1px solid rgba(0,229,255,.25);}
.badge-yellow { background: rgba(255,209,102,.12);color: #ffd166; border:1px solid rgba(255,209,102,.3);}
.badge-orange { background: rgba(255,140,60,.12); color: #ff8c3c; border:1px solid rgba(255,140,60,.3); }
.badge-red    { background: rgba(255,79,123,.12); color: #ff4f7b; border:1px solid rgba(255,79,123,.3); }

/* ── Step note box ────────────────────────── */
.step-note {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  border-radius: 8px;
  padding: .75rem 1.2rem;
  font-family: var(--mono);
  font-size: .85rem;
  color: var(--text);
  margin-top: .5rem;
}

/* ── Streamlit component overrides ───────── */
div[data-testid="stTabs"] > div > div > button {
  font-family: var(--font) !important;
  font-size: .9rem !important;
  color: var(--muted) !important;
  border-radius: 8px 8px 0 0 !important;
  padding: .6rem 1.2rem !important;
}
div[data-testid="stTabs"] > div > div > button[aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
  background: var(--surface) !important;
}
div[data-testid="stTabs"] > div { background: var(--bg) !important; }

/* Slider */
[data-testid="stSlider"] > div > div > div { background: var(--accent) !important; }

/* Selectbox & radio */
[data-testid="stSelectbox"] div[role="combobox"] {
  background: var(--surface2) !important;
  border-color: var(--border) !important;
  border-radius: 8px !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
}
[data-testid="stRadio"] label { color: var(--text) !important; font-family: var(--font) !important; }

/* Buttons */
[data-testid="stButton"] > button {
  background: linear-gradient(135deg, var(--accent), #0099bb) !important;
  color: #000 !important;
  font-family: var(--font) !important;
  font-weight: 600 !important;
  border: none !important;
  border-radius: 8px !important;
  padding: .55rem 1.5rem !important;
  letter-spacing: .02em !important;
  transition: opacity .2s !important;
}
[data-testid="stButton"] > button:hover { opacity: .85 !important; }

/* Number input */
[data-testid="stNumberInput"] input {
  background: var(--surface2) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
  font-family: var(--mono) !important;
}

/* Text area */
textarea {
  background: var(--surface2) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  font-family: var(--mono) !important;
  font-size: .85rem !important;
  border-radius: 8px !important;
}

/* Metric */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size:.8rem !important; }
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: var(--mono) !important; }

/* Dataframe */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius:8px !important; overflow:hidden; }

/* Divider */
hr { border-color: var(--border) !important; }

/* ── Race result table ────────────────────── */
.race-table { width:100%; border-collapse:collapse; font-family:var(--font); font-size:.9rem; }
.race-table th {
  background: var(--surface2);
  color: var(--muted);
  font-size:.72rem;
  letter-spacing:.1em;
  text-transform:uppercase;
  padding:.7rem 1rem;
  text-align:left;
  border-bottom:1px solid var(--border);
}
.race-table td { padding:.65rem 1rem; border-bottom:1px solid var(--border); color:var(--text); }
.race-table tr:last-child td { border-bottom:none; }
.race-table tr:hover td { background: rgba(255,255,255,.02); }
.winner-row td { color: var(--gold) !important; }
.rank-1 { color:var(--gold); font-weight:700; }
.rank-2 { color:var(--muted); }
.rank-3 { color:#cd7f32; }

/* ── Quiz styles ──────────────────────────── */
.quiz-q {
  font-size:1rem;
  font-weight:500;
  color:var(--text);
  margin-bottom:.3rem;
}
[data-testid="stRadio"] > div { background:var(--surface) !important; border-radius:8px; padding:.5rem .75rem; }

/* ── Scrollbar ────────────────────────────── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Data classes & algorithm logic
# ─────────────────────────────────────────────
@dataclass
class Step:
    array: List[int]
    i: Optional[int] = None
    j: Optional[int] = None
    note: str = ""
    swaps: int = 0
    comparisons: int = 0


def bubble_sort_steps(arr: List[int]) -> List[Step]:
    a = arr[:]
    steps = [Step(a[:], note="Start")]
    n = len(a)
    swaps = comparisons = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            steps.append(Step(a[:], i=j, j=j+1, note=f"Compare a[{j}]={a[j]} and a[{j+1}]={a[j+1]}", swaps=swaps, comparisons=comparisons))
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swaps += 1
                swapped = True
                steps.append(Step(a[:], i=j, j=j+1, note=f"Swap → a[{j}]={a[j]}, a[{j+1}]={a[j+1]}", swaps=swaps, comparisons=comparisons))
        if not swapped:
            break
    steps.append(Step(a[:], note="✓ Sorted!", swaps=swaps, comparisons=comparisons))
    return steps


def selection_sort_steps(arr: List[int]) -> List[Step]:
    a = arr[:]
    steps = [Step(a[:], note="Start")]
    n = len(a)
    swaps = comparisons = 0
    for i in range(n):
        min_idx = i
        steps.append(Step(a[:], i=i, note=f"Find min in a[{i}..{n-1}]", swaps=swaps, comparisons=comparisons))
        for j in range(i+1, n):
            comparisons += 1
            steps.append(Step(a[:], i=min_idx, j=j, note=f"Compare a[{min_idx}]={a[min_idx]} with a[{j}]={a[j]}", swaps=swaps, comparisons=comparisons))
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            steps.append(Step(a[:], i=i, j=min_idx, note=f"Swap a[{i}] ↔ a[{min_idx}]", swaps=swaps, comparisons=comparisons))
    steps.append(Step(a[:], note="✓ Sorted!", swaps=swaps, comparisons=comparisons))
    return steps


def insertion_sort_steps(arr: List[int]) -> List[Step]:
    a = arr[:]
    steps = [Step(a[:], note="Start")]
    swaps = comparisons = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        steps.append(Step(a[:], i=i, note=f"Insert key={key} (a[{i}])", swaps=swaps, comparisons=comparisons))
        while j >= 0 and a[j] > key:
            comparisons += 1
            a[j+1] = a[j]
            steps.append(Step(a[:], i=j, j=j+1, note=f"Shift a[{j}]={a[j+1]} right", swaps=swaps, comparisons=comparisons))
            j -= 1
        a[j+1] = key
        steps.append(Step(a[:], i=j+1, note=f"Place key={key} at index {j+1}", swaps=swaps, comparisons=comparisons))
    steps.append(Step(a[:], note="✓ Sorted!", swaps=swaps, comparisons=comparisons))
    return steps


def merge_sort_steps(arr: List[int]) -> List[Step]:
    steps = [Step(arr[:], note="Start merge sort")]
    a = arr[:]
    comparisons_box = [0]

    def merge_sort(a, lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        merge_sort(a, lo, mid)
        merge_sort(a, mid, hi)
        left = a[lo:mid]
        right = a[mid:hi]
        k = lo
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons_box[0] += 1
            if left[i] <= right[j]:
                a[k] = left[i]; i += 1
            else:
                a[k] = right[j]; j += 1
            k += 1
            steps.append(Step(a[:], i=k-1, note=f"Merge [{lo},{hi}): placed {a[k-1]}", comparisons=comparisons_box[0]))
        while i < len(left):
            a[k] = left[i]; i += 1; k += 1
        while j < len(right):
            a[k] = right[j]; j += 1; k += 1

    merge_sort(a, 0, len(a))
    steps.append(Step(a[:], note="✓ Sorted!", comparisons=comparisons_box[0]))
    return steps


def linear_search_steps(arr: List[int], target: int) -> List[Step]:
    steps = [Step(arr[:], note=f"Linear search for {target}")]
    for i, val in enumerate(arr):
        steps.append(Step(arr[:], i=i, note=f"Check index {i}: {val} {'== target ✓' if val==target else '≠ target'}"))
        if val == target:
            steps.append(Step(arr[:], i=i, note=f"Found {target} at index {i} after {i+1} checks!"))
            return steps
    steps.append(Step(arr[:], note=f"{target} not found after {len(arr)} checks"))
    return steps


def binary_search_steps(sorted_arr: List[int], target: int) -> List[Step]:
    a = sorted_arr[:]
    steps = [Step(a[:], note=f"Binary search for {target}")]
    lo, hi = 0, len(a) - 1
    checks = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        checks += 1
        steps.append(Step(a[:], i=mid, note=f"mid={mid}, a[mid]={a[mid]}, range=[{lo},{hi}]"))
        if a[mid] == target:
            steps.append(Step(a[:], i=mid, note=f"Found {target} at index {mid} in {checks} checks!"))
            return steps
        if a[mid] < target:
            lo = mid + 1
            steps.append(Step(a[:], note=f"Go right → range=[{lo},{hi}]"))
        else:
            hi = mid - 1
            steps.append(Step(a[:], note=f"Go left  → range=[{lo},{hi}]"))
    steps.append(Step(a[:], note=f"{target} not found"))
    return steps


def bfs_steps(adj: Dict[str, List[str]], start: str) -> List[str]:
    visited = {start}
    q = [start]
    order = []
    while q:
        node = q.pop(0)
        order.append(node)
        for nei in adj.get(node, []):
            if nei not in visited:
                visited.add(nei)
                q.append(nei)
    return order


def dfs_steps(adj: Dict[str, List[str]], start: str) -> List[str]:
    visited = set()
    order = []
    def dfs(u):
        visited.add(u)
        order.append(u)
        for v in adj.get(u, []):
            if v not in visited:
                dfs(v)
    dfs(start)
    return order


def parse_adj(text_block: str) -> Dict[str, List[str]]:
    adj: Dict[str, List[str]] = {}
    for line in text_block.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        node, rest = line.split(':', 1)
        node = node.strip()
        neighbors = [x.strip() for x in rest.split(',') if x.strip()]
        adj[node] = neighbors
    for node, nbrs in list(adj.items()):
        for v in nbrs:
            adj.setdefault(v, [])
    return adj


# ─────────────────────────────────────────────
#  Plotly bar chart for array state
# ─────────────────────────────────────────────
PLOT_BG    = "#14181f"
PLOT_PAPER = "#14181f"
BAR_BASE   = "#2a3a55"
BAR_HI     = "#00e5ff"
BAR_HJ     = "#ff4f7b"
GRID_COLOR = "#1c2230"
FONT_COLOR = "#e4eaf5"

def plotly_array(arr: List[int],
                 hi: Optional[int] = None,
                 hj: Optional[int] = None,
                 title: str = "") -> go.Figure:
    colors = []
    for k in range(len(arr)):
        if k == hi:
            colors.append(BAR_HI)
        elif k == hj:
            colors.append(BAR_HJ)
        else:
            colors.append(BAR_BASE)

    fig = go.Figure(go.Bar(
        x=list(range(len(arr))),
        y=arr,
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="index %{x}<br>value %{y}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(color=FONT_COLOR, size=13, family="Space Grotesk"), x=0),
        paper_bgcolor=PLOT_PAPER,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family="Space Grotesk"),
        xaxis=dict(showgrid=False, zeroline=False, title="Index",
                   tickfont=dict(size=10), color=FONT_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False, title="Value",
                   tickfont=dict(size=10), color=FONT_COLOR),
        margin=dict(l=40, r=10, t=35, b=35),
        height=260,
    )
    return fig


# ─────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">⚗️ science fair edition</div>
  <h1>AlgoLab</h1>
  <p class="hero-sub">Step-by-step algorithm visualizations with real benchmark experiments. Watch how algorithms work — then measure how fast they actually are.</p>
  <div class="stat-row">
    <div class="stat-pill"><span>6</span> algorithms</div>
    <div class="stat-pill"><span>BFS</span> &amp; <span>DFS</span> graph traversal</div>
    <div class="stat-pill"><span>Live</span> benchmarks</div>
    <div class="stat-pill"><span>Race</span> mode</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Tabs
# ─────────────────────────────────────────────
tabs = st.tabs(["🏁  Guide", "🔀  Sorting", "⚡  Race Mode", "🔎  Searching", "🧭  Graphs", "📈  Big-O", "🧪  Benchmark", "✅  Quiz"])


# ══════════════════════════════════════════════
#  TAB 0 — Guide
# ══════════════════════════════════════════════
with tabs[0]:
    c1, c2, c3 = st.columns(3, gap="medium")
    cards = [
        ("🔀", "Sorting", "card-accent",
         "Watch Bubble, Selection, Insertion, and Merge Sort move data step by step. Track swaps and comparisons live."),
        ("⚡", "Race Mode", "card-gold",
         "Run two algorithms head-to-head on the same array. See which wins — and by how much."),
        ("🧪", "Benchmark", "card-purple",
         "Generate real timing data across input sizes. Plot the curves and compare them to Big-O theory."),
    ]
    for col, (icon, title, cls, desc) in zip([c1, c2, c3], cards):
        with col:
            st.markdown(f"""
            <div class="card {cls}">
              <div style="font-size:1.8rem;margin-bottom:.5rem">{icon}</div>
              <div style="font-weight:600;font-size:1rem;margin-bottom:.4rem">{title}</div>
              <div style="color:var(--muted);font-size:.88rem;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-pink" style="margin-top:.5rem">
      <div class="section-label">Science fair tip</div>
      <div style="font-size:.95rem;line-height:1.7;color:var(--text)">
        Frame your project as an experiment: <em>"At what input size does algorithm choice start to matter — and by how much?"</em>
        Use the <strong>Benchmark</strong> tab to collect real data, then present the charts as your experimental results.
        The <strong>Race Mode</strong> tab makes a great live demo for judges.
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 1 — Sorting
# ══════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-label">Step-by-step visualizer</div>', unsafe_allow_html=True)
    colL, colR = st.columns([1, 2.5], gap="large")

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        algo = st.selectbox("Algorithm", ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"])
        n_sort = st.slider("Array size", 5, 40, 14, key="sort_n")
        max_sort = st.slider("Max value", 10, 200, 60, key="sort_max")
        speed_sort = st.slider("Delay per step (s)", 0.0, 0.4, 0.04, 0.01, key="sort_speed")
        seed_sort = st.number_input("Random seed", 0, 999999, 42, key="sort_seed")
        run_sort = st.button("▶ Run Demo", use_container_width=True, key="run_sort")
        st.markdown('</div>', unsafe_allow_html=True)

        complexity_map = {
            "Bubble Sort":    ("O(n²)", "O(n)", "O(n²)", "O(1)"),
            "Selection Sort": ("O(n²)", "O(n²)", "O(n²)", "O(1)"),
            "Insertion Sort": ("O(n²)", "O(n)", "O(n²)", "O(1)"),
            "Merge Sort":     ("O(n log n)", "O(n log n)", "O(n log n)", "O(n)"),
        }
        cases = complexity_map[algo]
        badge_cls = ["badge-red","badge-green","badge-red","badge-cyan"]
        labels = ["Worst","Best","Average","Space"]
        st.markdown('<div class="card card-accent" style="margin-top:.5rem">', unsafe_allow_html=True)
        st.markdown(f'<div class="section-label">{algo} complexity</div>', unsafe_allow_html=True)
        html_badges = "".join(
            f'<div style="margin:.25rem 0"><span style="color:var(--muted);font-size:.78rem;width:70px;display:inline-block">{l}</span>'
            f'<span class="badge {c}">{v}</span></div>'
            for l, c, v in zip(labels, badge_cls, cases)
        )
        st.markdown(html_badges + '</div>', unsafe_allow_html=True)

    with colR:
        random.seed(int(seed_sort))
        arr_sort = [random.randint(1, int(max_sort)) for _ in range(int(n_sort))]
        st.markdown(f'<div class="card" style="margin-bottom:.75rem"><span style="color:var(--muted);font-size:.8rem">Starting array → </span>'
                    f'<span style="font-family:var(--mono);font-size:.82rem;color:var(--accent)">{arr_sort}</span></div>',
                    unsafe_allow_html=True)

        if run_sort:
            if algo == "Bubble Sort":
                steps = bubble_sort_steps(arr_sort)
            elif algo == "Selection Sort":
                steps = selection_sort_steps(arr_sort)
            elif algo == "Insertion Sort":
                steps = insertion_sort_steps(arr_sort)
            else:
                steps = merge_sort_steps(arr_sort)

            chart_ph = st.empty()
            note_ph  = st.empty()
            m1, m2, m3 = st.columns(3)
            ctr_ph   = m1.empty()
            swap_ph  = m2.empty()
            comp_ph  = m3.empty()

            for idx, s in enumerate(steps):
                fig = plotly_array(s.array, hi=s.i, hj=s.j)
                chart_ph.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                note_ph.markdown(f'<div class="step-note">⟶ {s.note}</div>', unsafe_allow_html=True)
                ctr_ph.metric("Step", f"{idx+1}/{len(steps)}")
                swap_ph.metric("Swaps", s.swaps)
                comp_ph.metric("Comparisons", s.comparisons)
                if speed_sort > 0:
                    time.sleep(speed_sort)

            st.markdown('<div class="card card-accent"><span style="color:var(--success);font-weight:600">✓ Sorted!</span></div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 2 — Race Mode
# ══════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-label">Head-to-head algorithm race</div>', unsafe_allow_html=True)

    colL, colR = st.columns([1, 2.5], gap="large")
    sort_options = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"]

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        algo_a = st.selectbox("Algorithm A", sort_options, index=0, key="race_a")
        algo_b = st.selectbox("Algorithm B", sort_options, index=3, key="race_b")
        n_race = st.slider("Array size", 5, 60, 20, key="race_n")
        max_race = st.slider("Max value", 10, 200, 80, key="race_max")
        seed_race = st.number_input("Random seed", 0, 999999, 7, key="race_seed")
        array_type = st.selectbox("Array type", ["Random", "Nearly sorted", "Reversed"], key="race_type")
        run_race = st.button("▶ Start Race", use_container_width=True, key="run_race")
        st.markdown('</div>', unsafe_allow_html=True)

    with colR:
        random.seed(int(seed_race))
        base = [random.randint(1, int(max_race)) for _ in range(int(n_race))]
        if array_type == "Nearly sorted":
            base.sort()
            for _ in range(max(1, int(n_race)//10)):
                i, j = random.randrange(n_race), random.randrange(n_race)
                base[i], base[j] = base[j], base[i]
        elif array_type == "Reversed":
            base.sort(reverse=True)

        st.markdown(f'<div class="card" style="margin-bottom:.75rem"><span style="color:var(--muted);font-size:.8rem">Array ({array_type}) → </span>'
                    f'<span style="font-family:var(--mono);font-size:.8rem;color:var(--text)">{base}</span></div>',
                    unsafe_allow_html=True)

        if run_race:
            def get_steps(name, arr):
                if name == "Bubble Sort":    return bubble_sort_steps(arr)
                if name == "Selection Sort": return selection_sort_steps(arr)
                if name == "Insertion Sort": return insertion_sort_steps(arr)
                return merge_sort_steps(arr)

            steps_a = get_steps(algo_a, base[:])
            steps_b = get_steps(algo_b, base[:])

            # Show final stats table
            final_a = steps_a[-1]
            final_b = steps_b[-1]

            winner = algo_a if len(steps_a) <= len(steps_b) else algo_b
            winner_steps = min(len(steps_a), len(steps_b))

            table_html = f"""
            <table class="race-table" style="margin-bottom:1rem">
              <thead><tr><th>Metric</th><th style="color:#00e5ff">{algo_a}</th><th style="color:#ff4f7b">{algo_b}</th></tr></thead>
              <tbody>
                <tr><td>Total steps</td><td style="font-family:var(--mono)">{len(steps_a)}</td><td style="font-family:var(--mono)">{len(steps_b)}</td></tr>
                <tr><td>Comparisons</td><td style="font-family:var(--mono)">{final_a.comparisons}</td><td style="font-family:var(--mono)">{final_b.comparisons}</td></tr>
                <tr><td>Swaps</td><td style="font-family:var(--mono)">{final_a.swaps}</td><td style="font-family:var(--mono)">{final_b.swaps}</td></tr>
                <tr class="winner-row"><td>🏆 Winner</td><td colspan="2" style="font-weight:700">{winner} ({winner_steps} steps)</td></tr>
              </tbody>
            </table>"""
            st.markdown(table_html, unsafe_allow_html=True)

            # Side-by-side animated race
            ca, cb = st.columns(2)
            with ca:
                st.markdown(f'<div style="color:#00e5ff;font-weight:600;margin-bottom:.3rem">{algo_a}</div>', unsafe_allow_html=True)
                ph_a = st.empty()
                note_a = st.empty()
            with cb:
                st.markdown(f'<div style="color:#ff4f7b;font-weight:600;margin-bottom:.3rem">{algo_b}</div>', unsafe_allow_html=True)
                ph_b = st.empty()
                note_b = st.empty()

            max_steps = max(len(steps_a), len(steps_b))
            for k in range(max_steps):
                sa = steps_a[min(k, len(steps_a)-1)]
                sb = steps_b[min(k, len(steps_b)-1)]
                fig_a = plotly_array(sa.array, hi=sa.i, hj=sa.j, title=f"Step {min(k+1,len(steps_a))}/{len(steps_a)}")
                fig_b = plotly_array(sb.array, hi=sb.i, hj=sb.j, title=f"Step {min(k+1,len(steps_b))}/{len(steps_b)}")
                ph_a.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})
                ph_b.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
                note_a.markdown(f'<div class="step-note" style="border-left-color:#00e5ff;font-size:.78rem">{sa.note}</div>', unsafe_allow_html=True)
                note_b.markdown(f'<div class="step-note" style="border-left-color:#ff4f7b;font-size:.78rem">{sb.note}</div>', unsafe_allow_html=True)
                time.sleep(0.05)

            st.markdown(f'<div class="card card-gold" style="margin-top:.75rem"><span style="color:var(--gold);font-weight:700">🏆 {winner} wins!</span></div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 3 — Searching
# ══════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-label">Step-by-step search visualizer</div>', unsafe_allow_html=True)
    colL, colR = st.columns([1, 2.5], gap="large")

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        search_algo = st.selectbox("Algorithm", ["Linear Search", "Binary Search (sorted)"], key="search_algo")
        n_search = st.slider("Array size", 5, 50, 18, key="search_n")
        max_search = st.slider("Max value", 10, 300, 80, key="search_max")
        seed_search = st.number_input("Random seed", 0, 999999, 7, key="search_seed")
        speed_search = st.slider("Delay per step (s)", 0.0, 0.5, 0.07, 0.01, key="search_speed")
        run_search = st.button("▶ Run Search", use_container_width=True, key="run_search")
        st.markdown('</div>', unsafe_allow_html=True)

    with colR:
        random.seed(int(seed_search))
        arr_search = [random.randint(1, int(max_search)) for _ in range(int(n_search))]
        if search_algo.startswith("Binary"):
            arr_search.sort()

        st.markdown(f'<div class="card" style="margin-bottom:.75rem"><span style="color:var(--muted);font-size:.8rem">Array → </span>'
                    f'<span style="font-family:var(--mono);font-size:.82rem;color:var(--text)">{arr_search}</span></div>',
                    unsafe_allow_html=True)

        target = st.number_input("Target to find", min_value=1, max_value=int(max_search),
                                 value=arr_search[len(arr_search)//2], key="search_target")

        if run_search:
            if search_algo == "Linear Search":
                steps = linear_search_steps(arr_search, int(target))
                desc = "Checks items one by one from index 0. Simple but slow for large arrays: <span class='badge badge-yellow'>O(n)</span>"
            else:
                steps = binary_search_steps(arr_search, int(target))
                desc = "Halves the search range each step. Requires sorted array but very fast: <span class='badge badge-green'>O(log n)</span>"

            st.markdown(f'<div class="card card-accent" style="margin-bottom:.75rem;font-size:.88rem">{desc}</div>',
                        unsafe_allow_html=True)

            chart_ph = st.empty()
            note_ph  = st.empty()
            step_m   = st.empty()

            for idx, s in enumerate(steps):
                fig = plotly_array(s.array, hi=s.i, hj=s.j)
                chart_ph.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                note_ph.markdown(f'<div class="step-note">{s.note}</div>', unsafe_allow_html=True)
                step_m.metric("Steps taken", idx+1)
                if speed_search > 0:
                    time.sleep(speed_search)


# ══════════════════════════════════════════════
#  TAB 4 — Graphs
# ══════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-label">Graph traversal: BFS vs DFS</div>', unsafe_allow_html=True)
    st.markdown('<div class="card card-purple" style="font-size:.88rem;color:var(--muted);line-height:1.6;margin-bottom:1rem">Graphs are sets of <b style="color:var(--text)">nodes</b> connected by <b style="color:var(--text)">edges</b>. BFS explores level-by-level using a queue; DFS dives deep along one path first using recursion.</div>',
                unsafe_allow_html=True)

    colL, colR = st.columns([1, 2], gap="large")

    default_adj = {"A":["B","C"],"B":["D","E"],"C":["F"],"D":[],"E":["F"],"F":[]}

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        text_adj = st.text_area(
            "Adjacency list (node: neighbor1, neighbor2, ...)",
            value="\n".join([f"{k}: {', '.join(v)}" for k, v in default_adj.items()]),
            height=190, key="adj_text")
        start_node = st.text_input("Start node", value="A", key="start_node")
        trav = st.radio("Traversal type", ["BFS", "DFS"], horizontal=True, key="trav_type")
        run_graph = st.button("▶ Run Traversal", use_container_width=True, key="run_graph")
        st.markdown('</div>', unsafe_allow_html=True)

    with colR:
        try:
            adj = parse_adj(text_adj)
            st.markdown('<div class="card" style="margin-bottom:.75rem">', unsafe_allow_html=True)
            st.write("**Parsed adjacency list**")
            st.json(adj, expanded=False)
            st.markdown('</div>', unsafe_allow_html=True)

            if run_graph:
                if start_node not in adj:
                    st.error("Start node not found.")
                else:
                    if trav == "BFS":
                        order = bfs_steps(adj, start_node)
                        color = "#00e5ff"
                        desc = "BFS uses a **queue**: visits all neighbors before going deeper."
                    else:
                        order = dfs_steps(adj, start_node)
                        color = "#b47cff"
                        desc = "DFS uses a **stack/recursion**: goes as deep as possible before backtracking."

                    # Animated traversal path
                    path_ph = st.empty()
                    for k in range(1, len(order)+1):
                        path_str = " → ".join(
                            f'<span style="color:{color};font-weight:700">{n}</span>' if i == k-1
                            else f'<span style="color:var(--muted)">{n}</span>'
                            for i, n in enumerate(order[:k])
                        )
                        path_ph.markdown(
                            f'<div class="card" style="font-family:var(--mono);font-size:.95rem">{path_str}</div>',
                            unsafe_allow_html=True)
                        time.sleep(0.35)

                    st.markdown(f'<div class="card card-purple" style="margin-top:.5rem;font-size:.88rem">{desc}</div>',
                                unsafe_allow_html=True)

                    if trav == "BFS":
                        level = {start_node: 0}
                        q = [start_node]
                        while q:
                            u = q.pop(0)
                            for v in adj.get(u, []):
                                if v not in level:
                                    level[v] = level[u] + 1
                                    q.append(v)
                        df = pd.DataFrame(sorted(level.items(), key=lambda x: x[1]), columns=["Node", "BFS Level"])
                        st.dataframe(df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Could not parse graph: {e}")


# ══════════════════════════════════════════════
#  TAB 5 — Big-O
# ══════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-label">Time complexity reference</div>', unsafe_allow_html=True)

    bigo_data = [
        ("O(1)",       "Constant",      "badge-green",  "Array index access, hash lookup, stack push"),
        ("O(log n)",   "Logarithmic",   "badge-cyan",   "Binary search on sorted array"),
        ("O(n)",       "Linear",        "badge-cyan",   "Linear search, single loop scan"),
        ("O(n log n)", "Linearithmic",  "badge-yellow", "Merge sort, heap sort"),
        ("O(n²)",      "Quadratic",     "badge-orange", "Bubble, selection, insertion sort (worst)"),
        ("O(2ⁿ)",      "Exponential",   "badge-red",    "Brute-force subsets"),
        ("O(n!)",      "Factorial",     "badge-red",    "Brute-force travelling salesman"),
    ]

    table_html = '<table class="race-table"><thead><tr><th>Notation</th><th>Name</th><th>Common examples</th></tr></thead><tbody>'
    for notation, name, badge, example in bigo_data:
        table_html += f'<tr><td><span class="badge {badge}">{notation}</span></td><td style="color:var(--muted)">{name}</td><td style="font-size:.85rem">{example}</td></tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown('<br><div class="section-label">Growth comparison</div>', unsafe_allow_html=True)

    n_bigo = st.slider("Max n", 10, 300, 100, key="bigo_n")
    ns = list(range(1, n_bigo + 1))

    fig_bigo = go.Figure()
    curves = [
        ("O(log n)",   [math.log2(n) for n in ns],              "#06d6a0"),
        ("O(n)",       [float(n) for n in ns],                   "#00e5ff"),
        ("O(n log n)", [n * math.log2(n) for n in ns],           "#ffd166"),
        ("O(n²)",      [float(n*n) for n in ns],                  "#ff4f7b"),
    ]
    for label, ys, color in curves:
        fig_bigo.add_trace(go.Scatter(x=ns, y=ys, name=label, line=dict(color=color, width=2.5),
                                     hovertemplate=f"{label}: %{{y:.0f}}<extra></extra>"))

    fig_bigo.update_layout(
        paper_bgcolor=PLOT_PAPER, plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family="Space Grotesk"),
        xaxis=dict(title="n (input size)", gridcolor=GRID_COLOR, color=FONT_COLOR),
        yaxis=dict(title="Operations (rough)", gridcolor=GRID_COLOR, color=FONT_COLOR),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR, borderwidth=1),
        height=380, margin=dict(l=50, r=20, t=20, b=50),
    )
    st.plotly_chart(fig_bigo, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════
#  TAB 6 — Benchmark (science fair killer feature)
# ══════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-label">Empirical experiment — real timing data</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card card-purple" style="font-size:.88rem;line-height:1.7;color:var(--muted)">
      This tab runs each algorithm on arrays of increasing size and records real wall-clock time.
      It's the <b style="color:var(--text)">experimental result</b> section of your science fair project —
      compare the measured curves to the theoretical Big-O curves above.
    </div>""", unsafe_allow_html=True)

    colL, colR = st.columns([1, 2.5], gap="large")

    with colL:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        bench_algos = st.multiselect(
            "Algorithms to benchmark",
            ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort"],
            default=["Bubble Sort", "Insertion Sort", "Merge Sort"],
            key="bench_algos")
        bench_max_n = st.slider("Maximum n", 100, 3000, 800, 50, key="bench_n")
        bench_steps_n = st.slider("Number of data points", 5, 20, 10, key="bench_steps")
        bench_type = st.selectbox("Input type", ["Random", "Nearly sorted", "Reversed"], key="bench_type")
        bench_seed = st.number_input("Seed", 0, 999999, 0, key="bench_seed")
        run_bench = st.button("▶ Run Experiment", use_container_width=True, key="run_bench")
        st.markdown('</div>', unsafe_allow_html=True)

    with colR:
        if run_bench and bench_algos:
            ns_bench = [max(5, int(bench_max_n * i / bench_steps_n))
                        for i in range(1, bench_steps_n + 1)]

            def make_arr(n):
                random.seed(int(bench_seed))
                a = [random.randint(1, 1000) for _ in range(n)]
                if bench_type == "Nearly sorted":
                    a.sort()
                    for _ in range(max(1, n//10)):
                        i, j = random.randrange(n), random.randrange(n)
                        a[i], a[j] = a[j], a[i]
                elif bench_type == "Reversed":
                    a.sort(reverse=True)
                return a

            def time_algo(name, arr):
                a = arr[:]
                t0 = timeit.default_timer()
                if name == "Bubble Sort":
                    n = len(a)
                    for i in range(n):
                        swapped = False
                        for j in range(n-i-1):
                            if a[j] > a[j+1]:
                                a[j], a[j+1] = a[j+1], a[j]
                                swapped = True
                        if not swapped: break
                elif name == "Selection Sort":
                    n = len(a)
                    for i in range(n):
                        m = i
                        for j in range(i+1, n):
                            if a[j] < a[m]: m = j
                        a[i], a[m] = a[m], a[i]
                elif name == "Insertion Sort":
                    for i in range(1, len(a)):
                        k = a[i]; j = i-1
                        while j >= 0 and a[j] > k:
                            a[j+1] = a[j]; j -= 1
                        a[j+1] = k
                elif name == "Merge Sort":
                    def ms(x):
                        if len(x) <= 1: return x
                        m = len(x)//2
                        L, R = ms(x[:m]), ms(x[m:])
                        res = []; i = j = 0
                        while i < len(L) and j < len(R):
                            if L[i] <= R[j]: res.append(L[i]); i += 1
                            else: res.append(R[j]); j += 1
                        res.extend(L[i:]); res.extend(R[j:])
                        return res
                    ms(a)
                return (timeit.default_timer() - t0) * 1000  # ms

            results: Dict[str, List[float]] = {a: [] for a in bench_algos}
            progress = st.progress(0, text="Running experiment…")

            total_ops = len(ns_bench) * len(bench_algos)
            op = 0
            for n in ns_bench:
                arr_b = make_arr(n)
                for algo_name in bench_algos:
                    results[algo_name].append(time_algo(algo_name, arr_b))
                    op += 1
                    progress.progress(op / total_ops, text=f"Testing n={n}…")

            progress.empty()

            # Plot
            colors_b = {"Bubble Sort": "#ff4f7b", "Selection Sort": "#ffd166",
                        "Insertion Sort": "#00e5ff", "Merge Sort": "#b47cff"}

            fig_b = go.Figure()
            for algo_name in bench_algos:
                fig_b.add_trace(go.Scatter(
                    x=ns_bench, y=results[algo_name],
                    name=algo_name,
                    mode="lines+markers",
                    line=dict(color=colors_b.get(algo_name, "#fff"), width=2.5),
                    marker=dict(size=6),
                    hovertemplate=f"{algo_name}<br>n=%{{x}}<br>%{{y:.2f}} ms<extra></extra>"))

            fig_b.update_layout(
                paper_bgcolor=PLOT_PAPER, plot_bgcolor=PLOT_BG,
                font=dict(color=FONT_COLOR, family="Space Grotesk"),
                xaxis=dict(title="n (input size)", gridcolor=GRID_COLOR, color=FONT_COLOR),
                yaxis=dict(title="Time (ms)", gridcolor=GRID_COLOR, color=FONT_COLOR),
                legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR, borderwidth=1),
                height=380, margin=dict(l=50, r=20, t=20, b=50),
            )
            st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})

            # Summary table
            df_bench = pd.DataFrame(results, index=[f"n={n}" for n in ns_bench])
            df_bench.index.name = "Input size"
            df_bench = df_bench.applymap(lambda x: f"{x:.3f} ms")
            st.dataframe(df_bench, use_container_width=True)

            # Insight
            fastest = min(bench_algos, key=lambda a: results[a][-1])
            st.markdown(f"""
            <div class="card card-gold" style="margin-top:.75rem;font-size:.9rem;line-height:1.7">
              <div class="section-label">Experiment finding</div>
              At n={ns_bench[-1]}, <b style="color:var(--gold)">{fastest}</b> was the fastest algorithm on <b>{bench_type.lower()}</b> input.
              <br>Notice how O(n²) algorithms curve sharply upward while O(n log n) stays relatively flat — that's Big-O theory confirmed by real data.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="color:var(--muted);font-size:.9rem;line-height:1.7">
              Select at least one algorithm on the left, then click <b style="color:var(--text)">Run Experiment</b>.<br><br>
              The chart will show real measured time in milliseconds across different input sizes.
              This is your experimental data — compare the curve shapes to the Big-O chart in the previous tab.
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB 7 — Quiz
# ══════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-label">Knowledge check</div>', unsafe_allow_html=True)

    questions = [
        {"q": "Binary search requires the array to be…",
         "opts": ["random", "sorted", "reversed", "all equal"],
         "ans": 1, "why": "Binary search halves its search range by comparing to the middle — that only works if the array is in order."},
        {"q": "Which traversal explores nodes level-by-level?",
         "opts": ["DFS", "Insertion Sort", "BFS", "Selection Sort"],
         "ans": 2, "why": "BFS uses a queue and visits all neighbors before going deeper, so it naturally explores by level."},
        {"q": "Which grows slowest for large n?",
         "opts": ["O(n²)", "O(n log n)", "O(2ⁿ)", "O(n!)"],
         "ans": 1, "why": "O(n log n) is far slower than O(1) or O(log n) but much faster than the other options listed."},
        {"q": "Bubble sort mainly works by…",
         "opts": ["choosing the smallest item each pass", "swapping adjacent out-of-order items", "splitting into halves", "inserting into a sorted section"],
         "ans": 1, "why": "Bubble sort compares neighbors and swaps until the largest element 'bubbles' to the end each pass."},
        {"q": "Merge sort's time complexity is…",
         "opts": ["O(n²)", "O(n)", "O(n log n)", "O(log n)"],
         "ans": 2, "why": "Merge sort divides the array in half (log n levels) and merges in linear time at each level → O(n log n)."},
        {"q": "What data structure does BFS use internally?",
         "opts": ["Stack", "Queue", "Heap", "Hash table"],
         "ans": 1, "why": "BFS uses a queue (FIFO) to ensure it processes nodes level by level."},
    ]

    user_answers = []
    for idx, item in enumerate(questions):
        st.markdown(f'<div class="card" style="margin-bottom:.6rem"><div class="quiz-q">Q{idx+1}: {item["q"]}</div></div>',
                    unsafe_allow_html=True)
        choice = st.radio("", item["opts"], index=0, key=f"quiz_{idx}", horizontal=True, label_visibility="collapsed")
        user_answers.append(item["opts"].index(choice))

    if st.button("✅ Check Answers", use_container_width=False, key="quiz_submit"):
        score = sum(1 for i, item in enumerate(questions) if user_answers[i] == item["ans"])
        for i, item in enumerate(questions):
            correct = item["ans"]
            if user_answers[i] == correct:
                st.markdown(f'<div class="card card-accent"><b style="color:var(--success)">Q{i+1} ✓ Correct</b><br><span style="color:var(--muted);font-size:.85rem">{item["why"]}</span></div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="card card-pink"><b style="color:var(--accent2)">Q{i+1} ✗ Not quite — correct: {item["opts"][correct]}</b><br><span style="color:var(--muted);font-size:.85rem">{item["why"]}</span></div>',
                            unsafe_allow_html=True)

        pct = score / len(questions)
        color = "#06d6a0" if pct >= 0.8 else ("#ffd166" if pct >= 0.5 else "#ff4f7b")
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:2rem;margin-top:1rem">
          <div style="font-size:3rem;font-family:var(--mono);color:{color};font-weight:700">{score}/{len(questions)}</div>
          <div style="color:var(--muted);margin-top:.4rem">{"Excellent — you've mastered this!" if pct==1 else "Good work!" if pct>=0.8 else "Keep reviewing — you're getting there!"}</div>
        </div>""", unsafe_allow_html=True)
