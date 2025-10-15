from fastapi import FastAPI

from cs_fundamentals.routers.health import router as health_router
from cs_fundamentals.routers.data_structures_bst_runner import (
    router as binary_search_tree_router,
)
from cs_fundamentals.routers.data_structures_graph_union_find_runner import (
    router as graph_union_find_router,
)
from cs_fundamentals.routers.data_structures_graph_islands_runner import (
    router as graph_islands_router,
)
from cs_fundamentals.routers.data_structures_linked_list_double_runner import (
    router as linked_list_double_router,
)
from cs_fundamentals.routers.data_structures_linked_list_single_runner import (
    router as linked_list_single_router,
)
from cs_fundamentals.routers.data_structures_max_heap_runner import (
    router as max_heap_router,
)
from cs_fundamentals.routers.data_structures_min_heap_runner import (
    router as min_heap_router,
)
from cs_fundamentals.routers.data_structures_queue_array_runner import (
    router as queue_array_router,
)
from cs_fundamentals.routers.data_structures_queue_linked_list_runner import (
    router as queue_linked_list_router,
)
from cs_fundamentals.routers.data_structures_stack_array_runner import (
    router as stack_array_router,
)
from cs_fundamentals.routers.data_structures_stack_linked_list_runner import (
    router as stack_linked_list_router,
)
from cs_fundamentals.routers.patterns_bfs_runner import (
    router as breadth_first_search_router,
)
from cs_fundamentals.routers.patterns_dfs_runner import (
    router as depth_first_search_router,
)
from cs_fundamentals.routers.patterns_singleton import router as singleton_router
from cs_fundamentals.routers.patterns_fast_slow_pointers_runner import (
    router as fast_slow_pointers_router,
)
from cs_fundamentals.routers.patterns_sliding_window_runner import (
    router as sliding_window_router,
)
from cs_fundamentals.routers.patterns_sorting import router as sorting_router
from cs_fundamentals.routers.patterns_two_pointers_runner import (
    router as two_pointers_router,
)
from cs_fundamentals.routers.practice_runner import router as practice_router
from cs_fundamentals.routers.practice_matrix_runner import (
    router as practice_matrix_router,
)
from cs_fundamentals.routers.targets import router as targets_router


app: FastAPI = FastAPI(title="CS Fundamentals API", version="0.1.0")
v1_prefix: str = "/api/v1"

# Core
app.include_router(health_router, prefix=v1_prefix)
app.include_router(practice_matrix_router, prefix=v1_prefix)
app.include_router(practice_router, prefix=v1_prefix)
app.include_router(targets_router, prefix=v1_prefix)

# Data Structures
app.include_router(binary_search_tree_router, prefix=v1_prefix)
app.include_router(graph_islands_router, prefix=v1_prefix)
app.include_router(graph_union_find_router, prefix=v1_prefix)
app.include_router(linked_list_double_router, prefix=v1_prefix)
app.include_router(linked_list_single_router, prefix=v1_prefix)
app.include_router(max_heap_router, prefix=v1_prefix)
app.include_router(min_heap_router, prefix=v1_prefix)
app.include_router(queue_array_router, prefix=v1_prefix)
app.include_router(queue_linked_list_router, prefix=v1_prefix)
app.include_router(stack_array_router, prefix=v1_prefix)
app.include_router(stack_linked_list_router, prefix=v1_prefix)

# Patterns
app.include_router(breadth_first_search_router, prefix=v1_prefix)
app.include_router(depth_first_search_router, prefix=v1_prefix)
app.include_router(fast_slow_pointers_router, prefix=v1_prefix)
app.include_router(singleton_router, prefix=v1_prefix)
app.include_router(sliding_window_router, prefix=v1_prefix)
app.include_router(sorting_router, prefix=v1_prefix)
app.include_router(two_pointers_router, prefix=v1_prefix)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "API is running", "docs": "/docs"}
