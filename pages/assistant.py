import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from youtubesearchpython import VideosSearch
import re
from streamlit_mermaid import st_mermaid  # ✅ Direct rendering

# ----------------- LOAD & CONFIGURE -----------------
st.markdown("""
<style>
/* ---- GLOBAL APP BACKGROUND ---- */
body, .stApp {
    font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
    background: linear-gradient(135deg, #0d0d0f 0%, #1b2735 50%, #090a0f 100%);
    color: #e0e0e0 !important;
    letter-spacing: 0.4px;
}

/* ---- HEADINGS ---- */
h1, h2, h3, .stApp h1, .stApp h2, .stApp h3 {
    font-weight: 700;
    margin-bottom: 0.6em;
    color: #a8c7fa; /* Cinematic neon blue */
    text-shadow: 0px 0px 12px rgba(168,199,250,0.4);
    letter-spacing: 1px;
}

/* ---- CONTAINERS / BLOCKS ---- */
[data-testid="stVerticalBlock"] > div {
    background: rgba(20, 25, 35, 0.85);
    border-radius: 20px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.6), inset 0 0 40px rgba(63,94,251,0.05);
    padding: 2rem 1.5rem !important;
    margin-bottom: 2rem;
    animation: cinematic-fade 1s ease-in-out, zoom-in 1.2s ease;
}

@keyframes cinematic-fade {
  from {opacity: 0; transform: translateY(40px);}
  to {opacity: 1; transform: none;}
}
@keyframes zoom-in {
  from {transform: scale(0.95);}
  to {transform: scale(1);}
}

/* ---- PARAGRAPH / TEXT ---- */
.stMarkdown {
    font-size: 1rem;
    color: #cfd2d7 !important;
    margin-bottom: 1.2em;
}

/* ---- BUTTONS ---- */
button, .stButton>button {
    background: linear-gradient(90deg, #141E30 0%, #243B55 100%);
    color: #e0e0e0 !important;
    border: none !important;
    border-radius: 12px;
    padding: 0.8em 1.5em;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    margin: 0.6em 0;
    transition: all 0.35s ease-in-out;
    box-shadow: 0 0 12px rgba(0,0,0,0.6);
}
button:hover, .stButton>button:hover {
    background: linear-gradient(90deg, #3a0ca3, #4361ee, #4cc9f0);
    color: #ffffff !important;
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0px 0px 22px rgba(76,201,240,0.6), 0px 0px 42px rgba(67,97,238,0.4);
}

/* ---- INPUTS ---- */
div[data-baseweb="radio"], div[data-baseweb="select"] {
    background: rgba(30, 36, 50, 0.9) !important;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,.4);
    margin-bottom: 1.1em;
    animation: cinematic-fade 1s ease;
}
div[data-baseweb="radio"]:hover, div[data-baseweb="select"]:hover {
    box-shadow: 0 0 15px rgba(76,201,240,0.2);
    border: 1px solid #4cc9f0;
}

/* ---- ANSWER / CODE BLOCKS ---- */
[data-testid="stMarkdownContainer"] code, 
[data-testid="stMarkdownContainer"] pre {
    background: #121212;
    padding: 0.7em 1em;
    border-radius: 8px;
    font-size: 1.05em;
    color: #4cc9f0;
    box-shadow: inset 0 0 10px rgba(67,97,238,0.2);
}

/* ---- SUCCESS / ALERTS ---- */
.stAlert-success {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #a8c7fa !important;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.5);
}

/* ---- MERMAID DARK MODE ---- */
.mermaid > svg {
    border-radius: 12px;
    background: #0f1117 !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.6);
}
.mermaid .node rect, .mermaid .node circle, .mermaid .node ellipse {
    fill: #1a1d29 !important;
    stroke: #4cc9f0 !important;
}
.mermaid .edgePath path {
    stroke: #a8c7fa !important;
}

/* ---- RESPONSIVENESS ---- */
@media (max-width: 700px) {
    h1, h2, h3 { font-size: 1.25rem !important; }
    button, .stButton>button { width: 100% !important; font-size: 0.9rem; }
}
</style>
""", unsafe_allow_html=True)

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Career Chat", layout="wide")
st.title("🤖 Personalized Career Mentor")

# ----------------- VALIDATION -----------------
if "career_quiz" not in st.session_state:
    st.warning("⚠ Please complete the Career Path Quiz first.")
    st.stop()

# ----------------- HELPERS -----------------
def extract_mermaid_code(text):
    """Extracts Mermaid.js code block from LLM output."""
    match = re.search(r"```mermaid(.*?)```", text, re.DOTALL)
    if match:
        code = match.group(1).strip()
        return sanitize_mermaid_labels(code)
    return None

def sanitize_mermaid_labels(code):
    """
    Mermaid.js doesn't like certain characters (parentheses, commas, colons) unquoted.
    This function wraps labels in quotes if needed.
    """
    return re.sub(r"\[([^\]]+)\]", lambda m: f"[\"{m.group(1)}\"]", code)

# ----------------- USER PROFILE CONTEXT -----------------
quiz_context = "User quiz responses:\n"
for key, value in st.session_state.career_quiz.items():
    quiz_context += f"{key}: {value}\n"
quiz_context += "\nProvide personalized career advice."

# ----------------- CAREER RESOURCES -----------------
preferred_career = st.session_state.career_quiz.get("preferred_career", "").strip().lower()

roadmap_urls = {
    "frontend developer": "https://roadmap.sh/frontend",
    "backend developer": "https://roadmap.sh/backend",
    "devops engineer": "https://roadmap.sh/devops",
    "data scientist": "https://roadmap.sh/data-science",
    "machine learning engineer": "https://roadmap.sh/machine-learning",
}

preferred_skills = {
    "frontend developer": ["HTML", "CSS", "JavaScript", "React.js", "Redux", "Git", "Responsive Design"],
    "backend developer": ["Python", "Java", "Node.js", "Express", "SQL/NoSQL", "API Design", "Authentication"],
    "devops engineer": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS/Azure", "Monitoring", "Scripting"],
    "data scientist": ["Python", "Pandas", "Numpy", "ML", "Deep Learning", "Data Viz", "SQL"],
    "machine learning engineer": ["Python", "TensorFlow/PyTorch", "ML Algorithms", "Preprocessing", "Deployment"],
}

career_skills = preferred_skills.get(preferred_career, [])
roadmap_url = roadmap_urls.get(preferred_career)

# ----------------- LAYOUT -----------------
col1, col2 = st.columns([1, 2])

# ----------------- LEFT COLUMN -----------------
with col1:
    if preferred_career:
        st.markdown(f"### 🛤 Career Roadmap: **{preferred_career.title()}**")
        if roadmap_url:
            st.markdown(f"[🔗 View Full Roadmap]({roadmap_url})")
        else:
            st.info("No roadmap available for this career.")

        if career_skills:
            st.markdown("### 📌 Recommended Skills")
            for skill in career_skills:
                st.write(f"- {skill}")

        st.markdown(f"### 🎥 YouTube Resources for {preferred_career.title()}")
        try:
            videosSearch = VideosSearch(f"{preferred_career} roadmap skills", limit=3)
            results = videosSearch.result().get('result', [])
            if results:
                for video in results:
                    st.markdown(f"**[{video['title']}]({video['link']})**\n- {video['channel']['name']} | {video['duration']}")
            else:
                st.info("No videos found.")
        except Exception as e:
            st.error(f"Failed to fetch YouTube videos: {e}")

# ----------------- RIGHT COLUMN (CHAT) -----------------
with col2:
    st.markdown("### 💬 Career Q&A Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about career path, skills, or roadmap...")

    if prompt:
        full_prompt = (
            quiz_context +
            f"\nUser question: {prompt}\n\n"
            f"Please provide:\n"
            f"1. Top skills to focus on.\n"
            f"2. A personalized career roadmap summary.\n"
            f"3. 2-3 learning resources (YouTube links).\n"
            f"4. A **Mermaid.js flowchart** diagram enclosed in ```mermaid code block.\n"
            f"Example:\n```mermaid\nflowchart TD\nA[Start] --> B[Skills] --> C[Internship] --> D[Job]\n```"
        )

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(full_prompt)
                    bot_reply = response.text
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    st.markdown(bot_reply)

                    # ✅ Extract and render Mermaid diagram directly
                    mermaid_code = extract_mermaid_code(bot_reply)
                    if mermaid_code:
                        st.markdown("### 🧠 Career Roadmap Visualization")
                        st_mermaid(mermaid_code)  # Direct render
                    else:
                        st.info("No Mermaid diagram found in the response.")
        except Exception as e:
            st.error(f"Error: {e}")
