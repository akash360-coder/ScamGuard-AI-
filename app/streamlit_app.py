import streamlit as st

from src.classifier import ScamClassifier

st.set_page_config(page_title="ScamGuard AI", layout="wide")
st.title("🛡️ ScamGuard AI")
st.caption("Explainable scam detection powered by LLM reasoning")

classifier = ScamClassifier()

user_input = st.text_area("Paste a suspicious message here:", height=180, placeholder="Example: 'URGENT! Your phone has been suspended...' ")

if st.button("Analyze Message", use_container_width=True):
    if not user_input.strip():
        st.warning("Please enter a message to analyze.")
    else:
        with st.spinner("Analyzing message..."):
            result = classifier.classify(user_input)
            explanation = classifier.explain(user_input, result)

        st.subheader("Result")
        col1, col2, col3 = st.columns(3)

        with col1:
            if result["classification"] == "SCAM":
                st.error("⚠️ SCAM DETECTED")
            else:
                st.success("✅ Legitimate")

        with col2:
            st.metric("Confidence", f"{result['confidence']:.0%}")

        with col3:
            st.write(f"**Type:** {result.get('scam_type', 'N/A')}")

        st.subheader("Red Flags")
        if result.get("red_flags"):
            for flag in result["red_flags"]:
                st.markdown(f"- {flag}")
        else:
            st.write("No obvious red flags identified.")

        st.subheader("Intent")
        st.write(result.get("intent", "Not identified."))

        st.subheader("Reasoning")
        st.info(result.get("reasoning", "No reasoning provided."))

        st.subheader("Explanation")
        st.write(explanation)
