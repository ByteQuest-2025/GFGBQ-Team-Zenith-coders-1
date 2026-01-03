cat > README.md << 'EOF'
# PS12: AI-Powered Grievance Redressal System

**Team Zenith Coders - ByteQuest 2025 Hackathon**

## Problem Statement
AI for Grievance Redressal in Public Governance - Automatically classify, prioritize, and route citizen complaints for faster resolution.

## Tech Stack
- Frontend: React (Vite) + Tailwind CSS
- Backend: FastAPI (Python)
- Database: MongoDB
- AI/NLP: scikit-learn + Transformers

## Project Structure
├── frontend/ # React app (Coder 1 + Coder 4)
├── backend/ # FastAPI server (Coder 2)
├── ai_service/ # NLP microservice (Coder 3)
└── docs/ # Documentation

## Setup Instructions

### Frontend
```bash
cd frontend
npm install
npm run dev
### Backend
bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
### ai service
cd ai_service
pip install -r requirements.txt
uvicorn app:app --reload --port 8001Team Members
Coder 1: Citizen UI

Coder 2: Backend API

Coder 3: AI/NLP Engine

Coder 4: Officer/Admin UI + Routing

Branch Strategy
main - Protected, always demo-ready

feature/citizen-ui - Coder 1

feature/backend-api - Coder 2

feature/ai-service - Coder 3

feature/officer-admin-ui - Coder 4
EOF


### Create .gitignore files

```bash
# Frontend .gitignore
cat > frontend/.gitignore << 'EOF'
node_modules/
dist/
.env
.env.local
*.log
EOF

# Backend .gitignore
cat > backend/.gitignore << 'EOF'
__pycache__/
*.pyc
.env
venv/
env/
uploads/
*.db
.pytest_cache/
EOF

# AI Service .gitignore
cat > ai_service/.gitignore << 'EOF'
__pycache__/
*.pyc
.env
venv/
env/
models/*.joblib
*.log
EOF

Create API Contract document
bash
cat > docs/API_CONTRACT.md << 'EOF'
# API Contract - PS12

**Base URLs:**
- Backend: `http://localhost:8000`
- AI Service: `http://localhost:8001`

## Authentication

### POST /auth/demo-login
**Request:**
```json
{
  "name": "Demo User",
  "role": "citizen|officer|admin"
}
Response:

json
{
  "token": "eyJ...",
  "user": {
    "id": "...",
    "name": "Demo User",
    "role": "citizen"
  }
}
Complaints (Citizen)
POST /complaints
Headers: Authorization: Bearer {token}
Body: multipart/form-data

title (required)

description (required)

address (optional)

latitude (optional)

longitude (optional)

image (optional file)

audio (optional file)

Response:

json
{
  "id": "...",
  "complaint_id": "COMP-2026-000123",
  "status": "SUBMITTED"
}
GET /complaints?mine=true
Response: Array of complaint summaries

GET /complaints/{id}
Response: Full complaint object (see schema below)

Officer Endpoints
GET /officer/inbox
Response: Array of assigned complaints

PATCH /complaints/{id}/status
Body:

json
{
  "status": "IN_PROGRESS|RESOLVED|REJECTED",
  "note": "Optional note"
}
Admin Endpoints
GET /admin/metrics
Response:

json
{
  "total": 150,
  "pending": 45,
  "resolved": 100,
  "avg_resolution_time": 1.5,
  "by_category": {...},
  "by_status": {...}
}
AI Service
POST /ai/triage
Request:

json
{
  "complaint_id": "COMP-2026-000123",
  "text": "Complaint text",
  "language": "auto"
}
Response:

json
{
  "category": "Utilities",
  "category_confidence": 0.86,
  "urgency_level": "MEDIUM",
  "urgency_score": 0.62,
  "keywords_detected": ["power", "outage"],
  "language_detected": "en"
}
Complaint Object Schema
json
{
  "id": "mongo_id",
  "complaint_id": "COMP-2026-000123",
  "title": "Streetlight not working",
  "description": "...",
  "category": "Utilities",
  "category_confidence": 0.86,
  "urgency_level": "MEDIUM",
  "urgency_score": 0.62,
  "status": "ASSIGNED",
  "assigned_department": "Electricity Board",
  "assigned_officer": {"name": "Officer Kumar"},
  "location": {
    "address": "...",
    "latitude": 0,
    "longitude": 0
  },
  "attachments": [
    {"type": "image", "url": "..."}
  ],
  "status_history": [
    {"status": "SUBMITTED", "timestamp": "...", "note": ""}
  ],
  "created_at": "2026-01-03T10:00:00Z"
}
EOF

text

### Create placeholder package files

```bash
# Frontend package.json
cat > frontend/package.json << 'EOF'
{
  "name": "ps12-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
EOF

# Backend requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
pymongo==4.6.1
motor==3.3.2
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
httpx==0.26.0
EOF

# AI Service requirements.txt
cat > ai_service/requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
scikit-learn==1.4.0
pandas==2.1.4
numpy==1.26.3
joblib==1.3.2
langdetect==1.0.9
textblob==0.17.1
python-dotenv==1.0.0
EOF