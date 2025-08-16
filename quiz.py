import streamlit as st

# Custom CSS for modern, readable UI
st.markdown("""
<style>
/* -------- GLOBAL -------- */
body, .stApp {
    font-family: 'Inter', 'Roboto', sans-serif !important;
    background: linear-gradient(135deg, #0f0f0f, #1a1a1a);
    color: #f5f5f5;
    overflow-x: hidden;
}

/* Smooth cinematic fade */
[data-testid="stVerticalBlock"] > div {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 2rem 1.8rem !important;
    margin-bottom: 2rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    backdrop-filter: blur(14px);
    animation: fadeUp 1.2s ease;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}
[data-testid="stVerticalBlock"] > div:hover {
    transform: translateY(-8px);
    box-shadow: 0 18px 60px rgba(0,0,0,0.55);
}

@keyframes fadeUp {
  from {opacity: 0; transform: translateY(30px);}
  to {opacity: 1; transform: translateY(0);}
}

/* -------- HEADINGS -------- */
h1, h2, h3, .stApp h1, .stApp h2, .stApp h3 {
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 0.6em;
    color: #ffffff;
    text-shadow: 0 0 18px rgba(0, 170, 255, 0.3);
}

/* -------- BUTTONS -------- */
.stButton>button {
    background: linear-gradient(90deg, #0d0d0d, #1f1f1f);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.8rem 1.6rem;
    font-size: 1.05rem;
    font-weight: 500;
    color: #f0f0f0 !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.stButton>button:hover {
    background: linear-gradient(90deg, #1f1f1f, #292929);
    border: 1px solid #00aaff;
    color: #00aaff !important;
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 30px rgba(0, 170, 255, 0.25);
}

/* -------- RADIO & SELECT -------- */
div[data-baseweb="radio"], div[data-baseweb="select"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px;
    padding: 0.6rem 0.9rem;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
}
div[data-baseweb="radio"]:hover, div[data-baseweb="select"]:hover {
    border: 1px solid #00aaff;
    box-shadow: 0 0 18px rgba(0,170,255,0.25);
}

/* -------- MERMAID FLOWCHART -------- */
.mermaid > svg {
    border-radius: 12px;
    background: rgba(0,0,0,0.4);
    box-shadow: 0 12px 30px rgba(0,0,0,0.5);
}
.mermaid .node rect {
    fill: rgba(255,255,255,0.05) !important;
    stroke: #00aaff !important;
}
.mermaid .edgePath path {
    stroke: #00aaff !important;
    stroke-width: 2px;
}

/* -------- MOBILE -------- */
@media (max-width: 700px) {
    h1, h2 { font-size: 1.4rem !important; }
    .stButton>button { width: 100% !important; font-size: 1rem !important; }
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Career Path Quiz",
    page_icon="🎯",
    layout="wide"
)


quiz_questions = [
    {
        "key": "age_range",
        "question": "What is your age range?",
        "options": ["Below 15", "15-18", "19-22", "23-30", "31-40", "41+"],
        "multi": False
    },
    {
        "key": "gender",
        "question": "What is your gender?",
        "options": ["Male", "Female", "Non-binary/Third gender", "Prefer not to say"],
        "multi": False
    },
    {
        "key": "education",
        "question": "What is your highest level of education?",
        "options": [
            "School (Up to Class 10)",
            "Higher Secondary (Class 12)",
            "Diploma",
            "Undergraduate Degree",
            "Postgraduate Degree",
            "Doctorate (PhD)",
            "Other/None"
        ],
        "multi": False
    },
    {
        "key": "subjects",
        "question": "Which subjects do you find most interesting?",
        "options": [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "Economics",
            "Business & Management",
            "History",
            "Political Science",
            "Psychology",
            "Sociology",
            "Philosophy",
            "Art & Design",
            "Music",
            "Sports/Physical Education",
            "Languages & Literature"
        ],
        "multi": True
    },
    {
        "key": "programming_language_known",
        "question": "Which programming languages do you know?",
        "options": [
            "Python",
            "C",
            "C++",
            "Java",
            "JavaScript",
            "TypeScript",
            "Ruby",
            "PHP",
            "Kotlin",
            "Swift",
            "R",
            "Go",
            "Rust",
            "SQL",
            "MATLAB",
            "Scala",
            "None"
        ],
        "multi": True
    },
    {
        "key": "career_interest",
        "question": "Which career fields interest you the most?",
        "options": [
            "Software Development",
            "Data Science / AI / ML",
            "Cybersecurity",
            "Cloud Computing / DevOps",
            "Web Development",
            "Mobile App Development",
            "Game Development",
            "Networking & IT Support",
            "Healthcare / Medicine",
            "Biotechnology",
            "Research & Academia",
            "Entrepreneurship / Startups",
            "Finance & Banking",
            "Marketing & Sales",
            "Government / Civil Services",
            "Design (UI/UX, Graphic, Fashion)",
            "Arts & Entertainment",
            "Sports & Fitness",
            "Law / Legal Studies",
            "Teaching & Education"
        ],
        "multi": True
    },
    {
        "key": "problem_solving",
        "question": "How do you prefer to solve problems?",
        "options": [
            "With a logical and analytical approach",
            "Through creative brainstorming",
            "By experimenting with trial and error",
            "By collaborating and asking for help",
            "By researching and learning independently"
        ],
        "multi": False
    },
    {
        "key": "communication_skills",
        "question": "How confident are you in your communication skills?",
        "options": [
            "Very confident",
            "Somewhat confident",
            "Neutral",
            "Not very confident",
            "Prefer not to say"
        ],
        "multi": False
    }
]



if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}


def next_question():
    """Save the answer and move to the next question."""
    q_key = quiz_questions[st.session_state.current_q]["key"]
    
    st.session_state.answers[q_key] = st.session_state[f"widget_{q_key}"]
    st.session_state.current_q += 1

def prev_question():
    """Go back to the previous question."""
    if st.session_state.current_q > 0:
        st.session_state.current_q -= 1

def restart_quiz():
    """Reset the quiz to the beginning."""
    st.session_state.current_q = 0
    st.session_state.answers = {}


def render_question():
    """Renders the current question, input widget, and navigation buttons."""
    q_data = quiz_questions[st.session_state.current_q]
    q_key = q_data["key"]
    
   
    stored_answer = st.session_state.answers.get(q_key, [] if q_data["multi"] else None)

    with st.container(border=True):
        
        progress_value = (st.session_state.current_q) / len(quiz_questions)
        st.progress(progress_value, text=f"Question {st.session_state.current_q + 1} of {len(quiz_questions)}")
        
        
        st.subheader(q_data["question"])

        
        if q_data["multi"]:
            st.multiselect(
                "Select all that apply:",
                q_data["options"],
                default=stored_answer,
                key=f"widget_{q_key}", 
                label_visibility="collapsed"
            )
        else:
           
            default_index = q_data["options"].index(stored_answer) if stored_answer in q_data["options"] else None
            st.radio(
                "Choose one:",
                q_data["options"],
                index=default_index,
                key=f"widget_{q_key}", 
                label_visibility="collapsed"
            )

        
        col1, col2, col3 = st.columns([2, 4, 2])
        with col1:
            st.button("⬅️\nBack", on_click=prev_question, disabled=(st.session_state.current_q == 0))
        with col3:
            st.button("Next\n➡️", on_click=next_question)

def render_results_summary():
    """Renders the final results and submission options."""
    st.success("✅ Quiz Complete!")
    st.balloons()
    
    st.header("Your Quiz Summary")

    for q_data in quiz_questions:
        q_key = q_data["key"]
        answer = st.session_state.answers.get(q_key)

        with st.expander(f"**{q_data['question']}**"):
            if answer:
               
                if isinstance(answer, list):
                    st.write(" &rarr; ".join(answer))
                else:
                    st.write(f"&rarr; {answer}")
            else:
                st.write("_Not answered_")

    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit and Find Your Career Path", type="primary", use_container_width=True):
            st.session_state["career_quiz"] = st.session_state.answers
            st.success("Results saved! Taking you to the Career Mentor...")
            
            st.switch_page("pages/assistant.py") 

    with col2:
        st.button("Restart Quiz 🔄", on_click=restart_quiz, use_container_width=True)



st.title("🎯 Career Path Quiz")
st.markdown("Answer these questions to help us understand you better and recommend a suitable career path.")


_, main_col, _ = st.columns([1, 2, 1])

with main_col:
    
    if st.session_state.current_q >= len(quiz_questions):
        render_results_summary()
    else:
        render_question()
        