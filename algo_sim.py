# app.py
# Streamlit Algorithms Learning / Simulator
# Run: streamlit run app.py

from __future__ import annotations
import time
import random
import heapq
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Iterable

import streamlit as st

st.set_page_config(page_title="Algorithms Learning Simulator", page_icon="🧠", layout="wide")
st.title("🧠 Algorithms Learning / Simulator")
st.caption("Interactive mini-simulators for common algorithms: sorting, graph pathfinding, and searching.")


# -----------------------------
# Helpers
# -----------------------------
def sleep_ms(ms: int):
    time.sleep(ms / 1000)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def colored_bar(values: List[int], highlight: Optional[set] = None) -> str:
    """Render an ASCII-ish bar chart using Markdown."""
    highlight = highlight or set()
    m = max(values) if values else 1
    lines = []
    for i, v in enumerate(values):
        blocks = int(1 + 20 * v / m)
        bar = "█" * blocks
        if i in highlight:
            lines.append(f"`{i:02d}` **{bar}**  ({v})")
        else:
            lines.append(f"`{i:02d}` {bar}  ({v})")
    return "\n".join(lines)


# -----------------------------
# Sorting Simulators
# -----------------------------
def bubble_sort_steps(arr: List[int]) -> Iterable[Tuple[List[int], set]]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            hl = {j, j + 1}
            yield a[:], hl
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                yield a[:], hl
        if not swapped:
            break
    yield a[:], set()


def insertion_sort_steps(arr: List[int]) -> Iterable[Tuple[List[int], set]]:
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        yield a[:], {i}
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            yield a[:], {j, j + 1}
            j -= 1
        a[j + 1] = key
        yield a[:], {j + 1}
    yield a[:], set()


def selection_sort_steps(arr: List[int]) -> Iterable[Tuple[List[int], set]]:
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield a[:], {min_idx, j}
            if a[j] < a[min_idx]:
                min_idx = j
                yield a[:], {min_idx, i}
        a[i], a[min_idx] = a[min_idx], a[i]
        yield a[:], {i, min_idx}
    yield a[:], set()


# -----------------------------
# Searching Simulators
# -----------------------------
def linear_search_steps(arr: List[int], target: int) -> Iterable[Tuple[int, Optional[int]]]:
    """Yields (index_being_checked, found_index_or_None_if_not_yet)."""
    for i, v in enumerate(arr):
        yield i, None
        if v == target:
            yield i, i
            return
    yield -1, None


def binary_search_steps(arr_sorted: List[int], target: int) -> Iterable[Tuple[int, int, int, Optional[int]]]:
    """Yields (lo, mid, hi, found_index_or_None_if_not_yet)."""
    lo, hi = 0, len(arr_sorted) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        yield lo, mid, hi, None
        if arr_sorted[mid] == target:
            yield lo, mid, hi, mid
            return
        if arr_sorted[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    yield lo, -1, hi, None


# -----------------------------
# Grid Pathfinding (BFS / Dijkstra / A*)
# -----------------------------
@dataclass(frozen=True)
class Node:
    r: int
    c: int


def neighbors(n: Node, rows: int, cols: int):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = n.r + dr, n.c + dc
        if 0 <= rr < rows and 0 <= cc < cols:
            yield Node(rr, cc)


def manhattan(a: Node, b: Node) -> int:
    return abs(a.r - b.r) + abs(a.c - b.c)


def reconstruct_path(prev: Dict[Node, Node], end: Node) -> List[Node]:
    path = [end]
    while end in prev:
        end = prev[end]
        path.append(end)
    path.reverse()
    return path


def bfs_steps(grid: List[List[int]], start: Node, goal: Node):
    """grid: 0=free, 1=wall"""
    rows, cols = len(grid), len(grid[0])
    q = [start]
    visited = {start}
    prev: Dict[Node, Node] = {}

    while q:
        cur = q.pop(0)
        yield {"current": cur, "frontier": set(q), "visited": set(visited), "path": None, "done": False}
        if cur == goal:
            path = reconstruct_path(prev, goal)
            yield {"current": cur, "frontier": set(q), "visited": set(visited), "path": path, "done": True}
            return
        for nb in neighbors(cur, rows, cols):
            if grid[nb.r][nb.c] == 1:
                continue
            if nb in visited:
                continue
            visited.add(nb)
            prev[nb] = cur
            q.append(nb)

    yield {"current": None, "frontier": set(), "visited": set(visited), "path": None, "done": True}


def dijkstra_steps(grid: List[List[int]], start: Node, goal: Node, weight: int = 1):
    rows, cols = len(grid), len(grid[0])
    dist: Dict[Node, float] = {start: 0.0}
    prev: Dict[Node, Node] = {}
    pq: List[Tuple[float, Node]] = [(0.0, start)]
    visited: set[Node] = set()

    while pq:
        d, cur = heapq.heappop(pq)
        if cur in visited:
            continue
        visited.add(cur)

        yield {"current": cur, "frontier": {n for _, n in pq}, "visited": set(visited), "dist": dict(dist), "path": None, "done": False}

        if cur == goal:
            path = reconstruct_path(prev, goal)
            yield {"current": cur, "frontier": {n for _, n in pq}, "visited": set(visited), "dist": dict(dist), "path": path, "done": True}
            return

        for nb in neighbors(cur, rows, cols):
            if grid[nb.r][nb.c] == 1:
                continue
            nd = d + weight
            if nb not in dist or nd < dist[nb]:
                dist[nb] = nd
                prev[nb] = cur
                heapq.heappush(pq, (nd, nb))

    yield {"current": None, "frontier": set(), "visited": set(visited), "dist": dict(dist), "path": None, "done": True}


def astar_steps(grid: List[List[int]], start: Node, goal: Node):
    rows, cols = len(grid), len(grid[0])
    g: Dict[Node, float] = {start: 0.0}
    f: Dict[Node, float] = {start: float(manhattan(start, goal))}
    prev: Dict[Node, Node] = {}
    pq: List[Tuple[float, Node]] = [(f[start], start)]
    closed: set[Node] = set()

    while pq:
        _, cur = heapq.heappop(pq)
        if cur in closed:
            continue
        closed.add(cur)

        yield {"current": cur, "frontier": {n for _, n in pq}, "visited": set(closed), "g": dict(g), "path": None, "done": False}

        if cur == goal:
            path = reconstruct_path(prev, goal)
            yield {"current": cur, "frontier": {n for _, n in pq}, "visited": set(closed), "g": dict(g), "path": path, "done": True}
            return

        for nb in neighbors(cur, rows, cols):
            if grid[nb.r][nb.c] == 1:
                continue
            tentative = g[cur] + 1.0
            if nb not in g or tentative < g[nb]:
                prev[nb] = cur
                g[nb] = tentative
                f[nb] = tentative + manhattan(nb, goal)
                heapq.heappush(pq, (f[nb], nb))

    yield {"current": None, "frontier": set(), "visited": set(closed), "g": dict(g), "path": None, "done": True}


def render_grid(grid: List[List[int]], start: Node, goal: Node, visited: set[Node], frontier: set[Node], path: Optional[List[Node]]):
    rows, cols = len(grid), len(grid[0])
    path_set = set(path) if path else set()

    # Use emoji squares for clarity
    lines = []
    for r in range(rows):
        row_cells = []
        for c in range(cols):
            n = Node(r, c)
            if n == start:
                row_cells.append("🟩")  # start
            elif n == goal:
                row_cells.append("🟥")  # goal
            elif grid[r][c] == 1:
                row_cells.append("⬛")  # wall
            elif n in path_set:
                row_cells.append("🟨")  # final path
            elif n in frontier:
                row_cells.append("🟦")  # frontier
            elif n in visited:
                row_cells.append("🟪")  # visited
            else:
                row_cells.append("⬜")  # empty
        lines.append("".join(row_cells))
    return "\n".join(lines)


# -----------------------------
# Sidebar: choose module
# -----------------------------
with st.sidebar:
    st.header("🎛 Simulator")
    mode = st.radio("Choose a topic", ["Sorting", "Pathfinding", "Searching"], index=0)

    st.divider()
    st.subheader("⏱ Animation")
    speed = st.slider("Speed (ms per step)", 0, 500, 120, 10)
    auto_play = st.toggle("Auto-play", value=True)
    steps_per_tick = st.slider("Steps per tick", 1, 10, 1)

    st.divider()
    st.caption("Tip: turn off Auto-play to step manually.")


# -----------------------------
# Sorting UI
# -----------------------------
if mode == "Sorting":
    st.subheader("🔀 Sorting Visualizer")

    colA, colB = st.columns([1, 2])

    with colA:
        algo = st.selectbox("Algorithm", ["Bubble Sort", "Insertion Sort", "Selection Sort"])
        n = st.slider("Number of items", 5, 40, 18)
        maxv = st.slider("Max value", 10, 200, 100)

        if "sort_arr" not in st.session_state:
            st.session_state.sort_arr = [random.randint(1, maxv) for _ in range(n)]

        if st.button("🎲 Randomize array", use_container_width=True):
            st.session_state.sort_arr = [random.randint(1, maxv) for _ in range(n)]
            st.session_state.sort_iter = None

        if st.button("🔁 Reset (keep array)", use_container_width=True):
            st.session_state.sort_iter = None

        st.write("Array:", st.session_state.sort_arr)

    with colB:
        if "sort_iter" not in st.session_state:
            st.session_state.sort_iter = None

        arr = st.session_state.sort_arr[:]
        if st.session_state.sort_iter is None:
            if algo == "Bubble Sort":
                st.session_state.sort_iter = iter(bubble_sort_steps(arr))
            elif algo == "Insertion Sort":
                st.session_state.sort_iter = iter(insertion_sort_steps(arr))
            else:
                st.session_state.sort_iter = iter(selection_sort_steps(arr))

        placeholder = st.empty()
        info = st.empty()
        manual_col1, manual_col2 = st.columns([1, 1])

        def do_steps(k: int):
            last_state = None
            try:
                for _ in range(k):
                    last_state = next(st.session_state.sort_iter)
            except StopIteration:
                pass
            return last_state

        if auto_play:
            state = do_steps(steps_per_tick)
            if state is None:
                state = (st.session_state.sort_arr[:], set())
            values, hl = state
            placeholder.markdown(colored_bar(values, hl))
            info.write("Highlighted bars = elements being compared/moved.")
            sleep_ms(speed)
            st.rerun()
        else:
            with manual_col1:
                if st.button("➡️ Step", use_container_width=True):
                    state = do_steps(1)
                    if state is None:
                        state = (st.session_state.sort_arr[:], set())
                    values, hl = state
                    placeholder.markdown(colored_bar(values, hl))
            with manual_col2:
                if st.button("⏩ Step x10", use_container_width=True):
                    state = do_steps(10)
                    if state is None:
                        state = (st.session_state.sort_arr[:], set())
                    values, hl = state
                    placeholder.markdown(colored_bar(values, hl))
            info.write("Use Step to see each comparison/move.")


# -----------------------------
# Pathfinding UI
# -----------------------------
elif mode == "Pathfinding":
    st.subheader("🧭 Grid Pathfinding Simulator")

    colA, colB = st.columns([1, 2])

    with colA:
        alg = st.selectbox("Algorithm", ["BFS (unweighted)", "Dijkstra", "A* (Manhattan heuristic)"])
        rows = st.slider("Rows", 6, 20, 10)
        cols = st.slider("Cols", 6, 30, 18)
        wall_pct = st.slider("Wall density (%)", 0, 45, 20)

        start = Node(0, 0)
        goal = Node(rows - 1, cols - 1)

        if "grid" not in st.session_state or st.session_state.get("grid_shape") != (rows, cols, wall_pct):
            grid = [[0 for _ in range(cols)] for _ in range(rows)]
            # place random walls (avoid start/goal)
            for r in range(rows):
                for c in range(cols):
                    if (r, c) in [(start.r, start.c), (goal.r, goal.c)]:
                        continue
                    if random.randint(1, 100) <= wall_pct:
                        grid[r][c] = 1
            st.session_state.grid = grid
            st.session_state.grid_shape = (rows, cols, wall_pct)
            st.session_state.path_iter = None

        if st.button("🎲 New grid", use_container_width=True):
            st.session_state.grid_shape = None  # force regen on rerun
            st.rerun()

        if st.button("🔁 Reset run", use_container_width=True):
            st.session_state.path_iter = None

        st.markdown(
            """
**Legend:**  
🟩 start • 🟥 goal • ⬛ wall • 🟦 frontier • 🟪 visited • 🟨 final path • ⬜ empty
"""
        )

    with colB:
        grid = st.session_state.grid

        if "path_iter" not in st.session_state:
            st.session_state.path_iter = None

        if st.session_state.path_iter is None:
            if alg.startswith("BFS"):
                st.session_state.path_iter = iter(bfs_steps(grid, start, goal))
            elif alg.startswith("Dijkstra"):
                st.session_state.path_iter = iter(dijkstra_steps(grid, start, goal))
            else:
                st.session_state.path_iter = iter(astar_steps(grid, start, goal))

        grid_box = st.empty()
        stats = st.empty()
        manual_col1, manual_col2 = st.columns([1, 1])

        def step_path(k: int):
            last = None
            try:
                for _ in range(k):
                    last = next(st.session_state.path_iter)
            except StopIteration:
                pass
            return last

        if auto_play:
            state = step_path(steps_per_tick)
            if state is None:
                state = {"current": None, "frontier": set(), "visited": set(), "path": None, "done": True}
            txt = render_grid(grid, start, goal, state["visited"], state["frontier"], state["path"])
            grid_box.text(txt)

            path_len = len(state["path"]) if state.get("path") else 0
            stats.write(f"Visited: **{len(state['visited'])}** • Frontier: **{len(state['frontier'])}** • Path length: **{path_len}**")
            if state.get("done"):
                st.success("Done! Reset run or generate a new grid.")
                st.stop()
            sleep_ms(speed)
            st.rerun()
        else:
            with manual_col1:
                if st.button("➡️ Step", use_container_width=True):
                    state = step_path(1)
                    if state is None:
                        state = {"current": None, "frontier": set(), "visited": set(), "path": None, "done": True}
                    txt = render_grid(grid, start, goal, state["visited"], state["frontier"], state["path"])
                    grid_box.text(txt)
            with manual_col2:
                if st.button("⏩ Step x20", use_container_width=True):
                    state = step_path(20)
                    if state is None:
                        state = {"current": None, "frontier": set(), "visited": set(), "path": None, "done": True}
                    txt = render_grid(grid, start, goal, state["visited"], state["frontier"], state["path"])
                    grid_box.text(txt)
            stats.info("Use Step to watch the frontier grow and the path appear at the end.")


# -----------------------------
# Searching UI
# -----------------------------
else:
    st.subheader("🔎 Searching Simulator")

    colA, colB = st.columns([1, 2])

    with colA:
        n = st.slider("Array size", 5, 60, 25)
        maxv = st.slider("Max value", 10, 200, 80)

        if "search_arr" not in st.session_state:
            st.session_state.search_arr = sorted([random.randint(1, maxv) for _ in range(n)])

        if st.button("🎲 New sorted array", use_container_width=True):
            st.session_state.search_arr = sorted([random.randint(1, maxv) for _ in range(n)])
            st.session_state.search_lin_iter = None
            st.session_state.search_bin_iter = None

        arr = st.session_state.search_arr
        st.write("Array (sorted):")
        st.code(arr)

        target = st.number_input("Target value", min_value=0, max_value=500, value=int(arr[len(arr)//2]))

        algo = st.selectbox("Algorithm", ["Linear Search", "Binary Search"])

        if st.button("🔁 Reset search", use_container_width=True):
            st.session_state.search_lin_iter = None
            st.session_state.search_bin_iter = None

    with colB:
        placeholder = st.empty()
        info = st.empty()

        def render_indices(arr, active=None, lo=None, mid=None, hi=None, found=None):
            parts = []
            for i, v in enumerate(arr):
                tag = ""
                if found is not None and i == found:
                    tag = "✅"
                elif mid is not None and i == mid:
                    tag = "🎯"
                elif active is not None and i == active:
                    tag = "👀"
                elif lo is not None and hi is not None and (i == lo or i == hi):
                    tag = "📌"
                parts.append(f"{v:3d}{tag}")
            return " ".join(parts)

        if algo == "Linear Search":
            if "search_lin_iter" not in st.session_state:
                st.session_state.search_lin_iter = None
            if st.session_state.search_lin_iter is None:
                st.session_state.search_lin_iter = iter(linear_search_steps(arr, int(target)))

            def step(k: int):
                last = None
                try:
                    for _ in range(k):
                        last = next(st.session_state.search_lin_iter)
                except StopIteration:
                    pass
                return last

            manual_col1, manual_col2 = st.columns([1, 1])

            if auto_play:
                state = step(steps_per_tick)
                if state is None:
                    state = (-1, None)
                i, found = state
                placeholder.code(render_indices(arr, active=i if i >= 0 else None, found=found))
                if found is not None:
                    st.success(f"Found {target} at index {found}.")
                    st.stop()
                sleep_ms(speed)
                st.rerun()
            else:
                with manual_col1:
                    if st.button("➡️ Step", use_container_width=True):
                        state = step(1)
                        if state is None:
                            state = (-1, None)
                        i, found = state
                        placeholder.code(render_indices(arr, active=i if i >= 0 else None, found=found))
                        if found is not None:
                            st.success(f"Found {target} at index {found}.")
                with manual_col2:
                    if st.button("⏩ Step x10", use_container_width=True):
                        state = step(10)
                        if state is None:
                            state = (-1, None)
                        i, found = state
                        placeholder.code(render_indices(arr, active=i if i >= 0 else None, found=found))
                        if found is not None:
                            st.success(f"Found {target} at index {found}.")
            info.write("👀 = current check, ✅ = found")

        else:
            if "search_bin_iter" not in st.session_state:
                st.session_state.search_bin_iter = None
            if st.session_state.search_bin_iter is None:
                st.session_state.search_bin_iter = iter(binary_search_steps(arr, int(target)))

            def step(k: int):
                last = None
                try:
                    for _ in range(k):
                        last = next(st.session_state.search_bin_iter)
                except StopIteration:
                    pass
                return last

            manual_col1, manual_col2 = st.columns([1, 1])

            if auto_play:
                state = step(steps_per_tick)
                if state is None:
                    state = (0, -1, len(arr) - 1, None)
                lo, mid, hi, found = state
                placeholder.code(render_indices(arr, lo=lo, mid=mid if mid >= 0 else None, hi=hi, found=found))
                if found is not None:
                    st.success(f"Found {target} at index {found}.")
                    st.stop()
                if mid == -1:
                    st.warning(f"{target} not found.")
                    st.stop()
                sleep_ms(speed)
                st.rerun()
            else:
                with manual_col1:
                    if st.button("➡️ Step", use_container_width=True):
                        state = step(1)
                        if state is None:
                            state = (0, -1, len(arr) - 1, None)
                        lo, mid, hi, found = state
                        placeholder.code(render_indices(arr, lo=lo, mid=mid if mid >= 0 else None, hi=hi, found=found))
                        if found is not None:
                            st.success(f"Found {target} at index {found}.")
                with manual_col2:
                    if st.button("⏩ Step x10", use_container_width=True):
                        state = step(10)
                        if state is None:
                            state = (0, -1, len(arr) - 1, None)
                        lo, mid, hi, found = state
                        placeholder.code(render_indices(arr, lo=lo, mid=mid if mid >= 0 else None, hi=hi, found=found))
                        if found is not None:
                            st.success(f"Found {target} at index {found}.")
            info.write("📌 = lo/hi bounds, 🎯 = mid, ✅ = found")


st.divider()
st.subheader("📌 Ideas to extend this project")
st.markdown(
    """
- Add **Merge Sort / Quick Sort** with recursion visualization  
- Add **Minimum Spanning Tree** (Kruskal/Prim) on a random graph  
- Add **DP** visualizers (coin change, knapsack, LCS)  
- Add **Big-O quiz mode**: guess complexity from the animation  
"""
)
