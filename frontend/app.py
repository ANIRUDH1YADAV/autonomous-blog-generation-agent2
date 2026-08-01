import streamlit as st

from datetime import date

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "backend"))

from graph.workflow import app

from components.plan_view import (
    render_plan
)

from components.evidence_view import (
    render_evidence
)

from components.blog_view import (
    render_blog
)

from components.images_view import (
    render_images
)

from components.logs_view import (
    render_logs
)


st.set_page_config(
    page_title="Blog Writing Agent",
    page_icon="📝",
    layout="wide"
)

if "result" not in st.session_state:
    st.session_state.result = None


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title(
        "Generate New Blog"
    )

    topic = st.text_area(
        "Topic",
        height=120
    )

    as_of = st.date_input(
        "As-of Date",
        value=date.today()
    )

    generate = st.button(
        "🚀 Generate Blog",
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "History"
    )

    st.info(
        "History storage coming next."
    )


# ---------------- HEADER ----------------

st.title(
    "Blog Writing Agent"
)

st.caption(
    "LangGraph + FastAPI + Groq"
)

# ---------------- GENERATE ----------------

if generate:

    if not topic.strip():

        st.warning(
            "Enter a topic."
        )

    else:

        try:

            inputs = {
                "topic": topic,
                "mode": "",
                "needs_research": False,
                "queries": [],
                "evidence": [],
                "plan": None,
                "as_of": str(as_of),
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

            progress_area = st.empty()

            current_state = {}

            last_node = None

            for event in app.stream(
                inputs,
                stream_mode="updates"
            ):

                if (
                    isinstance(event, dict)
                    and len(event) == 1
                ):

                    node_name = next(
                        iter(event.keys())
                    )

                    if node_name != last_node:

                        status.write(
                            f"➡️ Node: `{node_name}`"
                        )

                        last_node = node_name

                    node_output = event[
                        node_name
                    ]

                    if isinstance(
                        node_output,
                        dict
                    ):
                        current_state.update(
                            node_output
                        )

                    progress_area.json(
                        {
                            "mode": current_state.get(
                                "mode"
                            ),
                            "evidence_count": len(
                                current_state.get(
                                    "evidence",
                                    []
                                )
                            ),
                            "sections": len(
                                current_state.get(
                                    "sections",
                                    []
                                )
                            ),
                            "images": len(
                                current_state.get(
                                    "image_specs",
                                    []
                                )
                            )
                        }
                    )

            final_state = app.invoke(
                inputs
            )

            st.session_state.result = {
                "success": True,
                "markdown": final_state.get(
                    "final",
                    ""
                ),
                "plan": final_state.get(
                    "plan"
                ),
                "evidence": final_state.get(
                    "evidence",
                    []
                ),
                "image_specs": final_state.get(
                    "image_specs",
                    []
                ),
                "logs": final_state
            }

            status.update(
                label="✅ Completed",
                state="complete"
            )

        except Exception as e:

            st.error(str(e))


# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🧩 Plan",
        "📚 Evidence",
        "📄 Blog",
        "🖼 Images",
        "📋 Logs"
    ]
)

if st.session_state.result:

    result = st.session_state.result

    with tab1:

        render_plan(
            result.get("plan")
        )

    with tab2:

        render_evidence(
            result.get(
                "evidence",
                []
            )
        )

    with tab3:

        render_blog(
            result.get(
                "markdown",
                ""
            )
        )

    with tab4:

        render_images(
            result.get(
                "image_specs",
                []
            )
        )

    with tab5:

        render_logs(
            result.get(
                "logs",
                {}
            )
        )