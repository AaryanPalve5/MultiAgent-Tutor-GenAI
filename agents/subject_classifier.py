# File: D:\Tutor-AI\agents\subject_classifier.py

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ─── Load your .env so GEMINI_API_KEY is available ───
load_dotenv()

# Read the key from the SAME environment variable you have in .env
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

llm = GoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "Classify the following question into one subject or the most relatable to  from this list: "
        "math, physics, chemistry, biology. "
        "Return exactly one of: 'math', 'physics', 'chemistry', 'biology', or 'unknown'. If the answer is 'unknown' try finding the closest subject and retry"
        "Do not explain or elaborate, just reply with the subject keyword.\n\n"
        "Question: {question}\nSubject:"
    ),
)

chain = LLMChain(llm=llm, prompt=prompt)

def classify_subject(question):
    result = chain.run(question=question)
    return result.strip().lower()
