#  Azure Cloud-Based Document Management System

A secure, cloud-native **Document Management System** built using **Flask**, **Azure App Service**, **Azure SQL Database**, and **Azure Blob Storage**. The application allows users to securely upload, manage, download, version, and restore documents while maintaining complete audit logs. The project is deployed on Microsoft Azure with automated CI/CD using GitHub Actions.

---

#  Live Demo

**Application URL**

[https://YOUR-APP-NAME.azurewebsites.net](https://documentversionmanagement-ahgxhhfrarhdb3ff.centralindia-01.azurewebsites.net/)

---

#  Features

- User Registration
- Secure Login Authentication
- Password Hashing with Bcrypt
- Dashboard Analytics
- Upload Documents
- Download Documents
- Delete Documents
- Azure Blob Storage Integration
- Azure Blob Versioning
- Restore Previous Versions
- Audit Log Tracking
- Azure SQL Database
- Cloud Deployment
- GitHub Actions CI/CD

---

# Azure Services Used

| Service | Purpose |
|----------|----------|
| Azure App Service | Hosts the Flask Application |
| Azure SQL Database | Stores Users, Documents, Versions & Audit Logs |
| Azure Blob Storage | Stores Uploaded Documents |
| Azure Blob Versioning | Maintains Document Versions |
| Azure Deployment Center | GitHub Deployment |
| GitHub Actions | Continuous Deployment |

---

#  System Architecture

```text
                     User
                       │
                       ▼
             Azure App Service
               (Flask Backend)
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
 Azure SQL Database          Azure Blob Storage
(User Information)            (Document Storage)
```

---

#  Technology Stack

## Backend

- Python
- Flask
- SQLAlchemy
- Flask Login
- Flask Bcrypt
- Flask Migrate

## Frontend

- HTML5
- CSS3
- Bootstrap
- Jinja2

## Database

- Azure SQL Database

## Cloud

- Azure Blob Storage
- Azure App Service

## CI/CD

- GitHub Actions

---

#  Project Structure

```text
DocumentManagementSystem
│
├── app
│   ├── models
│   ├── routes
│   ├── services
│   ├── templates
│   ├── static
│   ├── utils
│   ├── extensions.py
│   └── config.py
│
├── migrations
├── screenshots
├── tests
├── requirements.txt
├── run.py
└── README.md
```

---

#  Modules

## Authentication

- User Registration
- Login
- Logout
- Password Encryption

---

## Dashboard

- Total Users
- Total Documents
- Total Versions
- Storage Usage
- Recent Uploads

---

## Document Management

- Upload Documents
- Download Documents
- Delete Documents
- Search Documents

---

## Version Management

- Automatic Version Creation
- Download Previous Versions
- Restore Previous Versions
- Version History

---

## Audit Logs

Tracks

- Upload
- Download
- Delete
- Restore

---

#  Security Features

- Password Hashing (Bcrypt)
- Environment Variables
- Azure SQL Secure Connection
- Azure Blob Storage
- Session Authentication

---

#  Screenshots

## Login

![Login](screenshots/login.png)

---

## Dashboard

![Dashboard](screenshots/dashboard.png)

---

## Documents

![Documents](screenshots/documents.png)

---

## Upload Document

![Upload](screenshots/upload.png)

---

## Version History

![Version History](screenshots/version-history.png)

---

## Audit Logs

![Audit Logs](screenshots/audit-logs.png)

---

## Azure Blob Storage

![Azure Blob Storage](screenshots/azure-blob-storage.png)

---

## Azure SQL Database

![Azure SQL Database](screenshots/azure-sql-database.png)

---

## Azure Dashboard

![Azure Dashboard](screenshots/azure-dashboard.png)

---

## Deployment Center

![Deployment Center](screenshots/deployment-center.png)

---

## SQL Metrics

![SQL Metrics](screenshots/sql-metrics.png)

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/Dhanushsj12/Azure-Document-Management-System.git
```

Navigate into the project

```bash
cd Azure-Document-Management-System
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
SECRET_KEY=

DATABASE_URL=

AZURE_STORAGE_CONNECTION_STRING=

AZURE_CONTAINER_NAME=
```

Run the application

```bash
flask run
```

---

# Future Improvements

- Role-Based Access Control
- AI Document Classification
- OCR Support
- Email Notifications
- Storage Analytics
- Multi-Factor Authentication

---

#  Author

**Dhanush S J**

Integrated M.Tech Software Engineering

Vellore Institute of Technology

GitHub

https://github.com/Dhanushsj12

LinkedIn

https://www.linkedin.com/in/dhanush-s-j-034147271

---

# License

This project is intended for educational and learning purposes.
