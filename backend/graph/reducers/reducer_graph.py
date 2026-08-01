from langgraph.graph import (
    StateGraph,
    START,
    END
)

from schemas.state import BlogState

from graph.nodes.merge_content import (
    merge_content
)

from graph.nodes.decide_images import (
    decide_images
)

from graph.nodes.generate_images import (
    generate_and_place_images
)


reducer_graph = StateGraph(
    BlogState
)

reducer_graph.add_node(
    "merge_content",
    merge_content
)

reducer_graph.add_node(
    "decide_images",
    decide_images
)

reducer_graph.add_node(
    "generate_and_place_images",
    generate_and_place_images
)

reducer_graph.add_edge(
    START,
    "merge_content"
)

reducer_graph.add_edge(
    "merge_content",
    "decide_images"
)

reducer_graph.add_edge(
    "decide_images",
    "generate_and_place_images"
)

reducer_graph.add_edge(
    "generate_and_place_images",
    END
)

reducer_subgraph = (
    reducer_graph.compile()
)