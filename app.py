import streamlit as st
import json
from parser import extract_text
from scorer import score_cv

st.title("CV-JD Fit Scorer")
st.caption("Upload a CV and paste a job description to get an instant fit analysis.")

uploaded_file = st.file_uploader("Upload CV (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=200)

if st.button("Analyse"):
    if not jd_text.strip():
        st.warning("Please paste a job description before analysing.")
    elif uploaded_file is None:
        st.warning("Please upload a CV before analysing.")
    else:
        with st.spinner("Analysing..."):
            try:
                cv_text = extract_text(uploaded_file)
                result = score_cv(cv_text, jd_text)

                st.subheader(f"Match Score: {result['score']} / 100")
                st.progress(result['score'] / 100)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Strengths**")
                    for s in result['strengths']:
                        st.markdown(f"✅ {s}")
                with col2:
                    st.markdown("**Gaps**")
                    for g in result['gaps']:
                        st.markdown(f"⚠️ {g}")

                st.info(f"**Recommendation:** {result['recommendation']}")

            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")