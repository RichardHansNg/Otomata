from collections import deque, namedtuple

T = {"4", "+", "*"}

grammar = {
    "S": [["S", "+", "S"], ["S", "*", "S"], ["4"]]
}

Configuration = namedtuple('Configuration', ['position', 'stack', 'parent'])

def simulate_pda(input_str):
    if len(input_str) < 4 or not all(char in T for char in input_str):
        print("Invalid input.")
        return

    initial_stack = ["S"]
    initial_conf = Configuration(0, initial_stack, None)
    queue = deque([initial_conf])
    visited = set([(0, tuple(initial_stack))])
    accepting_conf = None

    while queue and accepting_conf is None:
        conf = queue.popleft()
        if conf.position == len(input_str) and len(conf.stack) == 0:
            accepting_conf = conf
            break
        if len(conf.stack) > 0:
            top = conf.stack[-1]
            if top == "S":
                for prod in grammar["S"]:
                    new_stack = conf.stack[:-1] + list(reversed(prod))
                    key = (conf.position, tuple(new_stack))
                    if key not in visited:
                        visited.add(key)
                        new_conf = Configuration(conf.position, new_stack, conf)
                        queue.append(new_conf)
            elif top in T and conf.position < len(input_str) and top == input_str[conf.position]:
                new_stack = conf.stack[:-1]
                key = (conf.position + 1, tuple(new_stack))
                if key not in visited:
                    visited.add(key)
                    new_conf = Configuration(conf.position + 1, new_stack, conf)
                    queue.append(new_conf)

    if accepting_conf:
        path = []
        conf = accepting_conf
        while conf is not None:
            path.append(conf)
            conf = conf.parent
        path.reverse()
        print("Procedure:")
        print(f"{'Step':<4} | {'State':<10} | {'Stack':<20} | {'Tape':<20}")
        for i, conf in enumerate(path):
            state = "initial" if i == 0 else "accepted" if i == len(path) - 1 else "processing"
            stack_str = " ".join(conf.stack) if conf.stack else ""
            tape_str = input_str[conf.position:] if conf.position < len(input_str) else ""
            print(f"{i:<4} | {state:<10} | {stack_str:<20} | {tape_str:<20}")
    else:
        print("Rejected.")

input_str = input("String: ")
simulate_pda(input_str)
