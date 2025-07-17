import streamlit as st
from googlesearch import search
import requests
import fitz  # PyMuPDF
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import base64

# ---------- Search Agent ----------
def search_pdfs(topic):
    query = f"{topic} filetype:pdf"
    return [url for url in search(query, num_results=10) if url.endswith(".pdf")]

# ---------- Get First Valid PDF ----------
def get_valid_pdf(pdf_links, start_index=0):
    for i in range(start_index, len(pdf_links)):
        link = pdf_links[i]
        try:
            response = requests.get(link, timeout=20)
            if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(response.content)
                    return tmp_file.name, link, i
        except Exception:
            continue
    return None, None, None

# ---------- PDF Summarizer ----------
def summarize_pdf(pdf_path):
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
                if len(text) > 3000:
                    break
        return text[:3000]
    except Exception as e:
        raise RuntimeError(f"Failed to open or read the PDF: {e}")

# ---------- Create Summary PDF ----------
def create_pdf(text, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    x = 50
    y = height - 50
    for line in text.split('\n'):
        if y < 50:
            c.showPage()
            y = height - 50
        c.drawString(x, y, line[:110])
        y -= 15
    c.save()

# ---------- Streamlit UI ----------
st.set_page_config(page_title="SciSpark")
st.title("SciSpark: Research.Summarize.Ideate")

topic = st.text_input("🔍 Enter your research topic:")
next_pdf = st.button("🔁 Try another PDF")

if topic:
    if 'pdf_index' not in st.session_state or next_pdf:
        st.session_state.pdf_index = 0

    st.info("🔎 Searching and summarizing research papers...")
    pdf_links = search_pdfs(topic)

    if pdf_links:
        tmp_pdf_path, best_pdf_link, new_index = get_valid_pdf(pdf_links, start_index=st.session_state.pdf_index)

        if tmp_pdf_path:
            st.session_state.pdf_index = new_index + 1

            st.markdown(f"**PDF Selected:** [Click to View]({best_pdf_link})", unsafe_allow_html=True)
            try:
                summary = summarize_pdf(tmp_pdf_path)
                st.success("✅ Summary generated successfully!")

                st.subheader("Summary Preview:")
                st.write(summary)

                # Create summary PDF
                summary_pdf_path = os.path.join(tempfile.gettempdir(), "summary_output.pdf")
                create_pdf(summary, summary_pdf_path)

                # Read PDF as bytes for download
                with open(summary_pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                # Show download button
                st.download_button(
                    label="Download Summary PDF",
                    data=pdf_bytes,
                    file_name="summary.pdf",
                    mime="application/pdf"
                )

                # Also show PDF in iframe
                st.subheader("Summary PDF Viewer:")
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error summarizing PDF: {e}")
        else:
            st.error("No valid PDF found.")
    else:
        st.warning("No PDFs found. Try a more specific or academic topic.")
