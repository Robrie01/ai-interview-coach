
import streamlit as st
import openai
import json
from fpdf import FPDF
import datetime
import os

# ------------------ SETUP ------------------
openai.api_key = os.environ["OPENAI_API_KEY"]

# ------------------ DEFAULT PROFILE ------------------
def get_default_profile():
    return {
        "name": "Roy O’Brien",
        "title": "IT Systems Technician",
        "location": "Derry, Northern Ireland",
        "experience": [],
        "skills": [],
        "softSkills": [],
        "learning": [],
        "certifications": [],
        "goals": ""
    }

# ------------------ FUNCTION ------------------
def generate_interview_answer(question, profile):
    system_prompt = (
        "You are simulating interview responses for Roy O’Brien, based on the following profile data.\n"
        f"{json.dumps(profile)}\n\n"
        "Answer the following interview question as if you are Roy, in a clear and confident tone."
    )
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# ------------------ PDF EXPORT ------------------
def save_to_pdf(question, answer):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Question: {question}\n\nAnswer: {answer}")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"interview_answer_{timestamp}.pdf"
    pdf.output(filename)
    return filename

# ------------------ UI ------------------
st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🧠 Roy's AI Interview Coach")

st.write("Fill out or update your profile, then ask an interview-style question.")

# Editable profile fields
with st.expander("📝 Edit Profile"):
    name = st.text_input("Name", "Roy O’Brien")
    title = st.text_input("Job Title", "IT Systems Technician")
    location = st.text_input("Location", "Derry, Northern Ireland")
    experience = st.text_area("Experience (as bullet points)", "- IT Systems Technician at BT Group\n- Customer IT Support at BT Group\n- Technical Customer Service at EE")
    skills = st.text_area("Technical Skills (comma-separated)", "Windows, macOS, Linux, VMware, TeamViewer")
    soft_skills = st.text_area("Soft Skills (comma-separated)", "Problem-solving, Communication, Knowledge Sharing")
    learning = st.text_area("Currently Learning", "AWS CLF-C02, Azure AZ-900, Advanced Python")
    certifications = st.text_area("Certifications", "Python Programming (OpenEDG)")
    goals = st.text_area("Career Goals", "Explore roles in cloud, cybersecurity, or DevOps with learning opportunities.")

# Build profile from form
profile_data = {
    "name": name,
    "title": title,
    "location": location,
    "experience": experience.split("\n"),
    "skills": [s.strip() for s in skills.split(",")],
    "softSkills": [s.strip() for s in soft_skills.split(",")],
    "learning": learning.split(","),
    "certifications": certifications.split(","),
    "goals": goals
}

# Interview Q&A
st.markdown("---")
st.subheader("💬 Interview Simulator")
question_input = st.text_input("Enter your interview question")

if st.button("Generate Answer") and question_input:
    with st.spinner("Thinking..."):
        answer = generate_interview_answer(question_input, profile_data)
        st.markdown("---")
        st.subheader("🗣️ Answer:")
        st.write(answer)

        if st.button("📄 Export as PDF"):
            filename = save_to_pdf(question_input, answer)
            st.success(f"Saved as {filename}")
