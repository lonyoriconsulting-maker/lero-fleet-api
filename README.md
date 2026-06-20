# LERO Fleet API 🚚

A lightweight, high-performance REST API built with FastAPI for managing commercial vehicle fleets, tracking drivers, and logging trip metrics.

---

## 🚀 Features

* **Vehicle Management**: Add, update, and track vehicles within the fleet.
* **FastAPI Performance**: Built on ASGI standards for rapid response times.
* **Auto-generated Documentation**: Fully interactive OpenAPI documentation included.

---

## 🛠️ Project Structure

```text
lero-fleet-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 💻 Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites
* Python 3.10 or higher
* Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd lero-fleet-api
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Running the Server

Start the application with Uvicorn using the following command:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once started, the API will be available at:
* **Local API Home**: `http://localhost:8000`
* **Interactive API Docs (Swagger UI)**: `http://localhost:8000/docs`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Health check / Welcome message |
| **GET** | `/vehicles` | Retrieve a list of all fleet vehicles |
| **POST** | `/vehicles` | Add a new vehicle to the registry |

