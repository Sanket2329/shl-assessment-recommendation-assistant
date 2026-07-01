# 🎯 SHL Assessment Recommendation Assistant

An AI-powered SHL Assessment Recommendation System that recommends the most relevant SHL assessments based on job descriptions or hiring requirements.

The application combines semantic search using Sentence Transformers, Qdrant Vector Database, and Google's Gemini 2.5 Flash to provide intelligent, explainable, and grounded assessment recommendations.

---

# Features

- Semantic search over the complete SHL assessment catalog
- AI-powered recommendation explanations using Gemini 2.5 Flash
- Vector search with Qdrant
- FastAPI REST API
- Streamlit web application
- Assessment comparison
- Clarification for vague hiring requests
- Multi-turn conversation support
- Out-of-scope query handling
- Structured JSON responses

---

# Tech Stack

## Backend
- FastAPI
- Python 3.11

## AI
- Google Gemini 2.5 Flash
- Sentence Transformers (all-MiniLM-L6-v2)

## Vector Database
- Qdrant

## Frontend
- Streamlit

## Other
- Docker
- Pydantic
- Requests

---

# System Architecture

```
                User
                  │
                  ▼
           Streamlit UI
                  │
                  ▼
            FastAPI API
                  │
      ┌───────────┴────────────┐
      │                        │
      ▼                        ▼
Sentence Transformer      Qdrant Search
      │                        │
      └───────────┬────────────┘
                  ▼
         Top Matching Assessments
                  │
                  ▼
        Gemini 2.5 Flash Reasoning
                  │
                  ▼
      Structured Recommendation
                  │
                  ▼
             Streamlit UI
```

---

# Project Structure

```
shl-assignment/

├── app/
│   ├── api/
│   ├── services/
│   ├── schemas/
│   ├── data/
│   └── main.py
│
├── scripts/
│
├── tests/
│
├── streamlit_app/
│
├── requirements.txt
│
└── README.md
```

---

# Recommendation Pipeline

1. User submits a hiring requirement.
2. Sentence Transformer generates an embedding.
3. Qdrant performs semantic similarity search.
4. Top matching SHL assessments are retrieved.
5. Gemini receives:
   - User requirement
   - Conversation context
   - Retrieved assessments
6. Gemini explains why each assessment matches.
7. FastAPI returns structured recommendations.
8. Streamlit displays the results.

---

# Supported Features

## Assessment Recommendation

Example:

```
Looking for a Java Backend Developer with Spring Boot, REST APIs, SQL and strong problem-solving skills.
```

Returns:

- AI summary
- Recommended SHL assessments
- Match score
- Duration
- Remote support
- Assessment URL

---

## Assessment Comparison

Example:

```
Compare Java Frameworks (New) and Java 8 (New)
```

Returns:

- Key differences
- Best use cases
- Recommendation guidance

---

## Clarification

Example:

```
I need an assessment.
```

The assistant asks follow-up questions before recommending assessments.

---

## Out-of-Scope Detection

Example:

```
Who won the FIFA World Cup?
```

The assistant politely explains that it only supports SHL assessment recommendations.

---

# API Endpoints

## Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

## Chat

```
POST /chat
```

Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Looking for a Java Backend Developer."
    }
  ]
}
```

---

# Setup

## Clone

```bash
git clone <repository-url>
cd shl-assignment
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Start Qdrant

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

## Index SHL Catalog

```bash
python -m scripts.index_catalog
```

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

---

## Start Streamlit

```bash
streamlit run streamlit_app/app.py
```

---
# Evaluation Scenarios Tested

- Java Backend Developer
- Python Developer
- Sales Executive
- Graduate Hiring
- Assessment comparison
- Clarification flow
- Multi-turn refinement
- Out-of-scope queries

---

# Live Demo

Frontend

```
<Streamlit URL>
```

API

```
<FastAPI URL>
```

Health

```
<FastAPI URL>/health
```

Swagger

```
<FastAPI URL>/docs
```

---

# Example Screenshots

Add screenshots here after deployment.

- Home Page
- Recommendation Example
- Assessment Comparison
- Clarification Flow

---

# Future Improvements

- Hybrid semantic + keyword search
- Better assessment comparison using structured metadata
- Authentication
- Persistent chat history
- Cloud deployment
- Advanced ranking using rerankers

---

# Author

**Sanket Shakya**

B.Tech Artificial Intelligence & Data Science

Built for the **SHL GenAI Assessment Challenge**.