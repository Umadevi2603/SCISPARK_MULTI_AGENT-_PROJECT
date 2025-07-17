# SCISPARK_MULTI_AGENT-_PROJECT
# SciSpark: Intelligent Research Paper Summarizer

SciSpark is a multi-agent system built using Python and Streamlit that automates the process of discovering, analyzing, and summarizing academic research papers. Users simply input a topic, and the system handles everything from retrieving relevant PDF files to displaying and exporting concise summaries.

## Project Overview

In academic and research environments, finding and understanding relevant papers can be time-consuming. SciSpark streamlines this process using a set of intelligent agents:

- Search Agent: Fetches research paper links (PDFs) related to the user's topic.
- Validation Agent: Validates and downloads the first accessible and relevant PDF.
- Summarization Agent: Extracts key text from the PDF and summarizes it.
- Presentation Agent: Displays the summary and provides a PDF download option.
- Feedback Agent: Allows users to request another research paper if not satisfied with the initial one.

## Features

- Topic-based search for academic PDFs using Google Search
- Automated validation and selection of research papers
- Extraction and summarization of up to 3000 characters
- Display of the summary text and embedded PDF viewer
- Option to download the summary as a PDF file
- Ability to search for another research paper if the result is unsatisfactory
- Simple and clean black user interface

- Requirements
1. Python 3.8 or higher

2. streamlit

3. googlesearch-python

4. requests

5. PyMuPDF (fitz)

6. reportlab

