## This code defines a FastAPI application that allows users to create new patient records.
#  It includes a function to load existing patient data from a JSON file, a Pydantic model to validate incoming patient data, and an endpoint to handle the creation of new patients. 
# The endpoint checks for duplicate patient IDs before adding the new patient to the data and saving it back to the JSON file.
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Annotated, Optional,List
from datetime import date
import json
app = FastAPI()
def load_data():
    with open ("patient_data.json","r") as f:
        data = json.load(f)
    return data
class Patient(BaseModel):
    id: Annotated[int,Field(..., gt=0, description="The ID of the patient")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    age: Annotated[int, Field(..., gt=0, description="The age of the patient")]
    diagnosis: Annotated[List[str], Field(..., description="The diagnosis of the patient")]
    admission_date: Annotated[date, Field(..., description="The admission date of the patient")]

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    for p in data:
        if p["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data.append(patient.dict())
    with open("patient_data.json", "w") as f:
        json.dump(data, f)
    return {"message": "Patient created successfully"}
#Search for a patient by ID
#path is /search and it accepts a POST request with a JSON body containing the patient ID to search for.
class PatientSearch(BaseModel):
    id:Annotated[int, Field(..., gt=0, description="The ID of the patient to search for")]
@app.get("/search/{patient_id}")
def search_patient(patient_id: int = Path(..., gt=0, description="The ID of the patient to search for")):
    data = load_data()
    for p in data:
        if p["id"] == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")

### Update patient information
class PatientUpdate(BaseModel):
    id: Annotated[int, Field(..., gt=0, description="The ID of the patient to update")]
    name: Optional[str] = None
    age: Optional[int] = None
    diagnosis: Optional[List[str]] = None
    admission_date: Optional[date] = None

@app.put("/update")
def update_patient(patient: PatientUpdate):
    data = load_data()
    for p in data:
        if p["id"] == patient.id:
            if patient.name is not None:
                p["name"] = patient.name
            if patient.age is not None:
                p["age"] = patient.age
            if patient.diagnosis is not None:
                p["diagnosis"] = patient.diagnosis
            if patient.admission_date is not None:
                p["admission_date"] = str(patient.admission_date)
            with open("patient_data.json", "w") as f:
                json.dump(data, f)
            return {"message": "Patient updated successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")
##Delete a patient
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: int = Path(..., gt=0, description="The ID of the patient to delete")):
    data = load_data()
    for i, p in enumerate(data):
        if p["id"] == patient_id:
            del data[i]
            with open("patient_data.json", "w") as f:
                json.dump(data, f)
            return {"message": "Patient deleted successfully"}
    raise HTTPException(status_code=404, detail="Patient not found")
    