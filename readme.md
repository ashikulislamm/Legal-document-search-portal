# Legal Document Search Portal

A modern web application for searching and summarizing legal documents. Built with React (Frontend) and FastAPI (Backend), this application provides an intuitive interface for exploring legal concepts with instant summaries and relevant document snippets.

## 🎯 Features

- **Search Interface**: Clean, modern React UI with real-time search functionality
- **Document Summarization**: Automatically generates summaries based on search queries
- **Relevance Scoring**: Displays documents ranked by relevance to the search query
- **Snippet Highlighting**: Shows relevant text snippets from matching documents
- **Loading States**: Smooth loading indicators during API calls
- **Error Handling**: User-friendly error messages for failed requests
- **Responsive Design**: Modern UI built with Tailwind CSS

## 📁 Project Structure

```
Legal document search portal/
├── backend/
│   ├── requirements.txt          # Python dependencies
│   └── venv/
│       ├── app.py                # FastAPI application
│       └── docs/                 # Legal document files (.txt)
│           ├── doc1.txt
│           ├── doc2.txt
│           ├── doc3.txt
│           ├── doc4.txt
│           ├── doc5.txt
│           └── doc6.txt
│
└── frontend/
    ├── package.json              # Node.js dependencies
    ├── vite.config.js           # Vite configuration
    ├── tailwind.config.js       # Tailwind CSS configuration
    └── src/
        ├── main.jsx             # React entry point
        ├── App.jsx              # Main application component
        ├── lib/
        │   └── api.js           # API client
        └── components/
            ├── SearchBar.jsx   # Search input component
            ├── Results.jsx      # Search results display
            ├── SummaryPanel.jsx # Summary display component
            ├── Loader.jsx       # Loading indicator
            └── ErrorBanner.jsx  # Error message display
```

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **Git** (for cloning the repository)

## 📦 Installation & Setup

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (if not already created):
   ```bash
   # Windows
   python -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Upgrade pip (recommended) and install dependencies:**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Verify or create documents directory:**
   Ensure that the `backend/venv/docs/` directory contains `.txt` files with legal document content. The application will automatically load all `.txt` files from this directory.

   If the directory does not exist, create it:
   ```bash
   # macOS/Linux
   mkdir -p venv/docs
   ```
   ```powershell
   # Windows (PowerShell)
   New-Item -ItemType Directory -Force .\venv\docs | Out-Null
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   For CI environments (or to ensure a clean, lockfile-respecting install), use:
   ```bash
   npm ci
   ```

3. **Optional - Configure API URL:**
   Create a `.env` file in the `frontend` directory (if needed):
   ```env
   VITE_API=http://localhost:8000
   ```
   If not set, it defaults to `http://localhost:8000`.

## ▶️ Running the Application

### Start Backend Server

1. **Activate the virtual environment** (if not already activated):
   ```bash
   cd backend
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Navigate to the app directory and run:**
   ```bash
   cd venv
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend will be available at: `http://localhost:8000`

   You should see output like:
   ```
   ✓ Loaded 6 document(s) from ...
   API ready with 6 document(s) loaded.
   ```

### Start Frontend Development Server

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at: `http://localhost:5173` (or another port if 5173 is occupied)

3. **Open your browser** and navigate to the frontend URL shown in the terminal.

## 🔧 API Endpoints

### POST `/generate`

Generate search results and summary for a query.

**Request Body:**
```json
{
  "query": "contract breach"
}
```

**Response:**
```json
{
  "query": "contract breach",
  "results": [
    {
      "doc_id": "doc2",
      "title": "Contract Formation Guide",
      "score": 0.0125,
      "snippets": [
        "Breach of contract occurs when a party fails to perform their obligations...",
        "Material breaches substantially deprive the innocent party..."
      ]
    }
  ],
  "summary": "Breach of contract occurs when a party fails to perform their obligations as specified in the agreement...",
  "meta": {
    "took_ms": 15,
    "doc_count": 6
  }
}
```

### GET `/healthz`

Health check endpoint.

**Response:**
```json
{
  "ok": true,
  "docs": 6
}
```

### GET `/docs`

FastAPI automatic interactive API documentation (Swagger UI).

**Available at:** `http://localhost:8000/docs`

## 🎨 Usage

1. **Enter a search query** in the search bar (e.g., "negligence", "contract", "property law")
2. **Click "Search"** or press Enter
3. **View results:**
   - **Summary Panel**: Shows a generated summary based on your query
   - **Results List**: Displays matching documents with relevance scores and snippets

### Example Queries

- `contract`
- `negligence`
- `property ownership`
- `criminal procedure`
- `employment discrimination`
- `constitutional rights`

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python**: Programming language
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

### Frontend
- **React 19**: UI library
- **Vite**: Build tool and development server
- **Tailwind CSS 4**: Utility-first CSS framework
- **Axios**: HTTP client for API requests




## 🔒 Environment Variables

### Frontend

Create a `.env` file in the `frontend` directory:

```env
VITE_API=http://localhost:8000
```

