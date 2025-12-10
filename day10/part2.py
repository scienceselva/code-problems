import re
import pulp

def parse_line(line):

    paren_groups = re.findall(r'\((.*?)\)', line)
    target_raw = re.search(r'\{(.*?)\}', line)
    if not target_raw:
        raise ValueError("Target {} not found in line: " + line)
    target = list(map(int, target_raw.group(1).split(',')))
    
    buttons = []
    for g in paren_groups:
        g = g.strip()
        if g == "":
            buttons.append([])
        else:
            buttons.append(list(map(int, g.split(','))))

    return buttons, target


def solve_row_lp(buttons, target):
    num_buttons = len(buttons)
    num_counters = len(target)

    # Build effect matrix
    effect = []
    for b in buttons:
        vec = [0] * num_counters
        for idx in b:
            if idx < num_counters:
                vec[idx] += 1
        effect.append(vec)

    # LP model
    model = pulp.LpProblem("ButtonPress", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer")
         for i in range(num_buttons)]

    model += pulp.lpSum(x)

    # Add counter constraints
    for c in range(num_counters):
        model += pulp.lpSum(effect[b][c] * x[b] for b in range(num_buttons)) == target[c]

    model.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[model.status] != "Optimal":
        return None

    return sum(int(v.value()) for v in x)


def read_file(filename):
    total_sum = 0
    row_num = 1

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            buttons, target = parse_line(line)
            result = solve_row_lp(buttons, target)

            print(f"Row {row_num}: minimum presses = {result}")

            if result is not None:
                total_sum += result
            else:
                print(f"======> Row {row_num} has no valid solution <======")

            row_num += 1

    print("\nTotal presses for all rows =", total_sum)


if __name__ == "__main__":
    #read_file("test.txt")
    read_file("input.txt")