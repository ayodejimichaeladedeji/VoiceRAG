VoiceRAG
# 🎙️ Voice & Text Assistant with RAG

This project enables users to upload documents and ask questions through **voice** or **text**. It leverages **Retrieval-Augmented Generation (RAG)** to provide intelligent, context-aware answers using vector similarity search and generative AI.

---

## 🧠 Key Features

- 📄 **Document Upload:** Supports PDF upload and parsing using `PyMuPDF`.
- 🎙️ **Voice & Text Input:** Users can ask questions by speaking or typing.
- 🧮 **Vector Search with Pinecone:** Extracted text is embedded and stored for similarity-based retrieval.
- 🤖 **RAG-powered Responses:** Uses Google’s Gemini API to generate answers using relevant chunks from uploaded documents.
- 🔊 **Speech Transcription:** Utilizes FasterWhisper to transcribe voice input to text.

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
#### 2️⃣ Configuration
Create a `.env` file in the root directory and add the following environment variables. Replace the placeholder values with your actual API keys and other configurations:

```env
PINECONE_API_KEY=your_pinecone_api_key
GEMINI_API_KEY=your_gemini_api_key
INDEX_NAME=your_index_name
```

### 3️⃣ Start The Streamlit Frontend
```bash
streamlit run Home.py
```

### 4️⃣ Start The FastAPI Server
```bash
uvicorn main:app --reload
```
