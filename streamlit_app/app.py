import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="SHL Assessment Recommendation Assistant",
    page_icon="🎯",
    layout="wide",
)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("🎯 SHL Assessment Recommendation Assistant")

st.markdown(
    """
Find the most relevant **SHL assessments** using AI-powered semantic search,
vector retrieval, and conversational recommendations.

Paste a hiring requirement or job description below to receive grounded,
explainable SHL assessment recommendations.
"""
)

st.divider()

# ----------------------------------------------------
# Input
# ----------------------------------------------------

with st.container(border=True):

    st.subheader("📄 Hiring Requirement")

    query = st.text_area(
        "Hiring Requirement",
        height=180,
        label_visibility="collapsed",
        placeholder=(
            "Example:\n\n"
            "We are hiring a Java Backend Developer with experience in "
            "Spring Boot, REST APIs, SQL, Microservices, and strong "
            "problem-solving skills."
        ),
    )

# ----------------------------------------------------
# Search Button
# ----------------------------------------------------

if st.button(
    "🔍 Find Best Assessments",
    type="primary",
    use_container_width=True,
):

    if not query.strip():
        st.warning("Please enter a hiring requirement.")
        st.stop()

    with st.spinner(
        "🔍 Searching SHL catalog and generating AI recommendations..."
    ):

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code != 200:
            st.error("Unable to contact the API.")
            st.stop()

        data = response.json()

    # ------------------------------------------------
    # Recommendation Response
    # ------------------------------------------------

    if data.get("recommendations"):

        st.success(
            f"✅ Found {len(data['recommendations'])} recommended assessments."
        )

        st.subheader("🧠 AI Recommendation Summary")

        st.info(data["reply"])

        st.subheader("📋 Recommended Assessments")

        for assessment in data["recommendations"]:

            with st.container(border=True):

                st.markdown(f"## {assessment['name']}")

                col1, col2, col3, col4, col5 = st.columns(5)

                col1.metric(
                    "🎯 Match",
                    assessment.get("match_score", "N/A"),
                )

                col2.metric(
                    "⏱ Duration",
                    assessment.get("duration") or "N/A",
                )

                col3.metric(
                    "🌐 Remote",
                    assessment.get("remote") or "N/A",
                )

                col4.metric(
                    "🧠 Adaptive",
                    assessment.get("adaptive") or "N/A",
                )

                similarity = assessment.get("retrieval_score")

                if similarity is not None:
                    similarity = f"{similarity * 100:.1f}%"

                col5.metric(
                    "📊 Similarity",
                    similarity,
                )

                st.markdown("### Why this assessment?")

                st.write(
                    assessment.get("reason", "")
                )

                st.link_button(
                    "🔗 Open SHL Assessment",
                    assessment["url"],
                    use_container_width=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------
    # Clarification / Comparison / Out-of-Scope
    # ------------------------------------------------

    else:

        st.info(data["reply"])