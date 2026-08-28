import chromadb 
import os 
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))




with open("babok_requirements_kb.txt","r") as f:
    content=f.read()

chunks=[chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
print(f"Got {len(chunks)} chunks")
#for i, c in enumerate(chunks):
   # print(f"Chunk{i} ({len(c)} chars)")
   # print(c[:100],"...")

client=chromadb.Client()
collection = client.get_or_create_collection("babok_requirements")

collection.add(
    documents=chunks, 
    ids=[str(i) for i in range(len(chunks))]
)

print(f"Stored {collection.count()} chunks in Chroma")

def categorize_requirement(messy_input):
    results = collection.query(
        query_texts=[messy_input],
        n_results=2
    )
    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""You are a business analyst. Using ONLY the BABOK definitions below, categorize the following requirement into the correct type (Business, Stakeholder, Solution - Functional, Solution - Non-functional, or Transition). Give a one-line reason.
    If the input is not actually a requirement (e.g. it's a random question, unrelated text, or too vague to classify), say "Not a requirement" instead of forcing a category.

    BABOK definitions:
    {context}

    Requirement to categorize:
    "{messy_input}"

    Category:
    Reason:"""

    model = genai.GenerativeModel("gemini-flash-lite-latest")
    response = model.generate_content(prompt)
    return response.text


#test_input = "The system must respond to search queries within 2 seconds."
#result=categorize_requirement(test_input)
#print(result)

# = [
    "As a customer, I want to filter products by price so that I can find items within my budget.",
    "The company wants to reduce customer support costs by 20% this year.",
    "All new staff must complete data migration training before go-live.",
    "The app must be accessible for users with visual impairments, following WCAG guidelines."
#]

#for req in test_inputs:
   # print(f"Input: {req}")
   # print(categorize_requirement(req))
   # print("---")


st.set_page_config(page_title="BABOK Categorizer", layout="centered")

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
      html, body, [class*="css"], textarea, button, label, p, span, div {
          font-family: 'Courier Prime', 'Courier New', monospace !important;
      }
      .stApp { background: #f6f3ec; }
      .block-container { max-width: 720px; padding-top: 4.5rem; }
      .bb-brand { font-size: 12px; letter-spacing: .18em; text-transform: uppercase;
          color: #4a2a48; margin-bottom: 2rem; }
      .bb-label { font-size: 13px; font-weight: 700; letter-spacing: .12em;
          text-transform: uppercase; color: #2e1c2d; margin-bottom: .4rem; }
      textarea {
          background: #fdfdfb !important; color: #2e1c2d !important;
          border: 1.5px solid #4a2a48 !important; border-radius: 3px !important;
          font-size: 15px !important; line-height: 1.7 !important;
      }
      div.stButton > button {
          background: #a3e635; color: #232f0d; border: 1.5px solid #4a2a48;
          border-radius: 3px; padding: 12px 26px; font-size: 14px; font-weight: 700;
          letter-spacing: .14em; text-transform: uppercase; box-shadow: 3px 3px 0 #4a2a48;
      }
      div.stButton > button:hover { background: #b4ef52; }
      div.stButton > button:active { transform: translate(3px, 3px); box-shadow: none; }
      .bb-result {
          background: #4a2a48; color: #f2e9f1; border: 1.5px solid #4a2a48;
          border-radius: 3px; padding: 16px 18px; font-size: 15px; line-height: 1.7;
          min-height: 120px; white-space: pre-wrap;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="bb-brand">BABOK Requirement Categorizer</div>', unsafe_allow_html=True)
st.markdown('<div class="bb-label">Requirement</div>', unsafe_allow_html=True)

user_input = st.text_area("Requirement", placeholder="Paste a messy requirement here.", height=150, label_visibility="collapsed")

run = st.button("Categorize", disabled=not user_input.strip())

if run:
    st.session_state["result"] = categorize_requirement(user_input.strip())

result = st.session_state.get("result", "Result appears here.")

st.markdown('<div class="bb-label">Result</div>', unsafe_allow_html=True)
st.markdown(f'<div class="bb-result">{result}</div>', unsafe_allow_html=True)
#st.write("Paste a messy requirement below and see how it's categorized using BABOK's classification schema.")

#user_input = st.text_area("Requirement text")

#if st.button("Categorize"):
 #   if user_input.strip():
 #       with st.spinner("Categorizing..."):
 #           result = categorize_requirement(user_input)
 #       st.markdown(result)
 #   else:
 #       st.warning("Type something first.")