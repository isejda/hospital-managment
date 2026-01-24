# FastAPI ToDoApp Setup

## Prereqs
- Python 3.11+

## Install
From `C:\Users\User\Desktop\FastAPI`:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

If you use PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run migrations
From `C:\Users\User\Desktop\FastAPI\ToDoApp`:

```bash
python -m alembic upgrade head
```

## Run the app
From `C:\Users\User\Desktop\FastAPI`:

```bash
python -m uvicorn ToDoApp.main:app --reload
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

# Hospital Management APIs
Base path: `/hospital`

Core resources:
- Departments
- Doctors
- Patients
- Appointments
- Admissions
- Medications
- Prescriptions and prescription items
- Lab tests
- Invoices and invoice items
