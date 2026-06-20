# LERO Fleet Management API 🚚

A secured, production-grade REST API built with FastAPI and SQLAlchemy (SQLite) designed to manage commercial vehicle fleets, track driver registries, log trip metrics, and compute fuel efficiency analytics.

---

## 🚀 Key Features

* **Modular Clean Routing**: Structured architecture utilizing FastAPI `APIRouter`.
* **Relational Database Storage**: Live local data persistence inside SQLite managed by SQLAlchemy models.
* **Role-Based Access Control (RBAC)**: Distinct permissions separating Managers (full CRUD & analytics) from Drivers (trip logging only).
* **Advanced Analytics Engine**: Real-time programmatic math processing to calculate average fuel efficiency (L/100km).
* **Strict Input Validation**: Strong data integrity checks powered by Pydantic fields and validation constraints.
* **Search & Filters**: Case-insensitive filtering for vehicle manufacturers and numeric distance threshold limits.
* **Data Export Engine**: Manager-only capability to stream live database records into a downloadable CSV spreadsheet report.

---

## 🛠️ Project Structure

```text
lero-fleet-api/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── drivers.py
│   │   ├── trips.py
│   │   └── vehicles.py
│   ├── __init__.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── .gitignore
├── fleet.db
├── README.md
└── requirements.txt
```

---

## 💻 Getting Started

Follow these instructions to spin up the system within your local virtual environment layout.

### Prerequisites
* Python 3.10 or higher
* Git

### Installation & Activation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd lero-fleet-api
   ```

2. **Rebuild the virtual environment:**
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

Launch the Uvicorn ASGI loop with live hot-reloading:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once running, access the local system infrastructure at:
* **API Server Status Landing**: `http://localhost:8000`
* **Interactive Documentation Playground**: `http://localhost:8000/docs`

---

## 🔐 Authentication Tokens

To run or test restricted paths in the Swagger UI (`/docs`), click the green **"Authorize"** pad at the top right and enter one of these secret tokens in the `X-API-KEY` field:

* **Manager Token**: `LERO_MANAGER_SECRET_2026` *(Grants unrestricted database CRUD, filtering, analytics, and spreadsheet downloads)*
* **Driver Token**: `LERO_DRIVER_SECRET_2026` *(Grants basic data viewing and trip entry logging only)*

---

## 📡 API Endpoints Matrix (v1)

| Scope | Method | Endpoint Path | Access Level | Description |
| :--- | :--- | :--- | :--- | :--- |
| **System** | **GET** | `/` | Open Access | Verifies system health & status metrics |
| **Vehicles** | **POST** | `/api/v1/vehicles` | Managers Only | Registers a new unique vehicle |
| **Vehicles** | **GET** | `/api/v1/vehicles` | All Roles | Lists vehicles (Optional query parameter: `?make=`) |
| **Vehicles** | **PUT** | `/api/v1/vehicles/{id}` | Managers Only | Modifies core data records of an active vehicle |
| **Vehicles** | **DELETE**| `/api/v1/vehicles/{id}` | Managers Only | Deletes a vehicle from the active directory |
| **Vehicles** | **GET** | `/api/v1/vehicles/{id}/trips` | All Roles | Fetches all trips tied to that specific vehicle |
| **Vehicles** | **GET** | `/api/v1/vehicles/{id}/efficiency`| Managers Only | Programmatically processes fuel efficiency logs |
| **Drivers** | **POST** | `/api/v1/drivers` | Managers Only | Registers a new driver onto the platform roster |
| **Drivers** | **GET** | `/api/v1/drivers` | Managers Only | Fetches the complete secure master driver registry |
| **Trips** | **POST** | `/api/v1/trips` | All Roles | Validates and saves a fresh journey log metrics sheet |
| **Trips** | **GET** | `/api/v1/trips` | All Roles | Returns logged entries (Optional filter: `?min_distance=`) |
| **Trips** | **GET** | `/api/v1/trips/export/csv` | Managers Only | Streams a physical downloadable CSV file for Excel |

