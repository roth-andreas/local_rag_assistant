# Local RAG Assistant

A local Retrieval-Augmented Generation (RAG) assistant powered by **Ollama (Llama 3)**, **Streamlit**, and **ChromaDB**. This application allows you to upload PDF documents and chat with them securely on your local machine.

## Features

- **100% Local**: Runs entirely on your machine using Ollama. No data leaves your computer.
- **RAG Architecture**: Ingests PDFs, creates embeddings using `FastEmbed`, and stores them in a local ChromaDB vector store.
- **Interactive Chat**: Streamlit interface for seamless document querying.

## Prerequisites

- **Python 3.10+**
- **Ollama**: [Download and install Ollama](https://ollama.com/)
- **Llama 3 Model**: Run `ollama pull llama3` in your terminal.

## Setup

### Option 1: Local Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd local_rag_assistant
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv_new
    # Windows:
    .\venv_new\Scripts\activate
    # Mac/Linux:
    source venv_new/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:
    ```bash
    streamlit run src/app.py
    ```

### Option 2: Docker (Recommended)

1.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This will start the application, ChromaDB, and Ollama.
    
    > **Note:** On the first run, the container will automatically download the `llama3` model (approx. 4.7 GB). This may take a few minutes. The application will wait until the download is complete before starting.

2.  **Access the App**:
    Open [http://localhost:8501](http://localhost:8501).

    *   Streamlit App: `http://localhost:8501`
    *   Ollama API (Optional): `http://localhost:11435`
    *   ChromaDB (Optional): `http://localhost:8000`

## Usage

1.  Open the app in your browser.
2.  Use the sidebar to upload a PDF file.
3.  Click **"Ingest Document"** to process the file.
4.  Start chatting with your document in the main chat window.

## License

MIT
