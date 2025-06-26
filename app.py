from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from googletrans import Translator
import os

# Set your API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Enhanced Transcript helper with manual CC support
def get_transcript(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]

    # Step 1: Get transcript in any available language
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = next(iter(transcript_list))
    fetched = transcript.fetch()
    original_text = " ".join([chunk.text for chunk in fetched])

    # Step 2: Translate to English
    translator = Translator()
    max_len = 4500
    chunks = [original_text[i:i + max_len] for i in range(0, len(original_text), max_len)]

    translated_chunks = []
    for chunk in chunks:
        translated = translator.translate(chunk, dest='en')
        translated_chunks.append(translated.text)

    translated_text = " ".join(translated_chunks)
    return translated_text


# Initialize embeddings + model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
qa_chain = load_qa_chain(llm, chain_type="stuff")

# API route with improved error handling
@app.route("/ask", methods=["POST"])
def ask_doubt():
    data = request.json
    video_url = data.get("video_url")
    question = data.get("doubt")

    try:
        text = get_transcript(video_url)
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents([Document(page_content=text)])
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever()
        relevant_docs = retriever.get_relevant_documents(question)
        answer = qa_chain.run(input_documents=relevant_docs, question=question)
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "solution": "Something went wrong while processing the transcript.",
            "hint": "Make sure the video has subtitles enabled or is not restricted."
        }), 400

#  Run app
if __name__ == "__main__":
    app.run(debug=True)