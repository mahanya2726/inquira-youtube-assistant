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
import os

# ✅ Set your API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Initialize Flask
app = Flask(__name__)
CORS(app)  # <-- 🔥 This alone is enough

# ✅ Transcript helper
def get_transcript(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([entry["text"] for entry in transcript])

# ✅ Initialize embeddings + model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
qa_chain = load_qa_chain(llm, chain_type="stuff")

# ✅ API route
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
        return jsonify({"error": str(e)}), 500

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=True)
