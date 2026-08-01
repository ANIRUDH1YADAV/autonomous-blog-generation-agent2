from graph.nodes.decide_images import decide_images
from graph.nodes.generate_images import generate_and_place_images


from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.types import Send

from schemas.state import BlogState

from graph.nodes.router import (
    router_node,
    route_next
)

from graph.nodes.research import (
    research_node
)

from graph.nodes.orchestrator import (
    orchestrator_node
)

from graph.nodes.worker import (
    worker_node
)

from graph.reducers.reducer_graph import (
    reducer_subgraph
)


def fanout(state: BlogState):

    assert state["plan"] is not None

    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["topic"],
                "mode": state["mode"],
                "as_of": state["as_of"],
                "recency_days": state["recency_days"],
                "plan": state["plan"].model_dump(),
                "evidence": [
                    e.model_dump()
                    for e in state.get("evidence", [])
                ],
            },
        )
        for task in state["plan"].tasks
    ]


g = StateGraph(
    BlogState
)

# Nodes
g.add_node(
    "router",
    router_node
)

g.add_node(
    "research",
    research_node
)

g.add_node(
    "orchestrator",
    orchestrator_node
)

g.add_node(
    "worker",
    worker_node
)

g.add_node(
    "reducer",
    reducer_subgraph
)

g.add_node(
    "decide_images",
    decide_images
)

g.add_node(
    "generate_images",
    generate_and_place_images
)

# Start
g.add_edge(
    START,
    "router"
)

# Router → Research / Orchestrator
g.add_conditional_edges(
    "router",
    route_next,
    {
        "research": "research",
        "orchestrator": "orchestrator"
    }
)

# Research → Orchestrator
g.add_edge(
    "research",
    "orchestrator"
)

# Orchestrator → Workers (Parallel Fanout)
g.add_conditional_edges(
    "orchestrator",
    fanout,
    ["worker"]
)

# Workers → Reducer
g.add_edge(
    "worker",
    "reducer"
)

# Reducer → Decide Images → Generate Images → End
g.add_edge(
    "reducer",
    "decide_images"
)

g.add_edge(
    "decide_images",
    "generate_images"
)

g.add_edge(
    "generate_images",
    END
)

# Compile Graph
app = g.compile()