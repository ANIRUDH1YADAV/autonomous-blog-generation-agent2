import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "backend"))

import streamlit as st

from graph.workflow import app

inputs = {
    "topic": "What is LangGraph",
    "mode": "",
    "needs_research": False,
    "queries": [],
    "evidence": [],
    "plan": None,
    "as_of": "2026-06-26",
    "recency_days": 7,
    "sections": [],
    "merged_md": "",
    "md_with_placeholders": "",
    "image_specs": [],
    "final": "",
}

status = st.status(
    "Running Graph...",
    expanded=True
)

final_state = {}

for event in app.stream(
    inputs,
    stream_mode="updates"
):

    node_name = list(
        event.keys()
    )[0]

    status.write(
        f"Node: {node_name}"
    )

    final_state.update(
        event[node_name]
    )

status.update(
    label="Done",
    state="complete"
)

st.json(final_state)