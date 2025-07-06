
import langchain
import groq
import langchain_groq
import langchain_openai
import chromadb
import streamlit
import PyPDF2
import dotenv
import sentence_transformers
import os
import langchain_community
import openai
import tiktoken
import langchain_chroma
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
embedding_api_key=os.getenv("OPENAI_API_KEY")
hf_api_key=os.getenv("HF_API_KEY")
pdf_path = r"/Users/tasmiyataj/Downloads/CS_HDC_2 - Copy/docs/Heart-Disease-Classifications-and-Subclasses.pdf"
if os.path.exists(pdf_path):
    print(f"PDF file found at {pdf_path}")
else:
    print(f"PDF file not found at {pdf_path}")
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma 
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
def load_pdf_with_pypdf2(file_path):
    loader = PdfReader(file_path)
    documents = []
    for page_num, page in enumerate(loader.pages):
        text = page.extract_text()
        if text:
            doc = Document(page_content=text, metadata={"page": page_num})
            documents.append(doc)
    return documents
documents=load_pdf_with_pypdf2(pdf_path)
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=768, chunk_overlap=256)
documents = text_splitter.split_documents(documents)
documents
def remove_newlines(documents):
    for doc in documents:
        doc.page_content = doc.page_content.replace('\n', '')
    return documents
documents = remove_newlines(documents)
documents 

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.docstore.document import Document
batch = [Document(page_content="This is a test document."), Document(page_content="Another document.")]

embedding_model_hf = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma.from_documents(batch, embedding=embedding_model_hf, persist_directory="chroma")

from langchain_groq import ChatGroq

llm = ChatGroq(api_key=api_key, 
               model_name="llama-3.3-70b-versatile", 
               temperature=0.2)
from langchain.chains import RetrievalQA

retriever = db.as_retriever(search_type="similarity",
                            search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
) 
query = input("Enter your query: ")
print("Query:", query)
result = qa_chain.invoke({"query": query})
print("Answer:", result["result"])
               
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import sys

app = Flask(__name__)

# ✅ Try to load the model if available
try:
    model = joblib.load("heart_model.pkl")
    use_model = True
except FileNotFoundError:
    print("Model file not found. Using mock prediction.")
    model = None
    use_model = False

@app.route('/')
def home():
    return render_template('chatbot.html')  # Looks inside the /templates folder

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        symptoms = list(map(float, data['symptoms'].split(',')))
        if use_model:
            prediction = model.predict([symptoms])
            return jsonify({'result': str(prediction[0])})
        else:
            return jsonify({'result': 'Mock prediction: No model loaded'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ✅ Prevent crash in Jupyter
if __name__ == '__main__' and not hasattr(sys, 'ps1'):
    app.run(debug=True)


