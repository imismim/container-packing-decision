import math


class Containers:
    def __init__(self, capacity=None):
        self.capacity = capacity if capacity else 100
        self.items = []
        self.containers = []
        
        self.algorithm_complexity_nfa = 0
        self.algorithm_complexity_ffa = 0
        self.algorithm_complexity_wfa = 0
        self.algorithm_complexity_bfa = 0

    def add_item(self, items):
        if not isinstance(items, list):
            raise ValueError("Items should be a list")
        elif  max(items) > self.capacity:
            raise ValueError("All items should be less than or equal to the container capacity")
        else:
            self.items.extend(items)

    def NFA(self, sort=False, reverse=True):
        n = len(self.items)
        sort_ops = int(n * math.ceil(math.log2(n))) if (sort and n > 1) else 0
        items = sorted(self.items, reverse=reverse) if sort else self.items

        containers = []
        container = []
        ops = 0

        for item in enumerate(items):
            ops += 1  # check: fits in current container?
            if sum(list(map(lambda x: x[1], container))) + item[1] <= self.capacity:
                container.append(item)
            else:
                containers.append(container)
                container = [item]
        containers.append(container)

        self.algorithm_complexity_nfa = sort_ops + ops
        return containers

    def FFA(self, sort=False, reverse=True):
        n = len(self.items)
        sort_ops = int(n * math.ceil(math.log2(n))) if (sort and n > 1) else 0
        items = sorted(self.items, reverse=reverse) if sort else self.items

        containers = []
        container = []
        ops = 0

        for item in enumerate(items):
            ops += 1  # check: fits in current container?
            if sum(list(map(lambda x: x[1], container))) + item[1] <= self.capacity:
                container.append(item)
            else:
                for cont in containers:
                    ops += 1  # check: fits in existing container?
                    if sum(list(map(lambda x: x[1], cont))) + item[1] <= self.capacity:
                        cont.append(item)
                        break
                else:
                    containers.append(container)
                    container = [item]
        containers.append(container)

        self.algorithm_complexity_ffa = sort_ops + ops
        return containers

    def WFA(self, sort=False, reverse=True):
        n = len(self.items)
        sort_ops = int(n * math.ceil(math.log2(n))) if (sort and n > 1) else 0
        items = sorted(self.items, reverse=reverse) if sort else self.items

        containers = []
        container = []
        ops = 0

        for item in enumerate(items):
            ops += 1  # check: fits in current container?
            if sum(list(map(lambda x: x[1], container))) + item[1] <= self.capacity:
                container.append(item)
            else:
                free_space = (None, 0)
                for indx_cont, cont in enumerate(containers):
                    ops += 1  # check: scan for worst fit
                    cont_free_space = (
                        indx_cont, self.capacity - sum(list(map(lambda x: x[1], cont))))
                    if cont_free_space[1] > free_space[1] and cont_free_space[1] >= item[1]:
                        free_space = cont_free_space

                if free_space[0]:
                    containers[free_space[0]].append(item)
                else:
                    containers.append(container)
                    container = [item]
        containers.append(container)

        self.algorithm_complexity_wfa = sort_ops + ops
        return containers

    def BFA(self, sort=False, reverse=True):
        n = len(self.items)
        sort_ops = int(n * math.ceil(math.log2(n))) if (sort and n > 1) else 0
        items = sorted(self.items, reverse=reverse) if sort else self.items

        containers = []
        container = []
        ops = 0

        for item in enumerate(items):
            ops += 1  # check: fits in current container?
            if sum(list(map(lambda x: x[1], container))) + item[1] <= self.capacity:
                container.append(item)
            else:
                free_space = (None, self.capacity)
                for indx_cont, cont in enumerate(containers):
                    ops += 1  # check: scan for best fit
                    cont_free_space = (
                        indx_cont, self.capacity - sum(list(map(lambda x: x[1], cont))))
                    if cont_free_space[1] < free_space[1] and cont_free_space[1] >= item[1]:
                        free_space = cont_free_space

                if free_space[0]:
                    containers[free_space[0]].append(item)
                else:
                    containers.append(container)
                    container = [item]
        containers.append(container)

        self.algorithm_complexity_bfa = sort_ops + ops
        return containers
    

def containers_to_table(containers):
    all_cols = [col_idx for row in containers for col_idx, _ in row]
    if not all_cols:
        return [], 0, 0
    num_cols = max(all_cols) + 1
    num_rows = len(containers)

    header = ['Контейнер'] + list(range(1, num_cols+1))
    table = [header]
    for i, container in enumerate(containers):
        col_map = {col_idx: val for col_idx, val in container}
        row = [f'{i + 1}'] + [col_map.get(j, 'x') for j in range(num_cols)]
        table.append(row)

    return table, num_rows, num_cols


def items_str_to_list(items: str, items_index: int):
    if not items:
        return False, f"Items {items_index} is empty"
    
    try:
        return True, list(map(lambda x: int(x), items.split(" ")))
    except:
        return False, f"You entered invalid data for items {items_index}"