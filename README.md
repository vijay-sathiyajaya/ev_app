# WebAPI-IQ Project

This project contains a full-stack web application with separate frontend and backend folders.

## Project Structure

```
webapi-iq/
├── frontend/          # Vue 3 + Vite frontend application
│   ├── src/          # Source files
│   ├── package.json  # Node dependencies
│   └── vite.config.js
│
└── backend/          # Python Flask backend service
    ├── main.py      # Flask application
    ├── requirements.txt
    └── .env         # Environment variables
```

## Getting Started

### Frontend Setup (Vue 3)

```bash
cd frontend
npm install
npm run dev
```

This will start the development server at `http://localhost:3000`

### Backend Setup (Python)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python main.py
```

This will start the Flask server at `http://localhost:5000`

## API Endpoints

- `GET /api/health` - Check backend health status
- `GET /api/data` - Get sample data from backend
