import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Job Match Analytics & Visuals",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Advanced Job Match Analytics & Visualizations")

# ஹோம் பேஜில் அப்லோட் செய்த ரெஸ்யூம் டேட்டாவை எடுத்துக்கொள்கிறோம்
if 'resume_text' not in st.session_state:
    st.warning("⚠️ Please upload a resume first on the Home page (`app.py`) to view analytics!")
else:
    text = st.session_state['resume_text']
    found_skills = st.session_state['found_skills']
    missing_skills = st.session_state['missing_skills']
    file_name = st.session_state['file_name']

    JOB_DESCRIPTIONS = {
        "Python Developer": "Looking for a Python Developer experienced in Python programming, database management using SQL and MongoDB, backend development, and script optimization.",
        "Full Stack Developer": "Seeking a Full Stack Developer skilled in JavaScript, HTML, CSS, React for frontend, and Node.js for backend development.",
        "Data Scientist / Analyst": "Hiring Data Scientist / Analyst with strong skills in Python, Pandas, NumPy, Machine Learning, Data Science, SQL, and Excel for data modeling and analysis.",
        "Software Engineer": "Software Engineer position requiring strong foundations in Java, C++, C, data structures, and problem-solving abilities."
    }

    st.subheader("🤖 Predefined Job Roles Match Scores")
    
    job_names = []
    match_percentages = []
    recommended_jobs = []
    
    for job, jd_text in JOB_DESCRIPTIONS.items():
        vectorizer = TfidfVectorizer().fit_transform([text, jd_text])
        vectors = vectorizer.toarray()
        similarity_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        ai_match_percentage = int(similarity_score * 100)
        
        job_names.append(job)
        match_percentages.append(ai_match_percentage)
        
        col_j1, col_j2 = st.columns([3, 1])
        with col_j1:
            st.write(f"**{job}**")
            st.progress(ai_match_percentage)
        with col_j2:
            st.metric(label="AI Match", value=f"{ai_match_percentage}%")
            
        if ai_match_percentage > 10:
            recommended_jobs.append(f"{job} ({ai_match_percentage}%)")

    st.markdown("---")

    # Plotly Bar Chart
    st.subheader("📈 Interactive Job Fit Comparison Chart")
    df_chart = pd.DataFrame({
        "Job Role": job_names,
        "Match Percentage": match_percentages
    })
    
    fig = px.bar(
        df_chart, 
        x="Job Role", 
        y="Match Percentage", 
        color="Match Percentage",
        color_continuous_scale="blues",
        text="Match Percentage",
        title="Suitability Across Industry Roles"
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Download Report Feature
    st.subheader("📥 Download Analysis Report")
    report_data = {
        "File Name": [file_name],
        "Extracted Skills": [", ".join(found_skills) if found_skills else "None"],
        "Missing Skills": [", ".join(missing_skills[:6]) if missing_skills else "None"],
        "Recommended Jobs": [", ".join(recommended_jobs) if recommended_jobs else "None"]
    }
    df_report = pd.DataFrame(report_data)
    csv_data = df_report.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Structured Report as CSV",
        data=csv_data,
        file_name="ai_resume_analysis_report.csv",
        mime="text/csv"
    )
