# Inquira: Intelligent YouTube Video Question Answering System

**Inquira** is a smart assistant that allows users to ask questions about the content of any YouTube video and receive relevant, context-aware answers powered by **LangChain** and **Google Gemini**.

It is designed to assist learners, researchers, and professionals who want to extract insights from video lectures, tutorials, or presentations without watching the entire content.

---

## Features

- **Multilingual Transcript Handling**: Supports videos with captions in any language and translates them to English using Google Translate.
- **Contextual Question Answering**: Leverages LangChain's QA system and Google Gemini for accurate, meaningful answers.
- **YouTube Integration**: Automatically extracts subtitles using `youtube-transcript-api`.
- **Chrome Extension Interface**: Includes a browser extension to interact directly with YouTube videos in a user-friendly manner.
- **Efficient Text Chunking & Retrieval**: Uses FAISS vector store to retrieve the most relevant transcript segments for any query.

---

## Tech Stack

| Component      | Technology                          |
|----------------|--------------------------------------|
| Backend        | Python, Flask, Flask-CORS            |
| NLP/QA Engine  | LangChain, Google Gemini             |
| Embeddings     | Google Generative AI Embeddings      |
| Transcript API | youtube-transcript-api               |
| Translation    | googletrans (Google Translate API)   |
| Vector Store   | FAISS                                |
| Extension UI   | HTML, CSS, JavaScript                |

---

## Getting Started

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahanya2726/inquira-youtube-assistant.git

   cd inquira-youtube-assistant
   ```
2. **Install dependencies**
    ```bash
    pip install -r requirement.txt
    ```
3.**Create a .env file and set your Google API key:**
   ```bash
   GOOGLE_API_KEY=your_google_genai_api_key
   ```
4.**Run the Flask server**
   ```bash
   python app.py
   ```

## 🔌 Chrome Extension Setup

To use the Inquira Chrome extension:

1. **Open Chrome** and go to:  

2. **Enable Developer Mode** by toggling the switch in the top-right corner.

3. Click **"Load unpacked"**.

4. Select the `youtube-helper-extension` folder from your cloned repository.

5. Once loaded, the extension icon will appear in the Chrome toolbar.

6. Navigate to **any YouTube video**, click the extension, type your question, and press **"Ask"**.

> The extension will automatically capture the video URL and fetch an answer from the Flask server running locally.

