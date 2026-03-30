import streamlit as st
import json
import pandas as pd
import plotly.express as px

from utils.parser import extract_text
from utils.skills import extract_skills
from utils.matcher import calculate_match

# ✅ NEW (DATABASE)
from database import create_table, insert_data

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# ---------- CREATE DB TABLE ----------
create_table()

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>
body { background-color: #0e1117; }

h1 {
    color: white;
    text-align: center;
    font-size: 40px;
}

.card {
    background: linear-gradient(145deg, #1c1f26, #232734);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.6);
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    color: #00c6ff;
    margin-bottom: 10px;
}

.tag {
    display: inline-block;
    padding: 8px 12px;
    margin: 5px;
    border-radius: 20px;
    font-size: 14px;
}

.tag-success { background-color: #28a745; color: white; }
.tag-danger { background-color: #dc3545; color: white; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Analyze your resume against job roles</p>", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
with open("data/skills_list.json") as f:
    job_data = json.load(f)

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Settings")
job_role = st.sidebar.selectbox("Select Job Role", list(job_data.keys()))

uploaded_file = st.file_uploader("📄 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

# ---------- ATS SCORE ----------
def calculate_ats_score(text):
    score = 0
    text = text.lower()

    keywords = ["experience", "projects", "skills", "education", "internship"]

    for word in keywords:
        if word in text:
            score += 15

    if len(text) > 1000:
        score += 25

    return min(score, 100)

# ---------- MAIN ----------
if uploaded_file:
    text = extract_text(uploaded_file)

    # ---------- TEXT VIEW ----------
    with st.expander("📄 View Extracted Text"):
        st.write(text[:1000])

    job_skills = job_data[job_role]
    resume_skills = extract_skills(text, job_skills)

    score, matched, missing = calculate_match(resume_skills, job_skills)

    ats_score = calculate_ats_score(text)

    # ---------- SAVE TO DATABASE (🔥 IMPORTANT) ----------
    insert_data(
        job_role,
        score,
        ats_score,
        ", ".join(matched),
        ", ".join(missing)
    )

    # ---------- FEEDBACK ----------
    if score > 75:
        st.success("🔥 Strong Match! You're job-ready.")
    elif score > 50:
        st.warning("⚡ Moderate match — Improve some skills.")
    else:
        st.error("🚨 Low match — Focus on missing skills.")

    # ---------- ANALYSIS ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>📊 Analysis Result</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # Match Score
    col1.markdown(f"""
    <div class='card'>
    <h2 style='color:#00ffcc;'>🎯 {score}%</h2>
    <p>Match Score</p>
    </div>
    """, unsafe_allow_html=True)

    # ATS Score
    col2.markdown(f"""
    <div class='card'>
    <h2 style='color:#ffaa00;'>📄 {ats_score}/100</h2>
    <p>ATS Score</p>
    </div>
    """, unsafe_allow_html=True)

    # Matched Skills
    col3.markdown("### ✅ Matched Skills")
    for skill in matched:
        col3.markdown(f"<span class='tag tag-success'>{skill}</span>", unsafe_allow_html=True)

    # Missing Skills
    col4.markdown("### ❌ Missing Skills")
    for skill in missing:
        col4.markdown(f"<span class='tag tag-danger'>{skill}</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- CHART ----------
    chart_data = {
        "Category": ["Matched", "Missing"],
        "Count": [len(matched), len(missing)]
    }

    fig = px.pie(
        values=chart_data["Count"],
        names=chart_data["Category"],
        title="Skill Distribution"
    )

    st.plotly_chart(fig, width='stretch')

    # ---------- DOWNLOAD ----------
    result_data = {
        "Job Role": job_role,
        "Match Score": score,
        "ATS Score": ats_score,
        "Matched Skills": ", ".join(matched),
        "Missing Skills": ", ".join(missing)
    }

    df = pd.DataFrame([result_data])

    st.download_button(
        label="📥 Download Results as CSV",
        data=df.to_csv(index=False),
        file_name="resume_analysis.csv",
        mime="text/csv"
    )

else:
    st.info("📄 Please upload a resume to get analysis")

# ---------- FOOTER ----------
st.markdown("""
<hr>
<p style='text-align:center;color:gray; font-size:14px;'>
Built with ❤️ using Python & Streamlit <br>
<span style='color:#00c6ff;'>👩‍💻 Sneha Sunny</span>
</p>
""", unsafe_allow_html=True)