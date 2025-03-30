# 🛡️ CrewShift Backend

Fast. Secure. Scalable.  
Backend service for CrewShift — empowering secure and dynamic access to airline crew schedules.

![image](https://github.com/user-attachments/assets/f9292327-a8e1-4959-bc0c-f5ada06b7a14)

---

## 🚀 Tech Stack

- ⚡ **FastAPI** – blazing-fast Python API framework
- 🔥 **Firestore** – real-time NoSQL database by Google
- 🔐 **JWT Authentication** – secure and stateless login

---

## 🌐 Features

- 🔔 Email notifications for schedule access
- 🔐 API-only backend with OpenAPI docs

---

## 🛠️ Project Structure

app/  
├── api/  
├── core/  
├── crud/  
├── models/  
├── schemas/  
├── services/  
└── main.py

---

## How To Use It

You can just fork or clone this repository and spin up the backend instantly.

✨ It just works. ✨

---

## 🔧 Setup

```bash
cp .env.example .env
docker-compose up --build
Or run locally using:

bash
Copy
Edit
uvicorn app.main:app --reload
Configure your secrets and database in .env.

📦 Build & Deploy
bash
Copy
Edit
docker-compose up -d
Deployment options:

Railway

Render

DigitalOcean

Docker Compose (self-hosted)

🧪 Testing
Manual testing via /docs and /redoc has been prioritized.
Automated test coverage with Pytest to be included in the next release.

📄 License
The Backend API is licensed under the terms of the MIT license.
