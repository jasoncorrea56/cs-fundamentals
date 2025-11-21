# API - Surface & Example Calls

This document describes the **public API surface** of the cs-fundamentals service as currently exposed in the README.

Additional endpoints exist beyond what’s documented here. These examples focus on health, config, versioning, and practice exploration.

Base URL examples:

- Local (uvicorn / Docker): `http://127.0.0.1:8080`
- Local k8s (port‑forward/NodePort/Ingress): varies per setup
- Prod EKS: `https://csf.jasoncorrea.dev` (behind ALB + TLS)

---

## Design Notes

- The API is built with **FastAPI**, so:
  - Automatic OpenAPI spec and interactive docs (Swagger/Redoc) are available when enabled.
  - Pydantic models enforce input/output validation.
- Endpoints follow a versioned path prefix (`/api/v1/...`) to allow future versions.

For information on how to run the service so you can hit these endpoints, see [RUNBOOK.md](RUNBOOK.md). For operational checks around these endpoints in k8s/EKS, see [OPERATIONS.md](OPERATIONS.md).

---

## 1. Health & Diagnostics

### 1.1 Health Check

**Endpoint**

```text
GET /api/v1/healthz
```

**Purpose**

- Liveness/readiness indicator.
- Used by k8s probes, load balancers, and runbooks.

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/healthz | jq
```

### 1.2 Config Snapshot

**Endpoint**

```text
GET /api/v1/configz
```

**Purpose**

- Returns a sanitized view of effective configuration.
- Useful for debugging environment issues (env vars, feature flags, etc.).

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/configz | jq
```

### 1.3 Version

**Endpoint**

```text
GET /api/v1/version
```

**Purpose**

- Shows build/version info:
  - App version
  - Git SHA (if wired)
  - Build date/time
- Used in runbooks to ensure the correct version is deployed.

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/version | jq
```

---

## 2. Practice Endpoints

### 2.1 List Practice Targets

**Endpoint**

```text
GET /api/v1/targets
```

**Purpose**

- Lists available practice targets (data structures, problems, or exercises).
- Helps UIs/clients discover what can be requested or evaluated.

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/targets | jq
```

### 2.2 Submit Practice via Matrix

**Endpoint**

```text
POST /api/v1/practice-matrix/submit
```

**Purpose**

- Submit practice implementations using a **matrix-style** payload.
- Uses a logical key (e.g. `patterns.dfs`) plus a `methods` dictionary.
- Lets you bundle multiple method implementations under a single practice key.

**Request Body (shape)**

```jsonc
{
  "key": "patterns.dfs",
  "methods": {
    "<method_name>": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/practice-matrix/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "key": "patterns.dfs",
  "methods": {
    "preorder_dfs": "def preorder_dfs(node,out):\n    if not node: return\n    out.append(node.value)\n    preorder_dfs(node.left,out)\n    preorder_dfs(node.right,out)"
  }
}
JSON
```

### 2.3 Submit Practice with Module, Class and Tests

**Endpoint**

```text
POST /api/v1/practice/submit
```

**Purpose**

- Submit practice code for a specific **module + class** combination.
- Provide one or more method implementations plus explicit test files to run.
- Supports a test expression (`test_expr`) to select which tests execute.

**Request Body (shape)**

```jsonc
{
  "module": "cs_fundamentals.patterns.breadth_first_search",
  "class_name": "PracticeBreadthFirstSearch",
  "methods": {
    "<method_name>": "<python_source_code>"
  },
  "test_files": [
    "path/to/test_file.py",
    "path/to/other_test_file.py"
  ],
  "test_expr": "pytest expression to filter tests"
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/practice/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "module": "cs_fundamentals.patterns.breadth_first_search",
  "class_name": "PracticeBreadthFirstSearch",
  "methods": {
    "level_order_bfs": "def level_order_bfs(root):\n    if not root: return []\n    from collections import deque\n    q, res = deque([root]), []\n    while q:\n        node = q.popleft()\n        res.append(node.value)\n        if node.left: q.append(node.left)\n        if node.right: q.append(node.right)\n    return res"
  },
  "test_files": [
    "automation/test_patterns/test_breadth_first_search.py",
    "automation/test_patterns/test_practice/test_practice_breadth_first_search.py"
  ],
  "test_expr": "breadth_first_search or PracticeBreadthFirstSearch"
}
JSON
```

---

## 3. Data Structure Practice – Trees & Graphs

### 3.1 Binary Search Tree – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/bst/submit
```

**Purpose**

- Submit practice implementation(s) for **Binary Search Tree** operations.
- This example focuses on validating a BST (`is_valid_bst`).

**Request Body (shape)**

```jsonc
{
  "methods": {
    "is_valid_bst": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/bst/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "is_valid_bst": "def is_valid_bst(root):\n    import math\n    if not root: return True\n    stack=[(root,-math.inf,math.inf)]\n    while stack:\n        node,lo,hi=stack.pop()\n        if not node: continue\n        if not (lo < node.value < hi): return False\n        stack.append((node.right,node.value,hi))\n        stack.append((node.left,lo,node.value))\n    return True"
      }
}
JSON
```

---

### 3.2 Graph – Number of Islands II (Union-Find)

**Endpoint**

```text
POST /api/v1/data-structures/graph/islands/submit
```

**Purpose**

- Submit practice code for solving **Number of Islands II** using **Union-Find**.
- Implements both the Union-Find helper class and the primary `number_of_islands_2` method.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "UnionFind.__init__": "<python_source_code>",
    "UnionFind.find": "<python_source_code>",
    "UnionFind.union": "<python_source_code>",
    "UnionFind.is_valid": "<python_source_code>",
    "UnionFind.set_parent": "<python_source_code>",
    "number_of_islands_2": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/graph/islands/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "UnionFind.__init__": "def __init__(self, size):\n    self.root = [-1] * size\n    self.rank = [0] * size\n    self.count = 0",
    "UnionFind.find": "def find(self, node):\n    if node != self.root[node]:\n        self.root[node] = self.find(self.root[node])\n    return self.root[node]",
    "UnionFind.union": "def union(self, node_x, node_y):\n    rx, ry = self.find(node_x), self.find(node_y)\n    if rx != ry:\n        if self.rank[rx] > self.rank[ry]:\n            self.root[ry] = rx\n        elif self.rank[rx] < self.rank[ry]:\n            self.root[rx] = ry\n        else:\n            self.root[ry] = rx\n            self.rank[rx] += 1\n        self.count -= 1\n    return None",
    "UnionFind.is_valid": "def is_valid(self, node):\n    return self.root[node] >= 0",
    "UnionFind.set_parent": "def set_parent(self, node):\n    self.root[node] = node\n    self.count += 1\n    return None",
    "number_of_islands_2": "def number_of_islands_2(self, m, n, positions):\n    res = []\n    uf = self.UnionFind(m * n)\n    for r, c in positions:\n        idx = r * n + c\n        if not uf.is_valid(idx):\n            uf.set_parent(idx)\n            for nr, nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):\n                if 0 <= nr < m and 0 <= nc < n:\n                    nidx = nr * n + nc\n                    if uf.is_valid(nidx):\n                        uf.union(idx, nidx)\n        res.append(uf.count)\n    return res"
  }
}
JSON
```

### 3.3 Graph – Union-Find Core Structure

**Endpoint**

```text
POST /api/v1/data-structures/graph/union-find/submit
```

**Purpose**

- Submit a general-purpose **Union-Find / Disjoint Set** implementation.
- Covers initialization, `find`, `union`, and `is_connected` operations.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "find": "<python_source_code>",
    "union": "<python_source_code>",
    "is_connected": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/graph/union-find/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self, size):\n    self.root = list(range(size))\n    self.rank = [1] * size",
    "find": "def find(self, x):\n    if x != self.root[x]:\n        self.root[x] = self.find(self.root[x])\n    return self.root[x]",
    "union": "def union(self, x, y):\n    rx, ry = self.find(x), self.find(y)\n    if rx == ry:\n        return True\n    if self.rank[rx] > self.rank[ry]:\n        self.root[ry] = rx\n    elif self.rank[rx] < self.rank[ry]:\n        self.root[rx] = ry\n    else:\n        self.root[ry] = rx\n        self.rank[rx] += 1\n    return True",
    "is_connected": "def is_connected(self, x, y):\n    return self.find(x) == self.find(y)"
  }
}
JSON
```

---

## 4. Data Structure Practice – Linked Lists

### 4.1 Doubly Linked List – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/linked-list-double/submit
```

**Purpose**

- Submit practice implementations for a **doubly linked list**.
- Implements node lookup, tail access, getters, and index-based mutations.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "get_node": "<python_source_code>",
    "get_tail": "<python_source_code>",
    "get": "<python_source_code>",
    "get_list": "<python_source_code>",
    "add_at_head": "<python_source_code>",
    "add_at_tail": "<python_source_code>",
    "add_at_index": "<python_source_code>",
    "delete_at_index": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/linked-list-double/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self) -> None:\n    self.head = None",
    "get_node": "def get_node(self, index: int):\n    curr = self.head\n    i = 0\n    while curr and i < index:\n        curr = curr.next\n        i += 1\n    return curr",
    "get_tail": "def get_tail(self):\n    curr = self.head\n    while curr and curr.next:\n        curr = curr.next\n    return curr",
    "get": "def get(self, index: int) -> int:\n    node = self.get_node(index)\n    return node.value if node else -1",
    "get_list": "def get_list(self) -> list:\n    result = []\n    node = self.head\n    while node and node.value not in result:\n        result.append(node.value)\n        node = node.next\n    return result",
    "add_at_head": "def add_at_head(self, val: int) -> None:\n    new_node = Node(val, next_node=self.head, prev_node=None)\n    if self.head:\n        self.head.prev = new_node\n    self.head = new_node",
    "add_at_tail": "def add_at_tail(self, val: int) -> None:\n    if not self.head:\n        self.add_at_head(val)\n        return\n    tail = self.get_tail()\n    new_node = Node(val, next_node=None, prev_node=tail)\n    tail.next = new_node",
    "add_at_index": "def add_at_index(self, index: int, val: int) -> None:\n    if index == 0:\n        self.add_at_head(val)\n        return\n    prev = self.get_node(index - 1)\n    if not prev:\n        return\n    nxt = prev.next\n    new_node = Node(val, next_node=nxt, prev_node=prev)\n    prev.next = new_node\n    if nxt:\n        nxt.prev = new_node",
    "delete_at_index": "def delete_at_index(self, index: int) -> None:\n    node = self.get_node(index)\n    if not node:\n        return\n    prev, nxt = node.prev, node.next\n    if prev:\n        prev.next = nxt\n    else:\n        self.head = nxt\n    if nxt:\n        nxt.prev = prev"
  }
}
JSON
```

### 4.2 Singly Linked List – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/linked-list-single/submit
```

**Purpose**

- Submit practice implementations for a **singly linked list**.
- Implements operations for node access, insertion, deletion, and list representation.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "get_node": "<python_source_code>",
    "get_tail": "<python_source_code>",
    "get": "<python_source_code>",
    "get_list": "<python_source_code>",
    "add_at_head": "<python_source_code>",
    "add_at_tail": "<python_source_code>",
    "add_at_index": "<python_source_code>",
    "delete_at_index": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/linked-list-single/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self) -> None:\n    self.head = None",
    "get_node": "def get_node(self, index: int):\n    curr = self.head\n    i = 0\n    while curr and i < index:\n        curr = curr.next\n        i += 1\n    return curr",
    "get_tail": "def get_tail(self):\n    curr = self.head\n    while curr and curr.next:\n        curr = curr.next\n    return curr",
    "get": "def get(self, index: int) -> int:\n    node = self.get_node(index)\n    return node.value if node else -1",
    "get_list": "def get_list(self) -> list[int]:\n    vals = []\n    curr = self.head\n    # mirror reference impl behavior (stop if value repeats)\n    seen = set()\n    while curr and (curr.value not in seen):\n        vals.append(curr.value)\n        seen.add(curr.value)\n        curr = curr.next\n    return vals",
    "add_at_head": "def add_at_head(self, val: int) -> None:\n    new_node = Node(val)\n    new_node.next = self.head\n    self.head = new_node",
    "add_at_tail": "def add_at_tail(self, val: int) -> None:\n    if not self.head:\n        self.add_at_head(val)\n        return\n    tail = self.get_tail()\n    tail.next = Node(val)",
    "add_at_index": "def add_at_index(self, index: int, val: int) -> None:\n    if index == 0:\n        self.add_at_head(val)\n        return\n    prev = self.get_node(index - 1)\n    if not prev:\n        return\n    new_node = Node(val)\n    new_node.next = prev.next\n    prev.next = new_node",
    "delete_at_index": "def delete_at_index(self, index: int) -> None:\n    node = self.get_node(index)\n    if not node:\n        return\n    if index == 0:\n        self.head = node.next\n        return\n    prev = self.get_node(index - 1)\n    if prev:\n        prev.next = node.next"
  }
}
JSON
```

---

## 5. Data Structure Practice – Heaps

### 5.1 Max Heap – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/max-heap/submit
```

**Purpose**

- Submit practice implementation of a **max heap**.
- Implements heap initialization, `add`, and `pop` operations.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "add": "<python_source_code>",
    "pop": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/max-heap/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self, heap_size: int) -> None:\n    self.real_size = 0\n    self.heap_size = heap_size\n    self.max_heap = [0] * (heap_size + 1)",
    "add": "def add(self, element: int) -> bool:\n    self.real_size += 1\n    if self.real_size > self.heap_size:\n        self.real_size -= 1\n        return False\n    self.max_heap[self.real_size] = element\n    i = self.real_size\n    while i > 1 and self.max_heap[i] > self.max_heap[i//2]:\n        self.max_heap[i], self.max_heap[i//2] = self.max_heap[i//2], self.max_heap[i]\n        i //= 2\n    return True",
    "pop": "def pop(self) -> int:\n    import sys\n    if self.real_size < 1:\n        return -sys.maxsize\n    root = self.max_heap[1]\n    self.max_heap[1] = self.max_heap[self.real_size]\n    self.real_size -= 1\n    i = 1\n    while i * 2 <= self.real_size:\n        left, right = i * 2, i * 2 + 1\n        largest = left\n        if right <= self.real_size and self.max_heap[right] > self.max_heap[left]:\n            largest = right\n        if self.max_heap[i] < self.max_heap[largest]:\n            self.max_heap[i], self.max_heap[largest] = self.max_heap[largest], self.max_heap[i]\n            i = largest\n        else:\n            break\n    return root"
  }
}
JSON
```

### 5.2 Min Heap – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/min-heap/submit
```

**Purpose**

- Submit practice implementation of a **min heap**.
- Implements heap initialization, `add`, and `pop` operations.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "add": "<python_source_code>",
    "pop": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/min-heap/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self, heap_size: int) -> None:\n    self.real_size = 0\n    self.heap_size = heap_size\n    self.min_heap = [0] * (heap_size + 1)",
    "add": "def add(self, element: int) -> bool:\n    self.real_size += 1\n    if self.real_size > self.heap_size:\n        self.real_size -= 1\n        return False\n    self.min_heap[self.real_size] = element\n    i = self.real_size\n    while i > 1 and self.min_heap[i] < self.min_heap[i//2]:\n        self.min_heap[i], self.min_heap[i//2] = self.min_heap[i//2], self.min_heap[i]\n        i //= 2\n    return True",
    "pop": "def pop(self) -> int:\n    import sys\n    if self.real_size < 1:\n        return sys.maxsize\n    root = self.min_heap[1]\n    self.min_heap[1] = self.min_heap[self.real_size]\n    self.real_size -= 1\n    i = 1\n    while i * 2 <= self.real_size:\n        left, right = i * 2, i * 2 + 1\n        smallest = left\n        if right <= self.real_size and self.min_heap[right] < self.min_heap[left]:\n            smallest = right\n        if self.min_heap[i] > self.min_heap[smallest]:\n            self.min_heap[i], self.min_heap[smallest] = self.min_heap[smallest], self.min_heap[i]\n            i = smallest\n        else:\n            break\n    return root"
  }
}
JSON
```

---

## 6. Data Structure Practice – Queues

### 6.1 Queue (Array-backed) – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/queue/array/submit
```

**Purpose**

- Submit practice implementation for an **array-backed queue**.
- Demonstrates capacity management, circular indexing, and basic queue operations.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "__str__": "<python_source_code>",
    "is_full": "<python_source_code>",
    "is_empty": "<python_source_code>",
    "enqueue": "<python_source_code>",
    "dequeue": "<python_source_code>",
    "peek": "<python_source_code>",
    "rear": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/queue/array/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self, capacity: int) -> None:\n    from threading import Lock\n    self.queue = [0] * capacity\n    self.capacity = capacity\n    self.size = 0\n    self.head = 0\n    self.queue_lock = Lock()",
    "__str__": "def __str__(self) -> str:\n    return str(list(self.queue))",
    "is_full": "def is_full(self) -> bool:\n    return self.size == self.capacity",
    "is_empty": "def is_empty(self) -> bool:\n    return self.size == 0",
    "enqueue": "def enqueue(self, value: int) -> bool:\n    with self.queue_lock:\n        if self.is_full():\n            return False\n        self.queue[(self.head + self.size) % self.capacity] = value\n        self.size += 1\n    return True",
    "dequeue": "def dequeue(self) -> int | None:\n    if self.is_empty():\n        return None\n    value = self.peek()\n    self.queue[self.head] = None\n    self.head = (self.head + 1) % self.capacity\n    self.size -= 1\n    return value",
    "peek": "def peek(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.queue[self.head]",
    "rear": "def rear(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.queue[(self.head + self.size - 1) % self.capacity]"
  }
}
JSON
```

### 6.2 Queue (Linked-list-backed) – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/queue/linked-list/submit
```

**Purpose**

- Submit practice implementation for a **linked-list-backed queue**.
- Shows head/tail management and linked-node handling via plain dicts.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "__str__": "<python_source_code>",
    "is_full": "<python_source_code>",
    "is_empty": "<python_source_code>",
    "enqueue": "<python_source_code>",
    "dequeue": "<python_source_code>",
    "peek": "<python_source_code>",
    "rear": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/queue/linked-list/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self, capacity: int) -> None:\n    self.size = 0\n    self.capacity = capacity\n    self.head = None  # node is a dict: {'value': int, 'next': node|None}\n    self.tail = None",
    "__str__": "def __str__(self) -> str:\n    vals = []\n    node = self.head\n    while node is not None:\n        vals.append(node['value'])\n        node = node['next']\n    return str(vals)",
    "is_full": "def is_full(self) -> bool:\n    return self.size == self.capacity",
    "is_empty": "def is_empty(self) -> bool:\n    return self.size == 0",
    "enqueue": "def enqueue(self, value: int) -> bool:\n    if self.is_full():\n        return False\n    node = {'value': value, 'next': None}\n    if self.is_empty():\n        self.head = node\n        self.tail = node\n    else:\n        self.tail['next'] = node\n        self.tail = node\n    self.size += 1\n    return True",
    "dequeue": "def dequeue(self) -> int | None:\n    if self.is_empty():\n        return None\n    value = self.head['value']\n    self.head = self.head['next']\n    self.size -= 1\n    if self.size == 0:\n        self.tail = None\n    return value",
    "peek": "def peek(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.head['value']",
    "rear": "def rear(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.tail['value']"
  }
}
JSON
```

---

## 7. Data Structure Practice – Stacks

### 7.1 Stack (Array-backed) – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/stack/array/submit
```

**Purpose**

- Submit practice implementation for an **array-based stack**.
- Covers push/pop/peek and emptiness checks using a Python list.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "__str__": "<python_source_code>",
    "is_empty": "<python_source_code>",
    "push": "<python_source_code>",
    "pop": "<python_source_code>",
    "peek": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/stack/array/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self) -> None:\n    self.stack = []",
    "__str__": "def __str__(self) -> str:\n    result = list(self.stack)\n    result.reverse()\n    return str(result)",
    "is_empty": "def is_empty(self) -> bool:\n    return len(self.stack) == 0",
    "push": "def push(self, item) -> bool:\n    try:\n        self.stack.append(item)\n    except Exception:\n        return False\n    return True",
    "pop": "def pop(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.stack.pop()",
    "peek": "def peek(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.stack[-1]"
  }
}
JSON
```

### 7.2 Stack (Linked-list-backed) – Submit Practice

**Endpoint**

```text
POST /api/v1/data-structures/stack/linked-list/submit
```

**Purpose**

- Submit practice implementation for a **linked-list-based stack**.
- Uses dict-based nodes and stores top-of-stack in `self.top`.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "__init__": "<python_source_code>",
    "__str__": "<python_source_code>",
    "is_empty": "<python_source_code>",
    "push": "<python_source_code>",
    "pop": "<python_source_code>",
    "peek": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/data-structures/stack/linked-list/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "__init__": "def __init__(self) -> None:\n    self.top = None  # node is {'value': int, 'next': node|None}",
    "__str__": "def __str__(self) -> str:\n    vals = []\n    node = self.top\n    while node is not None:\n        vals.append(node['value'])\n        node = node['next']\n    return str(vals)",
    "is_empty": "def is_empty(self) -> bool:\n    return self.top is None",
    "push": "def push(self, data) -> bool:\n    node = {'value': data, 'next': self.top}\n    self.top = node\n    return True",
    "pop": "def pop(self) -> int | None:\n    if self.is_empty():\n        return None\n    val = self.top['value']\n    self.top = self.top['next']\n    return val",
    "peek": "def peek(self) -> int | None:\n    if self.is_empty():\n        return None\n    return self.top['value']"
  }
}
JSON
```

---

## 8. Pattern Practice – BFS & DFS

### 8.1 Breadth-First Search (BFS) – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/bfs/submit
```

**Purpose**

- Submit practice implementation of **level-order BFS traversal** on a tree.
- Returns a list of node values level-by-level.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "level_order_bfs": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/bfs/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "level_order_bfs": "def level_order_bfs(root):\n    if not root: return []\n    from collections import deque\n    q, res = deque([root]), []\n    while q:\n        node = q.popleft()\n        res.append(node.value)\n        if node.left: q.append(node.left)\n        if node.right: q.append(node.right)\n    return res"
  }
}
JSON
```

### 8.2 Depth-First Search (DFS) – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/dfs/submit
```

**Purpose**

- Submit practice implementations for **DFS traversals** and a **level-average** helper.
- Includes preorder, inorder, postorder traversals and a function computing average per level.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "preorder_dfs": "<python_source_code>",
    "inorder_dfs": "<python_source_code>",
    "postorder_dfs": "<python_source_code>",
    "get_avg_for_each_level": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/dfs/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "preorder_dfs": "def preorder_dfs(node, out):\n    if not node: return\n    out.append(node.value)\n    preorder_dfs(node.left, out)\n    preorder_dfs(node.right, out)\n    return",
    "inorder_dfs": "def inorder_dfs(node, out):\n    if not node: return\n    inorder_dfs(node.left, out)\n    out.append(node.value)\n    inorder_dfs(node.right, out)\n    return",
    "postorder_dfs": "def postorder_dfs(node, out):\n    if not node: return\n    postorder_dfs(node.left, out)\n    postorder_dfs(node.right, out)\n    out.append(node.value)\n    return",
    "get_avg_for_each_level": "def get_avg_for_each_level(root):\n    if not root: return []\n    data = {}\n    def walk(node, level=0):\n        if not node: return\n        s, c = data.get(level, (0, 0))\n        data[level] = (s + node.value, c + 1)\n        walk(node.left, level + 1)\n        walk(node.right, level + 1)\n    walk(root)\n    i, out = 0, []\n    while i in data:\n        s, c = data[i]\n        out.append(s / c)\n        i += 1\n    return out"
  }
}
JSON
```

---

## 9. Pattern Practice – Fast/Slow Pointers

### 9.1 Fast/Slow Pointers – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/fast-slow-pointers/submit
```

**Purpose**

- Submit practice implementations for **cycle detection** and **cycle entry** in linked lists.
- Demonstrates classic Floyd’s Tortoise and Hare patterns.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "has_cycle_in_linked_list": "<python_source_code>",
    "get_first_node_for_cycle_in_linked_list": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/fast-slow-pointers/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "has_cycle_in_linked_list": "def has_cycle_in_linked_list(head):\n    if not head: return False\n    slow, fast = head, head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False",
    "get_first_node_for_cycle_in_linked_list": "def get_first_node_for_cycle_in_linked_list(head):\n    if not head: return None\n    slow, fast = head, head\n    # phase 1: find meeting point\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            break\n    else:\n        return None\n    # phase 2: move one pointer to head; advance both one step\n    p1, p2 = head, slow\n    while p1 is not p2:\n        p1 = p1.next\n        p2 = p2.next\n    return p1"
  }
}
JSON
```

---

## 10. Pattern Practice – Sliding Window

### 10.1 Sliding Window – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/sliding-window/submit
```

**Purpose**

- Submit a suite of **sliding window** problems (fixed and variable size).
- Includes average, longest substring, fruit baskets, and other window-based patterns.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "avg_subarray_of_size_k": "<python_source_code>",
    "longest_substring_with_k_distinct_chars": "<python_source_code>",
    "longest_substring_with_distinct_chars": "<python_source_code>",
    "fruits_into_baskets": "<python_source_code>",
    "max_subarray_of_size_k": "<python_source_code>",
    "smallest_subarray_sum_greater_than_s": "<python_source_code>",
    "longest_subarray_with_ones_after_replacement": "<python_source_code>",
    "longest_substring_with_same_letters_after_replacement": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/sliding-window/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "avg_subarray_of_size_k": "def avg_subarray_of_size_k(nums, k):\n    res = []\n    window_sum = 0\n    for end, val in enumerate(nums):\n        window_sum += val\n        if end >= k - 1:\n            res.append(window_sum / k)\n            window_sum -= nums[end - k + 1]\n    return res",
    "longest_substring_with_k_distinct_chars": "def longest_substring_with_k_distinct_chars(s, k):\n    start = 0\n    best = 0\n    freq = {}\n    for end, ch in enumerate(s):\n        freq[ch] = freq.get(ch, 0) + 1\n        while len(freq) > k:\n            left = s[start]\n            freq[left] -= 1\n            if freq[left] == 0:\n                del freq[left]\n            start += 1\n        best = max(best, end - start + 1)\n    return best",
    "longest_substring_with_distinct_chars": "def longest_substring_with_distinct_chars(s):\n    start = 0\n    best = 0\n    last = {}\n    for end, ch in enumerate(s):\n        if ch in last:\n            start = max(start, last[ch] + 1)\n        last[ch] = end\n        best = max(best, end - start + 1)\n    return best",
    "fruits_into_baskets": "def fruits_into_baskets(fruit):\n    start = 0\n    best = 0\n    freq = {}\n    for end, ch in enumerate(fruit):\n        freq[ch] = freq.get(ch, 0) + 1\n        while len(freq) > 2:\n            left = fruit[start]\n            freq[left] -= 1\n            if freq[left] == 0:\n                del freq[left]\n            start += 1\n        best = max(best, end - start + 1)\n    return best",
    "max_subarray_of_size_k": "def max_subarray_of_size_k(nums, k):\n    max_sum = 0\n    window = 0\n    for end, val in enumerate(nums):\n        window += val\n        if end >= k - 1:\n            if window > max_sum:\n                max_sum = window\n            window -= nums[end - k + 1]\n    return max_sum",
    "smallest_subarray_sum_greater_than_s": "def smallest_subarray_sum_greater_than_s(nums, s):\n    import math\n    start = 0\n    window = 0\n    best = math.inf\n    for end, val in enumerate(nums):\n        window += val\n        while window >= s:\n            best = min(best, end - start + 1)\n            window -= nums[start]\n            start += 1\n    return 0 if best is math.inf else best",
    "longest_subarray_with_ones_after_replacement": "def longest_subarray_with_ones_after_replacement(nums, k):\n    start = 0\n    ones = 0\n    best = 0\n    for end, val in enumerate(nums):\n        if val == 1:\n            ones += 1\n        while (end - start + 1) - ones > k:\n            if nums[start] == 1:\n                ones -= 1\n            start += 1\n        best = max(best, end - start + 1)\n    return best",
    "longest_substring_with_same_letters_after_replacement": "def longest_substring_with_same_letters_after_replacement(s, k):\n    start = 0\n    best = 0\n    freq = {}\n    max_rep = 0\n    for end, ch in enumerate(s):\n        freq[ch] = freq.get(ch, 0) + 1\n        if freq[ch] > max_rep:\n            max_rep = freq[ch]\n        while (end - start + 1) - max_rep > k:\n            left = s[start]\n            freq[left] -= 1\n            start += 1\n        best = max(best, end - start + 1)\n    return best"
  }
}
JSON
```

---

## 11. Pattern Practice – Two Pointers

### 11.1 Two Pointers – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/two-pointers/submit
```

**Purpose**

- Submit a suite of **two-pointer** techniques on arrays.
- Covers problems such as `two_sum` (sorted), duplicate removal, sorted squares, 3-sum, product subarrays, and the Dutch National Flag problem.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "two_sum": "<python_source_code>",
    "remove_duplicates": "<python_source_code>",
    "square_sorted_array": "<python_source_code>",
    "three_sum": "<python_source_code>",
    "remove_duplicate_key": "<python_source_code>",
    "three_sum_to_target": "<python_source_code>",
    "triplets_with_smaller_sum": "<python_source_code>",
    "subarrays_with_product_less_than_target": "<python_source_code>",
    "dutch_national_flag_problem": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/two-pointers/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "two_sum": "def two_sum(nums, target):\n    left, right = 0, len(nums) - 1\n    while left < right:\n        s = nums[left] + nums[right]\n        if s == target:\n            return [left, right]\n        if s < target:\n            left += 1\n        else:\n            right -= 1\n    return []",
    "remove_duplicates": "def remove_duplicates(nums):\n    if not nums:\n        return 0\n    next_non_dupe = 1\n    for i in range(1, len(nums)):\n        if nums[i] != nums[next_non_dupe - 1]:\n            nums[next_non_dupe] = nums[i]\n            next_non_dupe += 1\n    return next_non_dupe",
    "square_sorted_array": "def square_sorted_array(nums):\n    n = len(nums)\n    left, right = 0, n - 1\n    res = [0] * n\n    idx = n - 1\n    while left <= right:\n        l2 = nums[left] * nums[left]\n        r2 = nums[right] * nums[right]\n        if l2 > r2:\n            res[idx] = l2\n            left += 1\n        else:\n            res[idx] = r2\n            right -= 1\n        idx -= 1\n    return res",
    "three_sum": "def three_sum(nums):\n    nums.sort()\n    res = []\n    n = len(nums)\n    for i in range(n):\n        if i > 0 and nums[i] == nums[i-1]:\n            continue\n        target = -nums[i]\n        left, right = i + 1, n - 1\n        while left < right:\n            s = nums[left] + nums[right]\n            if s == target:\n                res.append([nums[i], nums[left], nums[right]])\n                left += 1\n                right -= 1\n                while left < right and nums[left] == nums[left-1]:\n                    left += 1\n                while left < right and nums[right] == nums[right+1]:\n                    right -= 1\n            elif s < target:\n                left += 1\n            else:\n                right -= 1\n    return res",
    "remove_duplicate_key": "def remove_duplicate_key(nums, key):\n    next_non_key = 0\n    for i in range(len(nums)):\n        if nums[i] != key:\n            nums[next_non_key] = nums[i]\n            next_non_key += 1\n    return next_non_key",
    "three_sum_to_target": "def three_sum_to_target(nums, target):\n    import math\n    nums.sort()\n    smallest_diff = math.inf\n    n = len(nums)\n    for i in range(n - 2):\n        left, right = i + 1, n - 1\n        while left < right:\n            diff = target - nums[i] - nums[left] - nums[right]\n            if diff == 0:\n                return target\n            if abs(diff) < abs(smallest_diff) or (abs(diff) == abs(smallest_diff) and diff > smallest_diff):\n                smallest_diff = diff\n            if diff > 0:\n                left += 1\n            else:\n                right -= 1\n    return target - smallest_diff",
    "triplets_with_smaller_sum": "def triplets_with_smaller_sum(arr, target):\n    arr.sort()\n    n = len(arr)\n    count = 0\n    for i in range(n - 2):\n        left, right = i + 1, n - 1\n        while left < right:\n            s = arr[i] + arr[left] + arr[right]\n            if s < target:\n                count += (right - left)\n                left += 1\n            else:\n                right -= 1\n    return count",
    "subarrays_with_product_less_than_target": "def subarrays_with_product_less_than_target(arr, target):\n    from collections import deque\n    res = []\n    prod = 1\n    left = 0\n    for right, val in enumerate(arr):\n        prod *= val\n        while prod >= target and left <= right:\n            prod //= arr[left] if prod % arr[left] == 0 else prod / arr[left]\n            left += 1\n        tmp = deque()\n        for i in range(right, left - 1, -1):\n            tmp.appendleft(arr[i])\n            res.append(list(tmp))\n    return res",
    "dutch_national_flag_problem": "def dutch_national_flag_problem(arr):\n    i, low, high = 0, 0, len(arr) - 1\n    while i <= high:\n        if arr[i] == 0:\n            arr[i], arr[low] = arr[low], arr[i]\n            i += 1\n            low += 1\n        elif arr[i] == 1:\n            i += 1\n        else:\n            arr[i], arr[high] = arr[high], arr[i]\n            high -= 1\n    return arr"
  }
}
JSON
```

---

## 12. Pattern Practice – Singleton

### 12.1 Singleton & Borg Singleton – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/singleton/submit
```

**Purpose**

- Submit practice implementations for classic **Singleton** and **Borg Singleton** patterns.
- Includes variants that reset or share state across instances.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "PracticeSingletonClass.__new__": "<python_source_code>",
    "PracticeSingletonChild.print_access": "<python_source_code>",
    "PracticeBorgSingletonClass.__new__": "<python_source_code>",
    "PracticeBorgSingletonChild.print_access": "<python_source_code>",
    "PracticeBorgSingletonResetChild.__new__": "<python_source_code>",
    "PracticeBorgSingletonResetChild.print_access": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/singleton/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "PracticeSingletonClass.__new__": "def __new__(cls):\n    if not hasattr(cls, 'instance'):\n        cls.instance = object.__new__(cls)\n    return cls.instance",
    "PracticeSingletonChild.print_access": "def print_access(self) -> None:\n    print(f'Singleton class_access = {self.get_class_access()}')\n    print(f'Singleton instance_access = {self.get_instance_access()}')",
    "PracticeBorgSingletonClass.__new__": "def __new__(cls, *args, **kwargs):\n    obj = object.__new__(cls)\n    if not hasattr(cls, '_shared_borg_state'):\n        cls._shared_borg_state = {}\n    obj.__dict__ = cls._shared_borg_state\n    return obj",
    "PracticeBorgSingletonChild.print_access": "def print_access(self) -> None:\n    print(f'BorgSingleton class_access = {self.get_class_access()}')\n    print(f'BorgSingleton instance_access = {self.get_instance_access()}')",
    "PracticeBorgSingletonResetChild.__new__": "def __new__(cls, *args, **kwargs):\n    cls._shared_borg_state = {}\n    obj = object.__new__(cls)\n    obj.__dict__ = cls._shared_borg_state\n    return obj",
    "PracticeBorgSingletonResetChild.print_access": "def print_access(self) -> None:\n    print(f'BorgSingleton class_access = {self.get_class_access()}')\n    print(f'BorgSingleton instance_access = {self.get_instance_access()}')"
  }
}
JSON
```

---

## 13. Pattern Practice – Sorting

### 13.1 Sorting Patterns – Submit Practice

**Endpoint**

```text
POST /api/v1/patterns/sorting/submit
```

**Purpose**

- Submit practice implementations for a suite of **sorting algorithms**.
- Covers selection, bubble, insertion, merge, quick, heap, counting, radix, bucket, and novelty `stalin_sort`.

**Request Body (shape)**

```jsonc
{
  "methods": {
    "selection_sort": "<python_source_code>",
    "bubble_sort": "<python_source_code>",
    "insertion_sort": "<python_source_code>",
    "merge_sort": "<python_source_code>",
    "partition": "<python_source_code>",
    "quick_sort": "<python_source_code>",
    "heapify": "<python_source_code>",
    "heap_sort": "<python_source_code>",
    "counting_sort": "<python_source_code>",
    "radix_sort": "<python_source_code>",
    "bucket_sort": "<python_source_code>",
    "stalin_sort": "<python_source_code>"
  }
}
```

**Sample Call**

```bash
curl -s http://127.0.0.1:8080/api/v1/patterns/sorting/submit \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON' | jq
{
  "methods": {
    "selection_sort": "def selection_sort(nums: list[int]) -> list[int]:\n    for i in range(len(nums) - 1):\n        m = i\n        for j in range(i + 1, len(nums)):\n            if nums[j] < nums[m]:\n                m = j\n        nums[m], nums[i] = nums[i], nums[m]\n    return nums",
    "bubble_sort": "def bubble_sort(nums: list[int]) -> list[int]:\n    n = len(nums)\n    for i in range(n - 1):\n        swapped = False\n        for j in range(n - i - 1):\n            if nums[j] > nums[j + 1]:\n                nums[j], nums[j + 1] = nums[j + 1], nums[j]\n                swapped = True\n        if not swapped:\n            break\n    return nums",
    "insertion_sort": "def insertion_sort(nums: list[int]) -> list[int]:\n    for i in range(1, len(nums)):\n        key = nums[i]\n        j = i - 1\n        while j >= 0 and nums[j] > key:\n            nums[j + 1] = nums[j]\n            j -= 1\n        nums[j + 1] = key\n    return nums",
    "merge_sort": "def merge_sort(self, nums: list[int]) -> list[int]:\n    if len(nums) <= 1:\n        return nums\n    mid = len(nums) // 2\n    left = nums[:mid]\n    right = nums[mid:]\n    self.merge_sort(left)\n    self.merge_sort(right)\n    i = j = k = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            nums[k] = left[i]\n            i += 1\n        else:\n            nums[k] = right[j]\n            j += 1\n        k += 1\n    while i < len(left):\n        nums[k] = left[i]\n        i += 1; k += 1\n    while j < len(right):\n        nums[k] = right[j]\n        j += 1; k += 1\n    return nums",
    "partition": "def partition(nums, low, high) -> int:\n    pivot = nums[high]\n    i = low - 1\n    for j in range(low, high):\n        if nums[j] <= pivot:\n            i += 1\n            nums[i], nums[j] = nums[j], nums[i]\n    nums[i+1], nums[high] = nums[high], nums[i+1]\n    return i + 1",
    "quick_sort": "def quick_sort(self, nums: list[int], low: int, high: int) -> list[int]:\n    if len(nums) <= 1:\n        return nums\n    if low < high:\n        pi = self.partition(nums, low, high)\n        self.quick_sort(nums, low, pi - 1)\n        self.quick_sort(nums, pi + 1, high)\n    return nums",
    "heapify": "def heapify(self, nums, n, i) -> None:\n    largest = i\n    l = 2 * i + 1\n    r = 2 * i + 2\n    if l < n and nums[l] > nums[largest]:\n        largest = l\n    if r < n and nums[r] > nums[largest]:\n        largest = r\n    if largest != i:\n        nums[i], nums[largest] = nums[largest], nums[i]\n        self.heapify(nums, n, largest)",
    "heap_sort": "def heap_sort(self, nums: list[int]) -> list[int]:\n    n = len(nums)\n    for i in range(n // 2 - 1, -1, -1):\n        self.heapify(nums, n, i)\n    for i in range(n - 1, 0, -1):\n        nums[i], nums[0] = nums[0], nums[i]\n        self.heapify(nums, i, 0)\n    return nums",
    "counting_sort": "def counting_sort(nums, exp1) -> None:\n    n = len(nums)\n    output = [0] * n\n    count = [0] * 10\n    for i in range(n):\n        index = (nums[i] // exp1) % 10\n        count[index] += 1\n    for i in range(1, 10):\n        count[i] += count[i - 1]\n    for i in range(n - 1, -1, -1):\n        index = (nums[i] // exp1) % 10\n        output[count[index] - 1] = nums[i]\n        count[index] -= 1\n    for i in range(n):\n        nums[i] = output[i]",
    "radix_sort": "def radix_sort(self, nums: list[int]) -> list[int]:\n    if not nums:\n        return nums\n    max_val = max(nums)\n    exp = 1\n    while max_val // exp > 0:\n        self.counting_sort(nums, exp)\n        exp *= 10\n    return nums",
    "bucket_sort": "def bucket_sort(self, nums: list[float]) -> list[float]:\n    if not nums:\n        return nums\n    slot_num = 10\n    buckets = [[] for _ in range(slot_num)]\n    for v in nums:\n        idx = min(slot_num - 1, int(v * slot_num))\n        buckets[idx].append(v)\n    k = 0\n    for b in buckets:\n        # reuse insertion_sort implementation\n        b = self.insertion_sort(b)\n        for x in b:\n            nums[k] = x\n            k += 1\n    return nums",
    "stalin_sort": "def stalin_sort(nums: list[int]) -> list[int]:\n    if not nums:\n        return []\n    res = [nums[0]]\n    last = nums[0]\n    for x in nums[1:]:\n        if x >= last:\n            res.append(x)\n            last = x\n    return res"
  }
}
JSON
```
