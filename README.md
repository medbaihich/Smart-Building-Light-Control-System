# 💡 Smart Building Light Control System

## 📌 Project Overview

**Control Lumiere** is a robust web-based application designed to manage and automate lighting systems in multi-floor buildings. It utilizes a **Django** backend for management and data persistence, combined with an **XML-RPC** server architecture to interface with hardware (GPIO) or simulation layers.

The system allows facility managers to define zones, assign lamps, schedule automatic toggling, and view energy consumption analytics, all guarded by a granular permission system.

## 🚀 Key Features

### 🏢 Zone & Hardware Management

* **Zone Hierarchies:** Organize lights by Building, Floor, and Zone.
* **Lamp Management:** Map physical lamps to GPIO pins.
* **State Tracking:** Real-time feedback on whether zones are ON or OFF.

### 👥 User & Access Control

* **Role-Based Access:** Granular permissions per user/zone (`can_view`, `can_control`, `can_schedule`).
* **Admin Dashboard:** Dedicated staff views to manage Users, Zones, and Permissions.

### 📅 Automation & Scheduling

* **Flexible Scheduling:** Set automatic turn-on/turn-off actions for specific days of the week.
* **Time Windows:** Define `start_time`, `end_time`, and validity periods (`valid_from`, `valid_until`).

### 📊 Analytics & Monitoring

* **Activity Logs:** Audit trail of all user actions (Source, Timestamp, Details).
* **Energy Dashboard:** Visualize energy consumption and usage frequency via integrated charts.
* **Simulation Mode:** A visual interface to test lighting logic without physical hardware.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **API:** Django REST Framework (DRF)
* **Hardware Communication:** XML-RPC Server (Standard Library)
* **Task Queue:** Celery (for executing Schedules)
* **Frontend:** HTML5, Bootstrap, JavaScript (Chart.js)
* **Database:** SQLite (Default) / PostgreSQL (Recommended for Prod)

## 📂 Project Structure

```text
control_lumiere/
├── api/                  # API Endpoints (DRF Serializers & Views)
├── control_lumiere/      # Project settings and configuration
├── core/                 # Main application logic
│   ├── models.py         # DB Schemas (Zone, Lamp, Schedule, Analytics)
│   ├── views.py          # Dashboard, Simulation, and Admin views
│   └── templates/        # HTML Templates
├── rpc/                  # Hardware Interface Layer
│   ├── server.py         # XML-RPC Server for GPIO control
│   └── client.py         # Client to communicate with the server
└── static/               # CSS, JS, and Assets

```

## ⚙️ Architecture

The system operates using a decoupled architecture:

1. **Django Web App:** Handles user interaction, database management, and scheduling logic.
2. **RPC Client:** When a user toggles a light, Django acts as a client sending a command.
3. **RPC Server (`rpc/server.py`):** Listens on `localhost:8001`. It receives commands and performs the actual hardware switching (or prints to console in simulation mode).

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/medbaihich/control_lumiere.git
cd control_lumiere

```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

### 3. Install Dependencies

```bash
pip install django djangorestframework celery redis
# Add other requirements if necessary

```

### 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate

```

### 5. Create Superuser

```bash
python manage.py createsuperuser

```

## 🏃‍♂️ Running the Application

To run the full system, you need to start the RPC server and the Django web server.

### Step 1: Start the Hardware/RPC Server

Open a terminal and run the RPC server (handles the "physical" light switching):

```bash
python rpc/management/commands/runrpcserver.py
# Or directly: python rpc/server.py

```

*Listens on port 8001.*

### Step 2: Start the Django Web Server

Open a second terminal:

```bash
python manage.py runserver

```

*Access the dashboard at `http://127.0.0.1:8000/dashboard`.*

### Step 3: Start Celery (Optional - For Schedules)

If you want the schedules to trigger automatically:

```bash
celery -A control_lumiere worker --loglevel=info
celery -A control_lumiere beat --loglevel=info

```

## 🔗 API Documentation

The system exposes RESTful endpoints for analytics and data integration.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/predictions/<zone_id>/` | Get schedule predictions for a specific zone. |
| `GET` | `/api/stats/frequency/` | Retrieve usage frequency metrics. |
| `GET` | `/api/stats/energy/` | Retrieve energy consumption data aggregated by date. |

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

**Developed by Mohamed BAIHICH**
