import os
import streamlit as st
from dotenv import load_dotenv

from pdf_utils import extract_pdf_text, create_question_pdf
from generator import analyze_syllabus, generate_questions, validate_questions

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()

# ---------------------------------------------------------
# PREMIUM NAVY + WHITE THEME
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #102A43;
    --navy-deep: #071B33;
    --navy-mid: #173F67;
    --royal: #245B91;
    --accent: #55A6D9;
    --page: #F3F6FA;
    --surface: #FFFFFF;
    --text: #142B43;
    --muted: #66788A;
    --border: #DCE5EF;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--page);
    color: var(--text);
}

/* Main content alignment */
.block-container {
    max-width: 1440px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071B33 0%, #12395F 100%);
    border-right: 1px solid rgba(255,255,255,0.10);
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #D8E5F2 !important;
}
[data-testid="stSidebar"] .stAlert {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.20);
}

/* Hero banner */
.hero {
    background: linear-gradient(115deg, #071B33 0%, #12395F 58%, #245B91 100%);
    padding: 34px 38px;
    border-radius: 20px;
    margin-bottom: 26px;
    box-shadow: 0 12px 30px rgba(7,27,51,0.16);
    border: 1px solid rgba(255,255,255,0.10);
}
.hero-kicker {
    color: #9CC9EA;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(1.7rem, 3vw, 2.45rem);
    line-height: 1.2;
    font-weight: 800;
    margin: 0 0 10px 0;
}
.hero p {
    color: #E2ECF5 !important;
    font-size: 1rem;
    margin: 0;
    max-width: 850px;
    line-height: 1.65;
}

/* Headings */
h1, h2, h3, h4, p, label, .stMarkdown {
    color: var(--text);
}
h2 {
    font-weight: 800 !important;
    letter-spacing: -0.4px;
}
h3 {
    font-weight: 700 !important;
}
.section-heading {
    color: var(--navy);
    font-size: 1.25rem;
    font-weight: 800;
    margin: 1.7rem 0 0.25rem 0;
}
.section-subtitle {
    color: var(--muted);
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* Containers and cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 5px 18px rgba(16,42,67,0.045);
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-left: 4px solid var(--royal);
    border-radius: 13px;
    padding: 16px 18px;
}
div[data-testid="stMetric"] label {
    color: var(--muted) !important;
    font-weight: 600;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-weight: 800;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    background: #FFFFFF !important;
    color: #102A43 !important;
    border: 1px solid #C9D6E3 !important;
    border-radius: 10px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus,
.stNumberInput input:focus {
    border: 1px solid #245B91 !important;
    box-shadow: 0 0 0 2px rgba(36,91,145,0.12) !important;
}
.stSelectbox [data-baseweb="select"] > div,
.stMultiSelect [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #102A43 !important;
    border-radius: 10px !important;
    border-color: #C9D6E3 !important;
}
[data-testid="stFileUploader"] {
    background: #F8FAFD;
    border: 1.5px dashed #8FA9C2;
    border-radius: 13px;
    padding: 12px;
}
[data-testid="stFileUploader"] * {
    color: #173F67 !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(110deg, #102A43, #245B91) !important;
    color: #FFFFFF !important;
    border: 1px solid #245B91 !important;
    border-radius: 10px !important;
    min-height: 43px;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #071B33 !important;
    border-color: #071B33 !important;
    box-shadow: 0 5px 14px rgba(16,42,67,0.18);
    transform: translateY(-1px);
}
.stButton > button p, .stDownloadButton > button p {
    color: #FFFFFF !important;
}

/* Tabs, expanders and alerts */
[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    color: var(--navy) !important;
    font-weight: 700;
}
.stAlert {
    border-radius: 12px;
}
hr {
    border-color: #DCE5EF;
}

/* Captions and helper text */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #66788A !important;
}

/* -----------------------------------------------------
   FIX: FILE UPLOADER + INFO MESSAGE CONTRAST
   ----------------------------------------------------- */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1px solid #D5E1ED !important;
    border-radius: 14px !important;
    padding: 14px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: #F7FAFE !important;
    border: 1.5px dashed #8EABC7 !important;
    border-radius: 11px !important;
}
[data-testid="stFileUploaderDropzone"] > div {
    background: transparent !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: #173F67 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: #173F67 !important;
    color: #FFFFFF !important;
    border: 1px solid #173F67 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploaderDropzone"] button * {
    color: #FFFFFF !important;
}
[data-testid="stFileUploader"] small {
    color: #52677D !important;
}

/* Streamlit info boxes: pale blue surface + readable navy text */
[data-testid="stAlert"] {
    background: #EAF2FA !important;
    border: 1px solid #C7D9EA !important;
    border-left: 4px solid #245B91 !important;
    border-radius: 11px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div,
[data-testid="stAlert"] label {
    color: #102A43 !important;
}
[data-testid="stAlert"] svg {
    color: #245B91 !important;
    fill: #245B91 !important;
}

/* Keep sidebar alerts consistent with the dark sidebar theme. */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(7, 27, 51, 0.72) !important;
    border: 1px solid rgba(255, 255, 255, 0.24) !important;
    border-left: 4px solid #55A6D9 !important;
}
[data-testid="stSidebar"] [data-testid="stAlertContainer"] {
    background: #173F67 !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] [data-testid="stAlert"] svg {
    color: #9CC9EA !important;
    fill: #9CC9EA !important;
}

/* Keep disabled/helper text readable */
.stTextArea textarea:disabled {
    color: #52677D !important;
    -webkit-text-fill-color: #52677D !important;
    opacity: 1 !important;
}

/* Responsive layout */
@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero {
        padding: 25px 22px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
defaults = {
    "syllabus_text": "",
    "analysis": None,
    "questions": [],
    "paper_settings": {},
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
QUESTION_TYPES = ["MCQ", "Short Answer", "Long Answer", "Case Study"]

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">INDALA COLLEGE • ACADEMIC ASSESSMENT</div>
    <h1>AI-Powered Question Paper Generator</h1>
    <p>Build structured, syllabus-aligned assessments with Bloom's Taxonomy,
    configurable marks distribution, editable questions and downloadable PDF output.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 📝 Assessment Studio")
    st.markdown("---")
    st.markdown("### About this application")
    st.write(
        "Upload a syllabus PDF, analyze its units and topics, configure an "
        "examination, and generate an editable question paper."
    )
    st.markdown("---")
    st.markdown("### Workflow")
    st.markdown(
        "1. Upload syllabus PDF\n\n"
        "2. Extract syllabus content\n\n"
        "3. Analyze units and topics\n\n"
        "4. Configure question paper\n\n"
        "5. Generate and edit questions\n\n"
        "6. Export PDF"
    )
    st.info(
        "Faculty should review all AI-generated questions and answer keys "
        "before using them in an actual examination."
    )

# ---------------------------------------------------------
# API KEY CHECK
# ---------------------------------------------------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file and restart the app.")
    st.code("GROQ_API_KEY=your_groq_api_key_here")
    st.stop()

# ---------------------------------------------------------
# 1. UPLOAD SYLLABUS
# ---------------------------------------------------------
st.markdown('<div class="section-heading">01 · Upload syllabus</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Start by uploading the subject syllabus in PDF format.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    uploaded = st.file_uploader("Choose a syllabus PDF", type=["pdf"])

    if uploaded:
        st.success(f"Selected file: {uploaded.name}")
        if st.button("📄 Extract syllabus text", type="primary"):
            with st.spinner("Reading and extracting PDF content..."):
                try:
                    extracted_text = extract_pdf_text(uploaded)
                    if extracted_text and extracted_text.strip():
                        st.session_state.syllabus_text = extracted_text
                        st.session_state.analysis = None
                        st.session_state.questions = []
                        st.session_state.paper_settings = {}
                        st.success(f"Successfully extracted {len(extracted_text):,} characters.")
                    else:
                        st.error(
                            "No text was extracted. If this is a scanned PDF, "
                            "install Tesseract OCR and follow the README instructions."
                        )
                except Exception as exc:
                    st.error(f"PDF extraction failed: {exc}")

    if st.session_state.syllabus_text:
        st.text_area(
            "Extracted syllabus content",
            st.session_state.syllabus_text,
            height=190,
            disabled=True,
        )
        st.download_button(
            "⬇️ Download extracted text",
            data=st.session_state.syllabus_text,
            file_name="extracted_syllabus.txt",
            mime="text/plain",
        )

# ---------------------------------------------------------
# 2. ANALYZE SYLLABUS
# ---------------------------------------------------------
if st.session_state.syllabus_text:
    st.markdown('<div class="section-heading">02 · Analyze syllabus</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Use AI to identify the subject, units, topics and learning outcomes.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        if st.button("🔍 Analyze syllabus with AI", type="primary"):
            try:
                with st.spinner("Identifying subject, units, topics and learning outcomes..."):
                    st.session_state.analysis = analyze_syllabus(
                        st.session_state.syllabus_text, api_key
                    )
                st.success("Syllabus analysis completed.")
            except Exception as exc:
                st.error(f"Syllabus analysis failed: {exc}")

    if st.session_state.analysis:
        analysis = st.session_state.analysis
        with st.container(border=True):
            st.subheader(f"Subject: {analysis.get('subject_name', 'Not identified')}")
            if analysis.get("description"):
                st.write(analysis["description"])

            units = analysis.get("units", [])
            if units:
                for unit_index, unit_data in enumerate(units):
                    with st.expander(
                        unit_data.get("unit_name", f"Unit {unit_index + 1}"),
                        expanded=(unit_index == 0),
                    ):
                        left, right = st.columns(2, gap="large")
                        with left:
                            st.markdown("**Topics**")
                            for topic in unit_data.get("topics", []):
                                st.write(f"• {topic}")
                        with right:
                            st.markdown("**Learning outcomes**")
                            for outcome in unit_data.get("learning_outcomes", []):
                                st.write(f"• {outcome}")
            else:
                st.info("No units were identified in the analysis result.")

# ---------------------------------------------------------
# 3. CONFIGURE QUESTION PAPER
# ---------------------------------------------------------
st.markdown('<div class="section-heading">03 · Configure question paper</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Choose the topic, difficulty, Bloom level and question distribution.</div>',
    unsafe_allow_html=True,
)

if not st.session_state.syllabus_text:
    st.info("Upload and extract a syllabus PDF to enable question generation.")
else:
    with st.container(border=True):
        left, right = st.columns(2, gap="large")

        with left:
            subject = st.text_input(
                "Subject name",
                value=(st.session_state.analysis or {}).get("subject_name", ""),
                placeholder="Enter subject name",
            )
            unit = st.text_input(
                "Unit or topic to assess",
                placeholder="Example: Unit 1 - Introduction to Machine Learning",
            )
            difficulty = st.selectbox("Difficulty level", ["Easy", "Medium", "Hard"])

        with right:
            bloom = st.selectbox("Bloom's Taxonomy level", BLOOM_LEVELS)
            duration = st.number_input(
                "Exam duration (minutes)",
                min_value=15,
                max_value=300,
                value=60,
                step=5,
            )

        st.markdown("#### Question distribution")
        st.caption("Set the number of questions and marks per question. Set a count to zero to skip a type.")

        defaults_by_type = {
            "MCQ": (5, 1),
            "Short Answer": (3, 2),
            "Long Answer": (2, 5),
            "Case Study": (0, 10),
        }

        section_configs = []
        question_columns = st.columns(4, gap="medium")

        for index, question_type in enumerate(QUESTION_TYPES):
            with question_columns[index]:
                st.markdown(f"**{question_type}**")
                count = st.number_input(
                    "Number",
                    min_value=0,
                    max_value=20,
                    value=defaults_by_type[question_type][0],
                    key=f"count_{question_type}",
                )
                marks = st.number_input(
                    "Marks each",
                    min_value=1,
                    max_value=50,
                    value=defaults_by_type[question_type][1],
                    key=f"marks_{question_type}",
                )
                if count:
                    section_configs.append({
                        "type": question_type,
                        "count": int(count),
                        "marks": int(marks),
                    })

        total_questions = sum(item["count"] for item in section_configs)
        total_marks = sum(item["count"] * item["marks"] for item in section_configs)

        st.markdown("---")
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Questions requested", total_questions)
        metric2.metric("Total marks", total_marks)
        metric3.metric("Duration", f"{duration} min")

        generate_clicked = st.button(
            "🚀 Generate question paper",
            type="primary",
            use_container_width=True,
        )

        if generate_clicked:
            if not subject.strip():
                st.error("Enter a subject name.")
            elif not unit.strip():
                st.error("Enter a unit or topic.")
            elif not section_configs:
                st.error("Choose at least one question type.")
            else:
                try:
                    with st.spinner("Generating questions. This may take a little time..."):
                        generated = generate_questions(
                            syllabus_text=st.session_state.syllabus_text,
                            subject=subject.strip(),
                            unit=unit.strip(),
                            difficulty=difficulty,
                            bloom_level=bloom,
                            sections=section_configs,
                            api_key=api_key,
                        )

                    errors, actual_marks = validate_questions(generated, section_configs)

                    if errors:
                        st.session_state.questions = []
                        st.error("The generated paper did not pass validation:")
                        for error in errors:
                            st.write(f"• {error}")
                        st.caption("Try generating again or reduce the number of questions.")
                    else:
                        st.session_state.questions = generated
                        st.session_state.paper_settings = {
                            "subject": subject.strip(),
                            "duration": int(duration),
                            "total_marks": actual_marks,
                            "difficulty": difficulty,
                            "bloom_level": bloom,
                            "unit": unit.strip(),
                        }
                        st.success("Question paper generated and basic structure validated.")

                except Exception as exc:
                    st.error(f"Generation failed: {exc}")

# ---------------------------------------------------------
# 4. REVIEW AND EDIT QUESTIONS
# ---------------------------------------------------------
if st.session_state.questions:
    st.markdown('<div class="section-heading">04 · Review and edit questions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Review generated questions and edit the wording, options and model answers.</div>',
        unsafe_allow_html=True,
    )

    questions = st.session_state.questions

    for i, question in enumerate(questions):
        label = (
            f"Q{i + 1} · {question.get('question_type', 'Question')} · "
            f"{question.get('marks', 0)} marks"
        )

        with st.expander(label, expanded=(i == 0)):
            question["question"] = st.text_area(
                "Question",
                question.get("question", ""),
                key=f"q_text_{i}",
            )
            st.caption(
                f"Bloom's level: {question.get('bloom_level', '')}  |  "
                f"Difficulty: {question.get('difficulty', '')}"
            )

            if question.get("question_type") == "MCQ":
                options = list(question.get("options") or [])
                options = (options + ["", "", "", ""])[:4]

                option_cols = st.columns(2, gap="medium")
                for j in range(4):
                    with option_cols[j % 2]:
                        options[j] = st.text_input(
                            f"Option {chr(65 + j)}",
                            options[j],
                            key=f"q_{i}_opt_{j}",
                        )
                question["options"] = options

                answer = question.get("correct_answer", "A")
                question["correct_answer"] = st.selectbox(
                    "Correct option",
                    ["A", "B", "C", "D"],
                    index=["A", "B", "C", "D"].index(answer)
                    if answer in ["A", "B", "C", "D"] else 0,
                    key=f"q_{i}_answer",
                )
                question["explanation"] = st.text_area(
                    "Explanation",
                    question.get("explanation", ""),
                    key=f"q_{i}_explanation",
                )
            else:
                question["model_answer"] = st.text_area(
                    "Model answer / marking guidance",
                    question.get("model_answer", ""),
                    key=f"q_{i}_model",
                )

    # -----------------------------------------------------
    # 5. ANSWER KEY
    # -----------------------------------------------------
    st.markdown('<div class="section-heading">05 · Answer key</div>', unsafe_allow_html=True)

    if st.checkbox("Show answer key on screen"):
        with st.container(border=True):
            for i, question in enumerate(questions):
                st.markdown(f"**Q{i + 1}. {question.get('question', '')}**")
                if question.get("question_type") == "MCQ":
                    st.success(f"Correct answer: {question.get('correct_answer', '')}")
                    st.write(question.get("explanation", ""))
                else:
                    st.write(question.get("model_answer", ""))
                if i < len(questions) - 1:
                    st.divider()

    # -----------------------------------------------------
    # 6. EXPORT PDF
    # -----------------------------------------------------
    st.markdown('<div class="section-heading">06 · Export PDF</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Create a downloadable question paper with optional answer key.</div>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        include_answers = st.checkbox(
            "Include answer key and model answers in this PDF",
            value=False,
        )
        settings = st.session_state.paper_settings

        try:
            pdf_bytes = create_question_pdf(
                subject=settings["subject"],
                questions=questions,
                duration=settings["duration"],
                total_marks=settings["total_marks"],
                include_answers=include_answers,
                unit=settings.get("unit", ""),
            )

            st.download_button(
                "📥 Download question paper PDF",
                data=pdf_bytes,
                file_name="AI_Question_Paper.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as exc:
            st.error(f"PDF creation failed: {exc}")

    if st.button("🗑️ Clear generated paper"):
        st.session_state.questions = []
        st.session_state.paper_settings = {}
        st.rerun()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding:12px 0 4px 0;">
        <div style="color:#173F67; font-weight:700;">AI-Powered Question Paper & Assessment Generator</div>
        <div style="color:#718096; font-size:0.8rem; margin-top:5px;">
            Academic assessment support • Review all AI-generated content before examination use.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
