# 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
import streamlit as st
from groq import Groq
import speech_recognition as sr
from gtts import gTTS
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# -------------------------
# GROQ API KEY
# -------------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------------
# PAGE SETTINGS
# -------------------------

st.set_page_config(page_title="AI Medical Prescription Generator", page_icon="💊")

st.title("💊 AI Medical Prescription Generator")
st.warning("⚠️ This system is for educational purposes only.")

# -------------------------
# SIDEBAR PATIENT DETAILS
# -------------------------

st.sidebar.header("Patient Details")

name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", min_value=1, max_value=120)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.sidebar.number_input("Weight (kg)")
allergies = st.sidebar.text_input("Allergies (if any)")

# -------------------------
# VOICE INPUT FUNCTION
# -------------------------

def voice_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak symptoms")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            st.success("Recognized: " + text)
            return text
        except:
            st.error("Voice not recognized")
            return ""

# -------------------------
# SYMPTOMS INPUT
# -------------------------

st.subheader("Symptoms")

symptoms = st.text_area("Enter symptoms")

if st.button("🎤 Speak Symptoms"):
    symptoms = voice_input()

duration = st.selectbox(
    "Duration of symptoms",
    ["1 day", "2-3 days", "1 week", "More than 1 week"]
)

severity = st.selectbox(
    "Severity",
    ["Mild", "Moderate", "Severe"]
)

# -------------------------
# GENERATE PRESCRIPTION
# -------------------------

if st.button("Generate Prescription"):

    if symptoms == "":
        st.warning("Please enter symptoms")

    else:

        prompt = f"""
You are an AI medical assistant. Generate a personalized medical prescription.

Patient Details
Name: {name}
Age: {age}
Gender: {gender}
Weight: {weight} kg
Allergies: {allergies}

Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}

Provide response in this structured format:

1. Possible Condition
Explain the likely illness.

2. Recommended Antibiotic Medicines (if required)
Give 2–3 commonly used antibiotics with dosage and duration.

3. Other Medicines
Pain relievers or fever reducers.

4. Dosage Instructions
Explain when and how medicines should be taken.

5. Possible Side Effects
Mention common side effects.

6. What to Avoid
Food, drinks, or habits to avoid.

7. Lifestyle Advice
Rest, hydration, diet.

8. When to See a Doctor
Warning signs requiring medical attention.

Give safe general advice only.
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=600
        )

        prescription = completion.choices[0].message.content

        st.subheader("📄 Generated Prescription")

        st.markdown(prescription)

        # -------------------------
        # PDF GENERATION
        # -------------------------

        pdf_file = "prescription.pdf"

        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("<b>AI Medical Prescription</b>", styles['Title']))
        story.append(Spacer(1,20))

        patient_info = f"""
Patient Name: {name}<br/>
Age: {age}<br/>
Gender: {gender}<br/>
Weight: {weight} kg<br/>
Allergies: {allergies}<br/><br/>
"""

        story.append(Paragraph(patient_info, styles['Normal']))
        story.append(Paragraph(prescription.replace("\n","<br/>"), styles['Normal']))

        pdf = SimpleDocTemplate(pdf_file)
        pdf.build(story)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download Prescription PDF",
                data=f,
                file_name="medical_prescription.pdf",
                mime="application/pdf"
            )

        # -------------------------
        # AI VOICE OUTPUT
        # -------------------------

        tts = gTTS(text=prescription, lang="en")

        audio_file = "prescription_audio.mp3"
        tts.save(audio_file)

        st.subheader("🔊 AI Voice Prescription")
        st.audio(audio_file)

        # remove temp files later
        if os.path.exists(audio_file):

            pass
