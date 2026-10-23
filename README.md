# 🏐 Voley Management API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)

*A robust RESTful API designed to manage members, membership plans, discount structures, and attendance for sports academies.*

[Report Bug](https://github.com/your-username/your-repo/issues) · [Request Feature](https://github.com/your-username/your-repo/issues)

</div>

---

## 📌 Table of Contents
- [Overview](#-overview)
- [How to use](#-how-to-use)
- [Architecture](#-architecture-&-best-practices)
- [Tech Stack](#-tech-stack)
  
---

## 📖 Overview

This backend application handles the core business logic for a volleyball academy. It features secure JWT authentication with role-based access control, automated database migrations, and dynamic fee calculations with custom discount tiers.

---
## 🚀 How to use

For this application, you will to use the swagger (bc im a **NOT** Frontend dev **YET**). This one uses an RBAC system, so you'll
need to log in and take the Token to access protected Endpoints.

1. Navigate to the swagger UI: [Voleyball Swagger](https://volleyball-club-core-api.onrender.com/docs)
---

2. Found the Login endpoint in "Users" place (it's the first one bwt, so you **shouldn't** miss it)

<details>
<summary>Click to view Swagger Authorization screenshot</summary>
<br>
<kbd>
  <img width="374" height="110" alt="image" src="https://github.com/user-attachments/assets/dcdbdb13-bf86-4785-8f7f-28b8de65969d" />
</kbd>
</details>

---

3. Log in using one of the pre-configured test accounts depending on the role you want to test:

| Role | Email | Password |
| :--- | :--- | :--- |
| **ADMIN** | `god_user@gmail.com` | `Im_God` |
| **GESTOR** | `good_user@gmail.com` | `Im_Good` |

---

4. Copy the `access_token` from the response.

<kbd>
<img width="1304" height="113" alt="image" src="https://github.com/user-attachments/assets/5dd1c83d-a3aa-4e2b-a487-e9304fdf0694" />
</kbd>

---

5. Click the **Authorize** button (🔒) at the top right of the Swagger UI, paste the token, and save.
<div>
  <kbd>
  <img width="178" height="93" alt="image" src="https://github.com/user-attachments/assets/06c190e2-4ce4-4ae7-8d8a-ea80a27e0875" />
  </kbd>
</div>
<div>
  <kbd>
  <img width="649" height="267" alt="image" src="https://github.com/user-attachments/assets/b3487fdb-5073-4cf1-8a5f-27296cc412c8" />
  </kbd>
</div>

---

## 🏛️ Architecture & Best Practices

This project was built following scalable backend patterns to ensure clean separation of concerns, maintainability, and security:

* **📁 Modular Folder Structure:** Code is organized by domain responsibilities (`api/` for endpoints, `core/` for configuration/security, `db/` for sessions and models) to keep components decoupled and easy to test.
<img width="256" height="694" alt="image" src="https://github.com/user-attachments/assets/3660010c-8b3d-424c-9f5b-070954458b4e" />

> [!TIP]
> **Environment Variables (.env)** An .env file is used to securely isolate sensitive credentials, such as database connection strings, secret keys, and system settings.
---
* **🛡️ Role-Based Access Control (RBAC):** Implements fine-grained access permissions, restricting sensitive operations depending on the user role (e.g., `ADMIN` vs `GESTOR`).
<img width="1046" height="487" alt="image" src="https://github.com/user-attachments/assets/6a39f65a-59c5-45a1-b874-271b9c794718" />

> [!TIP]
> **Dynamic rol auth** I created an dynamic rol system in one single def to keep clear code
> <img width="653" height="265" alt="image" src="https://github.com/user-attachments/assets/2051e356-481f-4800-bda3-decf1143829c" />

---

* **📋 Strict Data Validation (Pydantic Schemas):** Input and output data are rigorously validated using Pydantic schemas, preventing invalid payloads from ever hitting the database layer.
<img width="387" height="287" alt="image" src="https://github.com/user-attachments/assets/239b8e4e-9399-4d57-b727-41ef77a5c7d6" />

---

* **🔗 Relational Database Modeling (SQLAlchemy):** Strong data integrity using SQLAlchemy ORM to handle complex relationships (foreign keys, constraints, and cascades) cleanly.
<img width="1258" height="485" alt="image" src="https://github.com/user-attachments/assets/7e9b3b3c-3aaf-4a54-b507-ea8cd6d82e95" />

---

* **🔄 Database Migrations (Alembic):** Version-controlled schema migrations ensuring that database modifications are fully reproducible across different environments.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | Core programming language |
| **Framework** | FastAPI | High-performance asynchronous API framework |
| **ORM & Migrations** | SQLAlchemy + Alembic | Object-Relational Mapping and database version control |
| **Database** | PostgreSQL (Neon) | Cloud-native serverless relational database |
| **Containerization** | Docker & Compose | Environment isolation and deployment packaging |
