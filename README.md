# BABOK Requirements Classifier

A RAG app that classifies unstructured requirements into BABOK categories, grounded in real BABOK guide content rather than the model's general knowledge.

## How it works

- BABOK guide content is chunked and stored in a Chroma vector database
- On input, the app retrieves the most relevant BABOK content for that requirement
- Gemini uses the retrieved context to classify the requirement
- Non-requirement input returns a "Not a requirement" result instead of a forced classification
- Interface built with Streamlit

## Tech stack

Python, ChromaDB, Google Gemini API, Streamlit

## Screenshots

![Requirement classified as Solution - Functional]
<img width="1902" height="895" alt="Screenshot 2026-08-28 220459" src="https://github.com/user-attachments/assets/b2088e9e-c19e-4524-a499-a4a4eae0fa7e" />
![Requirement classified as Stakeholder]
<img width="1888" height="882" alt="Screenshot 2026-08-28 220817" src="https://github.com/user-attachments/assets/98085885-9b30-4487-92ad-a9518da36959" />


## Notes

Preceded by a smaller practice RAG build using manual cosine similarity with no vector database, used to understand the underlying mechanics first. This is the full version, built with ChromaDB and a styled interface.
