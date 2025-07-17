import streamlit as st
import fitz  # PyMuPDF
import ollama

# ---- Config ----
st.set_page_config(page_title="SciSpark - Research Assistant", layout="wide")
st.title("🔬 SciSpark | AI-powered Research Paper Assistant")
st.markdown("Upload a research paper and get summaries, key ideas, and new project inspiration using LLMs.")

# ---- Conversation State ----
if "convo" not in st.session_state:
    st.session_state.convo = []

# ---- LLM Chat Function ----
def query_llm(task_name, content):
    prompt = (
        f"You are an academic assistant. A user uploaded a research paper. Your task is to **{task_name}**.\n"
        f"Paper Content:\n{content[:4000]}"
    )
    st.session_state.convo.append({"role": "user", "content": prompt})

    full_response = ""
    stream = ollama.chat(model="llama3.2", messages=st.session_state.convo, stream=True)
    for chunk in stream:
        full_response += chunk["message"]["content"]

    st.session_state.convo.append({"role": "assistant", "content": full_response})
    return full_response

# ---- PDF Processing ----
def extract_pdf_text(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---- UI Layout ----
uploaded_file = st.file_uploader("📄 Upload a Research PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("📖 Reading and analyzing the PDF..."):
        full_text = extract_pdf_text(uploaded_file)

    st.success("✅ PDF content extracted!")

    # Sidebar Task Options
    st.sidebar.header("🛠️ Tasks")
    selected_tasks = st.sidebar.multiselect(
        "Select what you want the AI to do:",
        ["Summarize the Paper", "Extract Keywords", "Find Research Gaps", "Generate Project Ideas"],
        default=["Summarize the Paper"]
    )

    if st.sidebar.button("✨ Run AI"):
        for task in selected_tasks:
            with st.expander(f"🔍 {task}", expanded=True):
                result = query_llm(task_name=task, content=full_text)
                st.markdown(result)
else:
    st.info("📤 Please upload a research PDF to begin.")
