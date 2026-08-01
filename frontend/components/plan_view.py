import streamlit as st


def render_plan(plan):

    if not plan:
        st.info("No plan available.")
        return

    st.subheader(plan.blog_title)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Audience",
        plan.audience
    )

    col2.metric(
        "Tone",
        plan.tone
    )

    col3.metric(
        "Type",
        plan.blog_kind
    )

    st.divider()

    for task in plan.tasks:

        with st.expander(
            f"Task {task.id} • {task.title}"
        ):

            st.write(
                task.goal
            )

            st.markdown("### Bullets")

            for bullet in task.bullets:
                st.markdown(
                    f"- {bullet}"
                )

            st.caption(
                f"Target Words: {task.target_words}"
            )