import streamlit as st
import pdfplumber

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer - Home",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("🛠️ Navigation")
st.sidebar.success("Select 'Analytics' from the sidebar after uploading your resume.")

st.title("🚀 AI Resume Analyzer & Job Recommendation System")
st.write("Welcome! Upload your resume (PDF) to get instant AI-powered analysis, skill matching, and summary.")

# Predefined list of skills
PREDEFINED_SKILLS = [
    "Python", "Java", "C++", "C", "JavaScript", "HTML", "CSS", "React", 
    "Node.js", "SQL", "MongoDB", "Machine Learning", "Data Science", 
    "Pandas", "NumPy", "Streamlit", "Excel", "Communication", "Problem Solving"
]

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    # Extract text from PDF using pdfplumber
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
            
    found_skills = []
    for skill in PREDEFINED_SKILLS:
        if skill.lower() in text.lower():
            found_skills.append(skill)
            
    missing_skills = [skill for skill in PREDEFINED_SKILLS if skill not in found_skills]
    
    # 🌟 மிக முக்கியமானது: செஷன் ஸ்டேட்டில் டேட்டாவை சேமிக்கிறோம்
    st.session_state['resume_text'] = text
    st.session_state['found_skills'] = found_skills
    st.session_state['missing_skills'] = missing_skills
    st.session_state['file_name'] = uploaded_file.name

    st.success("Resume uploaded and processed successfully! You can now view Analytics.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Extracted Resume Text Preview")
        st.text_area("Resume Content", text[:600], height=200)
        
    with col2:
        st.subheader("🎯 Extracted Skills from Resume")
        if found_skills:
            st.success(", ".join(found_skills))
        else:
            st.warning("No matching predefined skills found in this resume.")

    st.markdown("---")

    # AI Resume Summary Generator
    st.subheader("📝 Automated AI Resume Summary")
    word_count = len(text.split())
    skills_text = ", ".join(found_skills) if found_skills else "General technical"
    
    ai_summary = (
        f"Dedicated professional with a background comprising approximately {word_count} words of documented project and experience details. "
        f"Demonstrated core competencies and technical proficiencies in key areas including **{skills_text}**. "
        f"Well-suited for roles requiring structured problem-solving, technical execution, and continuous adaptability."
    )
    st.success(ai_summary)

    st.info("💡 **Next Step:** Click on **Analytics** in the left sidebar to view interactive charts and match scores!")