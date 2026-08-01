import streamlit as st


def render_images(images):

    if not images:

        st.info(
            "No image specifications generated."
        )

        return

    for image in images:

        with st.container():

            st.subheader(
                image.filename
            )

            st.write(
                image.caption
            )

            st.code(
                image.prompt
            )

            col1, col2 = st.columns(2)

            col1.write(
                f"Size: {image.size}"
            )

            col2.write(
                f"Quality: {image.quality}"
            )

            st.divider()