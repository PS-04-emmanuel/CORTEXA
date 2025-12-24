# CORTEXA: AI-Powered Business Feasibility Analyzer

**CORTEXA** is a modern SaaS platform designed to help entrepreneurs and consultants validate business ideas instantly using advanced AI. Leveraging the power of Google's **Gemini 2.0 Flash** model, it provides deep insights, pros/cons analysis, economic feasibility scores, and downloadable PDF reports.

![CORTEXA Banner](https://via.placeholder.com/1200x600?text=CORTEXA+Business+Feasibility+AI)

## 🚀 Key Features

*   **AI-Driven Analysis**: Instant evaluation of business concepts using Gemini 2.0 LLMs.
*   **Detailed Reports**: Generates comprehensive breakdown including Executive Summary, Pros & Cons, and Economic Analysis.
*   **Feasibility Scoring**: Assigns a concrete 0-100 score to gauge idea viability.
*   **PDF Exports**: Download professional, reformatted PDF reports for offline sharing (powered by ReportLab).
*   **Secure Authentication**: robust JWT-based Auth flow with Signup, Login, and specialized Onboarding.
*   **History & Management**: Save and review past reports.
*   **Modern UI**: Sleek, responsive interface built with React, Tailwind CSS, and Shadcn UI.

## 🛠️ Tech Stack

### Frontend
*   **React 18** (Vite)
*   **Tailwind CSS** (v4)
*   **Shadcn UI** (Radix Primitives)
*   **React Query** (TanStack)
*   **Axios** (API Communication)

### Backend
*   **FastAPI** (Python 3.12+)
*   **PostgreSQL** (Database)
*   **SQLAlchemy** (Async ORM)
*   **Alembic** (Migrations)
*   **Gemini 2.0 Flash** (AI Engine)
*   **Argon2** (Security/Hashing)
*   **ReportLab** (PDF Generation)

## 📦 Installation & Setup

### Prerequisites
*   Node.js & npm
*   Python 3.12+
*   PostgreSQL
*   Google Gemini API Key

### Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/cortexa.git
    cd cortexa
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Install dependencies
    pip install -r requirements.txt
    # Run Migrations
    alembic upgrade head
    # Start Server
    uvicorn app.main:app --reload
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Environment Variables**
    *   Create `.env` in `backend/` with `DATABASE_URL` and `GEMINI_API_KEY`.

## 🤝 Contribution
Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License
MIT License
