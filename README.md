# Patient Management System

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [File Descriptions](#file-descriptions)
- [Streamlit Application](#streamlit-application)
- [Database](#database)
- [Error Handling](#error-handling)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **Patient Management System** is a full-stack web application designed to manage patient records in a healthcare environment. It provides a modern interface using Streamlit for the frontend and FastAPI for the backend, with data persisted in a JSON file format.

This system allows healthcare professionals to:
- Create and manage patient records
- Search for patients by ID
- Update patient information
- Delete patient records
- View patient details in an intuitive dashboard

---

## ✨ Features

### Core Features
- ✅ **Create Patients** - Add new patient records with validation
- ✅ **Search Patients** - Find patients by their unique ID
- ✅ **Update Patients** - Modify existing patient information
- ✅ **Delete Patients** - Remove patient records from the system
- ✅ **Data Validation** - Pydantic models ensure data integrity
- ✅ **Duplicate Prevention** - System checks for duplicate patient IDs
- ✅ **Beautiful UI** - Modern, responsive Streamlit interface
- ✅ **REST API** - Complete REST API with FastAPI
- ✅ **Real-time Updates** - JSON-based storage with instant persistence

### Advanced Features
- 🎨 Custom CSS styling with gradient backgrounds
- 📊 Patient data visualization
- 🔍 Advanced search and filter capabilities
- 💾 Auto-save functionality
- 📱 Responsive design for mobile and desktop

---

## 🗂️ Project Structure

```
Fastapi/
├── main.py                 # FastAPI backend application
├── streamlit_app.py        # Streamlit frontend application
├── patient_data.json       # JSON database with patient records
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | FastAPI | ≥ 0.115 |
| Frontend Framework | Streamlit | ≥ 1.36 |
| Web Server | Uvicorn | ≥ 0.30 |
| Data Validation | Pydantic | ≥ 2.7 |
| Data Storage | JSON | Native |
| Language | Python | 3.9+ |

---

## 📦 Requirements

All required Python packages are listed in `requirements.txt`:

```
fastapi>=0.115
pydantic>=2.7
streamlit>=1.36
uvicorn>=0.30
```

**System Requirements:**
- Python 3.9 or higher
- Windows, macOS, or Linux
- Minimum 2GB RAM
- 100MB free disk space

---

## 🚀 Installation

### Step 1: Clone or Download the Project
```bash
cd Fastapi
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
pip list
```

You should see:
- fastapi
- pydantic
- streamlit
- uvicorn

---

## ⚙️ Configuration

### Environment Setup

No special configuration is required. The application uses default settings:

- **Backend Port:** `8000` (FastAPI default)
- **Streamlit Port:** `8501` (Streamlit default)
- **Data File:** `patient_data.json` (auto-created if missing)
- **Encoding:** UTF-8

### Custom Configuration

To change ports, modify the run commands (see [Running the Application](#running-the-application) section).

---

## 💡 Usage

### Starting the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Access the API documentation at: `http://127.0.0.1:8000/docs`

### Starting the Frontend (Streamlit)

In a new terminal window:

```bash
streamlit run streamlit_app.py
```

**Output:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

### Using the Application

1. **Open Streamlit UI** in your browser at `http://localhost:8501`
2. **Create Patients** - Use the form to add new patient records
3. **Search Patients** - Enter a patient ID to view details
4. **Update Records** - Modify existing patient information
5. **Delete Records** - Remove patients from the system

---

## 🔌 API Endpoints

All endpoints return JSON responses. Base URL: `http://127.0.0.1:8000`

### 1. Create Patient
**Endpoint:** `POST /create`

**Request Body:**
```json
{
  "id": 11,
  "name": "John Doe",
  "age": 40,
  "diagnosis": ["Hypertension", "Diabetes"],
  "admission_date": "2026-06-15"
}
```

**Response (Success):**
```json
{
  "message": "Patient created successfully"
}
```

**Response (Error - Duplicate ID):**
```json
{
  "detail": "Patient with this ID already exists"
}
```

**Status Code:** `200` (Success), `400` (Duplicate ID)

---

### 2. Search Patient
**Endpoint:** `GET /search/{patient_id}`

**Example:** `GET /search/1`

**Response (Found):**
```json
{
  "id": 1,
  "name": "Ali Khan",
  "age": 34,
  "gender": "Male",
  "diagnosis": "Hypertension",
  "admission_date": "2026-05-01"
}
```

**Response (Not Found):**
```json
{
  "detail": "Patient not found"
}
```

**Status Code:** `200` (Success), `404` (Not Found)

---

### 3. Update Patient
**Endpoint:** `PUT /update`

**Request Body (Partial Update - Only changed fields):**
```json
{
  "id": 1,
  "name": "Ali Khan Updated",
  "age": 35
}
```

**Response (Success):**
```json
{
  "message": "Patient updated successfully"
}
```

**Response (Not Found):**
```json
{
  "detail": "Patient not found"
}
```

**Status Code:** `200` (Success), `404` (Not Found)

---

### 4. Delete Patient
**Endpoint:** `DELETE /delete/{patient_id}`

**Example:** `DELETE /delete/1`

**Response (Success):**
```json
{
  "message": "Patient deleted successfully"
}
```

**Response (Not Found):**
```json
{
  "detail": "Patient not found"
}
```

**Status Code:** `200` (Success), `404` (Not Found)

---

## 📊 Data Models

### Patient Model (Create)
Used for creating new patients.

```python
class Patient(BaseModel):
    id: int              # Unique identifier (must be > 0)
    name: str            # Patient's full name
    age: int             # Patient's age (must be > 0)
    diagnosis: List[str] # List of diagnoses
    admission_date: date # Date of admission (YYYY-MM-DD format)
```

**Field Validations:**
- `id`: Must be positive integer, must be unique
- `name`: Required string
- `age`: Must be positive integer
- `diagnosis`: List of at least one diagnosis
- `admission_date`: Valid date in YYYY-MM-DD format

---

### Patient Update Model
Used for updating existing patients (all fields optional).

```python
class PatientUpdate(BaseModel):
    id: int                      # Required - Patient ID to update
    name: Optional[str] = None   # Optional - New name
    age: Optional[int] = None    # Optional - New age
    diagnosis: Optional[List[str]] = None  # Optional - New diagnoses
    admission_date: Optional[date] = None  # Optional - New admission date
```

---

### Patient Search Model
Used for searching patients.

```python
class PatientSearch(BaseModel):
    id: int  # Patient ID to search for (must be > 0)
```

---

## 📄 File Descriptions

### `main.py` - FastAPI Backend
**Purpose:** RESTful API server for patient data management

**Key Components:**
- `load_data()` - Reads patient data from JSON file
- `Patient` - Pydantic model for patient creation
- `PatientSearch` - Pydantic model for searching
- `PatientUpdate` - Pydantic model for updates
- `@app.post("/create")` - Create new patient endpoint
- `@app.get("/search/{patient_id}")` - Search patient endpoint
- `@app.put("/update")` - Update patient endpoint
- `@app.delete("/delete/{patient_id}")` - Delete patient endpoint

**File Size:** ~4 KB
**Lines of Code:** ~90

---

### `streamlit_app.py` - Streamlit Frontend
**Purpose:** User-friendly web interface for managing patient records

**Key Functions:**
- `load_patients()` - Load patient data from JSON
- `save_patients()` - Save patient data to JSON
- `normalize_diagnosis()` - Format diagnosis data
- `normalize_patient()` - Standardize patient record format
- `next_patient_id()` - Generate next available patient ID
- `find_patient()` - Search for patient in data
- `app_styles()` - Apply custom CSS styling

**Features:**
- Custom gradient background
- Responsive card layouts
- Interactive forms and buttons
- Real-time data updates
- Professional styling with backdrop blur effects

**File Size:** ~15 KB
**Lines of Code:** ~300+

---

### `patient_data.json` - Data Storage
**Purpose:** JSON database storing all patient records

**Structure:**
```json
[
  {
    "id": 1,
    "name": "Ali Khan",
    "age": 34,
    "gender": "Male",
    "diagnosis": "Hypertension",
    "admission_date": "2026-05-01"
  },
  {
    "id": 2,
    "name": "Sara Ahmed",
    "age": 28,
    "gender": "Female",
    "diagnosis": "Asthma",
    "admission_date": "2026-05-02"
  }
]
```

**Sample Data:** 10 patient records

---

### `requirements.txt` - Dependencies
**Purpose:** Lists all Python package dependencies

**Contents:**
```
fastapi>=0.115
pydantic>=2.7
streamlit>=1.36
uvicorn>=0.30
```

---

## 🎨 Streamlit Application

### User Interface Components

#### 1. **Header & Hero Section**
- Application title and description
- Custom gradient background with blur effects
- Professional styling

#### 2. **Patient Creation Form**
- Input fields for patient ID, name, age, gender
- Multi-select for diagnoses
- Date picker for admission date
- Submit button with validation

#### 3. **Search Functionality**
- Patient ID input field
- Real-time search results
- Detailed patient card display

#### 4. **Update Panel**
- Find patient by ID
- Edit individual fields
- Submit updates

#### 5. **Delete Section**
- Patient ID input for deletion
- Confirmation message
- Delete button

#### 6. **Patient List/Dashboard**
- Display all patient records
- Sortable table or card view
- Patient statistics and metrics

### Styling Features
- **Background:** Radial gradients with semi-transparent colors
- **Containers:** Padded blocks with rounded corners
- **Colors:** Professional blue and teal gradients
- **Shadows:** Box shadows for depth
- **Blur Effects:** Backdrop filter for modern look
- **Responsive:** Adapts to mobile and desktop

---

## 💾 Database

### Storage Method
- **Type:** JSON file-based database
- **Location:** `patient_data.json` in the project root
- **Format:** UTF-8 encoded JSON array

### Data Persistence
- Data is automatically saved after each operation:
  - Patient creation → File updated
  - Patient update → File updated
  - Patient deletion → File updated
  - Patient search → No file change

### Backup & Recovery
- **Manual Backup:** Copy `patient_data.json` to safe location
- **Auto-recovery:** Delete corrupted JSON to start fresh (data will be lost)
- **Best Practice:** Maintain regular backups

### Data Integrity
- Pydantic validation ensures data quality
- Duplicate ID prevention
- Date format validation
- Type checking for all fields

---

## ⚠️ Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | `patient_data.json` missing | Run create endpoint once to generate file |
| `JSONDecodeError` | Corrupted JSON file | Restore from backup or delete to reset |
| `400 - Duplicate ID` | Patient ID already exists | Use different ID |
| `404 - Not Found` | Patient ID doesn't exist | Verify patient ID |
| `Port already in use` | Port 8000/8501 occupied | Close app or use different port |
| `Module not found` | Missing dependencies | Run `pip install -r requirements.txt` |
| `Permission denied` | File access issue | Check file permissions |

### HTTP Status Codes

| Code | Meaning | Endpoint |
|------|---------|----------|
| 200 | Success | All successful operations |
| 400 | Bad Request | Duplicate patient ID |
| 404 | Not Found | Patient doesn't exist |
| 422 | Validation Error | Invalid data format |
| 500 | Server Error | Unexpected server error |

---

## ▶️ Running the Application

### Quick Start (Both Services)

**Terminal 1 - Start Backend:**
```bash
cd c:\Programs\Fastapi\Fastapi
uvicorn main:app --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd c:\Programs\Fastapi\Fastapi
streamlit run streamlit_app.py
```

**Terminal 3 (Optional) - Test API:**
```bash
# Get API documentation
curl http://127.0.0.1:8000/docs

# Test create patient
curl -X POST http://127.0.0.1:8000/create \
  -H "Content-Type: application/json" \
  -d '{
    "id": 11,
    "name": "Test User",
    "age": 30,
    "diagnosis": ["Test"],
    "admission_date": "2026-06-15"
  }'
```

### Custom Port Configuration

**Backend (Custom Port 9000):**
```bash
uvicorn main:app --port 9000 --reload
```

**Frontend (Custom Port 8502):**
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Production Deployment

```bash
# Without reload (production)
uvicorn main:app --host 0.0.0.0 --port 8000

# With Streamlit
streamlit run streamlit_app.py --logger.level=error
```

---

## 🤝 Contributing

### Guidelines
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** with clear messages (`git commit -m 'Add AmazingFeature'`)
6. **Push** to the branch (`git push origin feature/AmazingFeature`)
7. **Open** a Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Add docstrings to functions
- Include type hints
- Test new endpoints
- Update README for new features

---

## 📝 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute.

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Check existing issues
- Review API documentation: `http://127.0.0.1:8000/docs`
- Review code comments in source files

---

## 🎓 Learning Resources

### FastAPI
- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

### Streamlit
- [Streamlit Official Documentation](https://docs.streamlit.io/)
- [Streamlit Components Gallery](https://streamlit.io/components)

### Python
- [Python Official Documentation](https://docs.python.org/3/)
- [RESTful API Design Best Practices](https://restfulapi.net/)

---

## 📈 Future Enhancements

Potential features for future versions:
- [ ] Database migration from JSON to PostgreSQL
- [ ] User authentication and authorization
- [ ] Patient history tracking
- [ ] Email notifications
- [ ] Export reports (PDF/Excel)
- [ ] Advanced filtering and sorting
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Docker containerization
- [ ] Unit and integration tests
- [ ] CI/CD pipeline
- [ ] API versioning
- [ ] Swagger documentation enhancements

---

## ✅ Checklist for Getting Started

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `patient_data.json` exists in project root
- [ ] FastAPI backend running on port 8000
- [ ] Streamlit frontend running on port 8501
- [ ] Access Streamlit UI at `http://localhost:8501`
- [ ] Access API docs at `http://127.0.0.1:8000/docs`
- [ ] Test create, read, update, delete operations

---

**Last Updated:** June 15, 2026

**Version:** 1.0

**Author:** Your Organization

---

Thank you for using the Patient Management System! 🏥
