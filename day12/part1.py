#!/usr/bin/env python3
import sys
import re
from collections import defaultdict, namedtuple

# ---------------- Parsing input file ------------------
def parse_input_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = [ln.rstrip('\n') for ln in f]

    # Remove pure-empty trailing lines
    lines = raw

    # We'll parse shapes first: shape headers look like "0:" "1:" etc.
    # Region lines look like "12x5: 1 0 1 0 2 2"
    shapes = {}
    i = 0
    # Collect shape blocks until we hit a region line
    shape_header_re = re.compile(r'^\s*(\d+)\s*:\s*$')
    region_line_re = re.compile(r'^\s*(\d+)\s*x\s*(\d+)\s*:\s*(.*)$')
    # Read shapes until a region line is encountered
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == '':
            i += 1
            continue
        # if it's a region line, break to region parsing
        if region_line_re.match(ln):
            break
        m = shape_header_re.match(ln)
        if m:
            idx = int(m.group(1))
            i += 1
            grid = []
            # gather subsequent diagram lines until next header or region line or empty
            while i < len(lines):
                if lines[i].strip() == '':
                    i += 1
                    break
                if shape_header_re.match(lines[i]) or region_line_re.match(lines[i]):
                    break
                grid.append(lines[i])
                i += 1
            # normalize grid rows to same width (no need but keep)
            shapes[idx] = [r.rstrip() for r in grid]
        else:
            # stray non-header before regions: skip (robust)
            i += 1

    # Now parse region lines from remaining lines
    regions = []
    while i < len(lines):
        ln = lines[i].strip()
        i += 1
        if not ln:
            continue
        m = region_line_re.match(ln)
        if not m:
            # ignore stray lines
            continue
        W = int(m.group(1))
        H = int(m.group(2))
        counts_str = m.group(3).strip()
        if counts_str == '':
            counts = []
        else:
            counts = [int(x) for x in counts_str.split()]
        regions.append((W, H, counts))

    if not shapes:
        raise ValueError("No shapes parsed from input.")
    # ensure shapes list is contiguous from 0..maxidx
    max_idx = max(shapes.keys())
    shape_list = []
    for idx in range(max_idx + 1):
        if idx not in shapes:
            raise ValueError(f"Missing shape index {idx}")
        shape_list.append(shapes[idx])

    return shape_list, regions

# ---------------- Shape utilities ----------------
def shape_to_cells(diagram):
    cells = set()
    h = len(diagram)
    w = max((len(r) for r in diagram), default=0)
    for y, row in enumerate(diagram):
        for x, ch in enumerate(row):
            if ch == '#':
                cells.add((x, y))
    return cells

def normalize_cells_tuple(cells):
    if not cells:
        return tuple()
    minx = min(x for x, y in cells)
    miny = min(y for x, y in cells)
    shifted = tuple(sorted(((x - minx, y - miny) for x, y in cells)))
    return shifted

def all_orientations(cells):
    
    variants = set()
    clist = list(cells)
    for flip in (False, True):
        for rot in range(4):
            new = []
            for x, y in clist:
                xx, yy = x, y
                if flip:
                    xx = -xx
                # rotate 'rot' times 90deg
                for _ in range(rot):
                    xx, yy = -yy, xx
                new.append((xx, yy))
            variants.add(normalize_cells_tuple(new))
    return variants

def placements_bitmasks_for_variant(variant_tuple, W, H):
    
    if not variant_tuple:
        return []
    maxx = max(x for x, y in variant_tuple)
    maxy = max(y for x, y in variant_tuple)
    placements = []
    for ox in range(0, W - maxx):
        for oy in range(0, H - maxy):
            mask = 0
            ok = True
            for x, y in variant_tuple:
                gx = ox + x
                gy = oy + y
                if not (0 <= gx < W and 0 <= gy < H):
                    ok = False
                    break
                pos = gy * W + gx
                mask |= (1 << pos)
            if ok:
                placements.append(mask)
    return placements

def generate_unique_placements(shape_diag, W, H):
    cells = shape_to_cells(shape_diag)
    variants = all_orientations(cells)
    placements = set()
    for var in variants:
        for mask in placements_bitmasks_for_variant(var, W, H):
            placements.add(mask)
    return sorted(placements)

# ---------------- Backtracking solver ----------------
# represent a shape requirement as a small object
ShapeReq = namedtuple('ShapeReq', ['idx', 'area', 'placements', 'count'])

def can_fit_region_backtrack(W, H, shapes_diags, counts, want_layout=False):
    S = len(shapes_diags)
    # normalize counts length
    if len(counts) < S:
        counts = counts + [0] * (S - len(counts))
    else:
        counts = counts[:S]

    # compute area per shape and total
    shape_areas = [len(shape_to_cells(diag)) for diag in shapes_diags]
    total_need_area = sum(a * c for a, c in zip(shape_areas, counts))
    if total_need_area > W * H:
        return False, None

    # generate placements bitmasks for each shape
    placements_per_shape = []
    for s in range(S):
        if counts[s] == 0:
            placements_per_shape.append([])
        else:
            pl = generate_unique_placements(shapes_diags[s], W, H)
            placements_per_shape.append(pl)
            if not pl and counts[s] > 0:
                # required but no placement possible
                return False, None

    # Construct a list of ShapeReq for shapes that have count>0
    shape_reqs = []
    for s in range(S):
        if counts[s] > 0:
            shape_reqs.append(ShapeReq(idx=s, area=shape_areas[s],
                                       placements=placements_per_shape[s],
                                       count=counts[s]))

    # order shape_reqs by heuristic: fewest placements per instance first, then larger area
    # compute metric: len(placements) (lower is harder); break ties by larger area
    def metric(req):
        # if placements list is empty, return huge
        plen = len(req.placements)
        # effective placements-per-piece (approx)
        eff = plen / req.count if req.count else float('inf')
        return (eff, -req.area)
    shape_reqs.sort(key=metric)

    # Precompute remaining area suffix for pruning: total area of remaining shapes
    rem_areas = [0] * (len(shape_reqs) + 1)
    for i in range(len(shape_reqs) - 1, -1, -1):
        rem_areas[i] = rem_areas[i + 1] + shape_reqs[i].area * shape_reqs[i].count

    # also precompute for speed the placements arrays
    placements_lists = [req.placements for req in shape_reqs]
    counts_list = [req.count for req in shape_reqs]
    areas_list = [req.area for req in shape_reqs]
    shape_indices = [req.idx for req in shape_reqs]

    # For building layout when found: we'll record (shape_idx, placement_mask, label_char)
    solution_assignment = []

    # Heavily prune: if some shape has fewer placements than required count choose -> impossible
    for req in shape_reqs:
        if len(req.placements) < req.count:
            return False, None

    # Helper recursive functions:
    sys.setrecursionlimit(10000)
    found_solution = False
    found_assignment = None


    # choose placements with strictly increasing placement indices (combinational selection).
    def place_shape_pieces(shape_idx_in_list, occ_mask):
        nonlocal found_solution, found_assignment
        if found_solution:
            return True  # early stop

        if shape_idx_in_list >= len(shape_reqs):
            # all shapes placed
            found_solution = True
            found_assignment = list(solution_assignment)
            return True

        # pruning by remaining area
        free_cells = W * H - occ_mask.bit_count()
        if free_cells < rem_areas[shape_idx_in_list]:
            return False

        placements = placements_lists[shape_idx_in_list]
        needed = counts_list[shape_idx_in_list]
        area = areas_list[shape_idx_in_list]
        shape_global_idx = shape_indices[shape_idx_in_list]

        # Implement iterative recursive helper for placement of k pieces of the current shape
        def place_k(pick_start_idx, placed_count, occ_mask_local, chosen_indices):
            nonlocal found_solution, found_assignment
            if found_solution:
                return True
            if placed_count == needed:
                # move to next shape
                # record chosen placements as assignments
                for pi in chosen_indices:
                    mask = placements[pi]
                    solution_assignment.append((shape_global_idx, mask))
                ok = place_shape_pieces(shape_idx_in_list + 1, occ_mask_local)
                if ok:
                    return True
                # backtrack remove added records
                for _ in range(len(chosen_indices)):
                    solution_assignment.pop()
                return False
            # Remaining pieces to place for this shape
            remaining_to_place = needed - placed_count
            # prune: if not enough placements left to choose (combinatorial)
            max_start = len(placements) - remaining_to_place
            if pick_start_idx > max_start:
                return False

            # Iteratively try placements in given order.
            for pi in range(pick_start_idx, len(placements)):
                pmask = placements[pi]
                if pmask & occ_mask_local:
                    continue
                # quick area-based prune: if after placing this piece there won't be enough free cells for remainder -> skip
                new_occ = occ_mask_local | pmask
                free_after = W * H - new_occ.bit_count()
                if free_after < (remaining_to_place - 1) * area:
                    continue
                # choose it
                chosen_indices.append(pi)
                if place_k(pi + 1, placed_count + 1, new_occ, chosen_indices):
                    return True
                chosen_indices.pop()
                if found_solution:
                    return True
            return False

        # start placing pieces for this shape
        return place_k(0, 0, occ_mask, [])

    # Start recursion
    initial_occ = 0
    ok = place_shape_pieces(0, initial_occ)
    if not ok:
        return False, None

    # Build layout grid if requested
    if want_layout and found_assignment is not None:
        # create grid with '.' initially
        grid = [['.' for _ in range(W)] for __ in range(H)]
        # assign letters to each placed piece; use A,B,C... then a..z then digits if needed
        labels = []
        for n in range(len(found_assignment)):
            if n < 26:
                labels.append(chr(ord('A') + n))
            elif n < 52:
                labels.append(chr(ord('a') + (n - 26)))
            else:
                labels.append(str(n - 52))
        for i, (shape_idx, pmask) in enumerate(found_assignment):
            lbl = labels[i]
            # paint bits
            bit = 0
            for pos in range(W * H):
                if (pmask >> pos) & 1:
                    y = pos // W
                    x = pos % W
                    grid[y][x] = lbl
        ascii_lines = [''.join(row) for row in grid]
        return True, ascii_lines

    return True, None

# ---------------- Main ----------------
def main():
    if len(sys.argv) < 2:
        print("missing input file")
        return
    path = sys.argv[1]
    shapes_diags, regions = parse_input_file(path)
    total_regions = len(regions)

    success_count = 0
    results = []
    for ri, (W, H, counts) in enumerate(regions, start=1):
        print(f"Region {ri}: {W}x{H} counts={counts} ...", end=' ', flush=True)
        ok, layout = can_fit_region_backtrack(W, H, shapes_diags, counts, want_layout=True)
        if ok:
            print("OK")
            success_count += 1
            print("Layout packing:")
            for line in layout:
                print(line)
        else:
            print("NO")
        results.append((ri, ok))

    print(f"\nTotal regions that can fit all presents: {success_count} / {total_regions}")

if __name__ == "__main__":
    main()
