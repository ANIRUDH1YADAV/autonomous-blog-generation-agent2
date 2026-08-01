import streamlit as st


def render_evidence(evidence):

    if not evidence:
        st.info("No evidence collected.")
        return

    for item in evidence:

        if isinstance(item, dict):
            title = item.get("title", "Evidence")
            data = item
        else:
            title = getattr(item, "title", "Evidence")
            data = item.model_dump() if hasattr(item, "model_dump") else vars(item)

        with st.expander(title):
            st.json(data)