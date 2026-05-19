# AI Risk Intelligence Flask App

A modern Flask + REST API web application using your trained `best_model_random_forest.pkl` model, PostgreSQL authentication, animated HTML/CSS/JS pages, snackbar notifications, and analysis history.

## Folder structure

```text
ai_analysis_app/
├── app.py
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── model_service.py
│   ├── models.py
│   └── routes.py
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   └── history.html
│   └── static/
│       ├── css/styles.css
│       └── js/
│           ├── app.js
│           ├── auth.js
│           ├── dashboard.js
│           └── history.js
└── model/
    └── best_model_random_forest.pkl
```

## Setup

1. Create the PostgreSQL database:

```sql
CREATE DATABASE ai_analysis_db;
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.example` and adjust credentials if needed:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
```

5. Run the app:

```bash
python app.py
```

Open `http://127.0.0.1:5000`.

## Optional PostgreSQL with Docker

```bash
docker compose up -d
python app.py
```

## REST API endpoints

- `POST /api/auth/signup` — create account
- `POST /api/auth/login` — login
- `POST /api/auth/logout` — logout
- `GET /api/features` — get model features
- `POST /api/analyze` — run model analysis and save history
- `GET /api/history` — list recent analysis
- `DELETE /api/history/<id>` — delete one history item

## Notes

- The app uses PostgreSQL through `DATABASE_URL`.
- Tables are created automatically on startup with `db.create_all()`.
- The model input fields were generated from the uploaded trained model feature names.
