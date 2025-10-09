# skut-notes
A **secure notes app** built with **Flask** and **JWT authentication**, with a full REST API, modular backend structure, and a responsive front-end interface.

---

## Features

- **JWT Auth** -- Register, log in, and ability to stay logged in using access & refresh tokens

- **CRUD Notes API** -- Create, read, update, and delete notes

- **Flask Blueprints** -- Organized modular routes (`auth`, `notes`)

- **SQLite Database** -- Persistent storage layer

- **Deployed on Render** -- Ready for live demo

---

## Tech Stack

| Layer | Technologies |
|-------|---------------|
| **Backend** | Flask · Flask-SQLAlchemy · Flask-JWT-Extended |
| **Frontend** | HTML · CSS (Flex/Grid Layout) · Vanilla JavaScript (Fetch API) |
| **Database** | SQLite |
| **Deployment** | Render |

## Project Overview

I created Skut Notes to be a lightweight full-stack web app to practice **secure authentication**, **data persistence**, and **frontend-backend integration** using Flask's ecosystem.

You can register a new account, log in, and manage personal notes securely -- each note can be created, edited, or deleted in real time.

The goal of the project was to learn and implement:
- Token-based auth flows (access + refresh)
- CRUD API design
- Separation of concerns using Blueprints
- Frontend/Backend data exchange with JSON

---

## Running Locally

```bash
# Clone the repo
git clone https://github.com/SkutM/skut-notes.git
cd skut-notes

# Set up virtual environment
python -m venv venv
venv\Scripts\activate # on Windows. otherwise, source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

Then open http://127.0.0.1:5000 in your browser!

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/register` | Create a new user |
| POST | `/api/login` | Authenticate a user, return JWT tokens |
| GET | `/api/notes` | Retrieve all notes (for logged-in user) |
| POST | `/api/notes` | Create a new note |
| PUT | `/api/notes/<id>` | Update an existing note |
| DELETE | `/api/notes/<id>` | Delete a note |

## Future Enhancements
- Dark/Light theme toggle (I'd like to make this, please return to this!)
- Etc., etc. (TBD)