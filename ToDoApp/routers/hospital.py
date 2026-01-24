from datetime import date, datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .auth import get_current_user, require_roles
from ..models import (
    Admissions,
    Appointments,
    Departments,
    Doctors,
    InvoiceItems,
    Invoices,
    LabTests,
    Medications,
    Patients,
    PrescriptionItems,
    Prescriptions,
    Workers,
)

router = APIRouter(
    prefix="/hospital",
    tags=["hospital"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
admin_dependency = Annotated[dict, Depends(require_roles("admin"))]
admin_secretary_dependency = Annotated[dict, Depends(require_roles("admin", "secretary"))]
admin_doctor_dependency = Annotated[dict, Depends(require_roles("admin", "doctor"))]
staff_dependency = Annotated[dict, Depends(require_roles("admin", "doctor", "secretary"))]


def apply_updates(db_obj, data: dict) -> None:
    for key, value in data.items():
        setattr(db_obj, key, value)


class DepartmentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = None


class DepartmentOut(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    user_id: Optional[int] = None
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    phone: Optional[str] = None
    specialization: Optional[str] = None
    department_id: Optional[int] = None
    is_active: bool = True


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=3, max_length=100)
    phone: Optional[str] = None
    specialization: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None


class DoctorOut(DoctorBase):
    id: int

    class Config:
        from_attributes = True


class WorkerBase(BaseModel):
    user_id: Optional[int] = None
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    phone: Optional[str] = None
    role: str = Field(min_length=2, max_length=100)
    department_id: Optional[int] = None
    is_active: bool = True


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=3, max_length=100)
    phone: Optional[str] = None
    role: Optional[str] = Field(default=None, min_length=2, max_length=100)
    department_id: Optional[int] = None
    is_active: Optional[bool] = None


class WorkerOut(WorkerBase):
    id: int

    class Config:
        from_attributes = True


class PatientBase(BaseModel):
    user_id: Optional[int] = None
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    dob: date
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    user_id: Optional[int] = None
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    dob: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None


class PatientOut(PatientBase):
    id: int

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    reason: Optional[str] = None
    status: str = Field(default="scheduled", max_length=50)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = Field(default=None, max_length=50)


class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        from_attributes = True


class AdmissionBase(BaseModel):
    patient_id: int
    attending_doctor_id: int
    admitted_at: datetime
    discharged_at: Optional[datetime] = None
    room_number: Optional[str] = None
    diagnosis: Optional[str] = None


class AdmissionCreate(AdmissionBase):
    pass


class AdmissionUpdate(BaseModel):
    patient_id: Optional[int] = None
    attending_doctor_id: Optional[int] = None
    admitted_at: Optional[datetime] = None
    discharged_at: Optional[datetime] = None
    room_number: Optional[str] = None
    diagnosis: Optional[str] = None


class AdmissionOut(AdmissionBase):
    id: int

    class Config:
        from_attributes = True


class MedicationBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = None


class MedicationOut(MedicationBase):
    id: int

    class Config:
        from_attributes = True


class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    issued_at: datetime
    notes: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    issued_at: Optional[datetime] = None
    notes: Optional[str] = None


class PrescriptionOut(PrescriptionBase):
    id: int

    class Config:
        from_attributes = True


class PrescriptionItemBase(BaseModel):
    prescription_id: int
    medication_id: int
    dosage: str
    frequency: str
    duration_days: int = Field(gt=0)


class PrescriptionItemCreate(PrescriptionItemBase):
    pass


class PrescriptionItemUpdate(BaseModel):
    prescription_id: Optional[int] = None
    medication_id: Optional[int] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration_days: Optional[int] = Field(default=None, gt=0)


class PrescriptionItemOut(PrescriptionItemBase):
    id: int

    class Config:
        from_attributes = True


class LabTestBase(BaseModel):
    patient_id: int
    ordered_by_doctor_id: int
    test_name: str = Field(min_length=1, max_length=200)
    ordered_at: datetime
    result: Optional[str] = None
    status: str = Field(default="ordered", max_length=50)


class LabTestCreate(LabTestBase):
    pass


class LabTestUpdate(BaseModel):
    patient_id: Optional[int] = None
    ordered_by_doctor_id: Optional[int] = None
    test_name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    ordered_at: Optional[datetime] = None
    result: Optional[str] = None
    status: Optional[str] = Field(default=None, max_length=50)


class LabTestOut(LabTestBase):
    id: int

    class Config:
        from_attributes = True


class InvoiceBase(BaseModel):
    patient_id: int
    issued_at: datetime
    total_amount: float = Field(ge=0)
    status: str = Field(default="unpaid", max_length=50)


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    patient_id: Optional[int] = None
    issued_at: Optional[datetime] = None
    total_amount: Optional[float] = Field(default=None, ge=0)
    status: Optional[str] = Field(default=None, max_length=50)


class InvoiceOut(InvoiceBase):
    id: int

    class Config:
        from_attributes = True


class InvoiceItemBase(BaseModel):
    invoice_id: int
    description: str = Field(min_length=1, max_length=200)
    amount: float = Field(ge=0)


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemUpdate(BaseModel):
    invoice_id: Optional[int] = None
    description: Optional[str] = Field(default=None, min_length=1, max_length=200)
    amount: Optional[float] = Field(default=None, ge=0)


class InvoiceItemOut(InvoiceItemBase):
    id: int

    class Config:
        from_attributes = True


@router.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(payload: DepartmentCreate, db: db_dependency, user: admin_secretary_dependency):
    department = Departments(**payload.model_dump())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.get("/departments", response_model=list[DepartmentOut])
def list_departments(db: db_dependency, user: staff_dependency):
    return db.query(Departments).all()


@router.get("/departments/{department_id}", response_model=DepartmentOut)
def get_department(db: db_dependency, department_id: int = Path(gt=0), user: staff_dependency = None):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    return department


@router.put("/departments/{department_id}", response_model=DepartmentOut)
def update_department(
    payload: DepartmentUpdate,
    db: db_dependency,
    department_id: int = Path(gt=0),
    user: admin_secretary_dependency = None,
):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    apply_updates(department, payload.model_dump(exclude_unset=True))
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


@router.delete("/departments/{department_id}", status_code=204)
def delete_department(db: db_dependency, department_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    department = db.query(Departments).filter(Departments.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found.")
    db.delete(department)
    db.commit()


@router.post("/doctors", response_model=DoctorOut, status_code=201)
def create_doctor(payload: DoctorCreate, db: db_dependency, user: admin_secretary_dependency):
    doctor = Doctors(**payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("/doctors", response_model=list[DoctorOut])
def list_doctors(db: db_dependency, user: staff_dependency):
    return db.query(Doctors).all()


@router.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(db: db_dependency, doctor_id: int = Path(gt=0), user: staff_dependency = None):
    doctor = db.query(Doctors).filter(Doctors.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    return doctor


@router.put("/doctors/{doctor_id}", response_model=DoctorOut)
def update_doctor(payload: DoctorUpdate, db: db_dependency, doctor_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    doctor = db.query(Doctors).filter(Doctors.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    apply_updates(doctor, payload.model_dump(exclude_unset=True))
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/doctors/{doctor_id}", status_code=204)
def delete_doctor(db: db_dependency, doctor_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    doctor = db.query(Doctors).filter(Doctors.id == doctor_id).first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found.")
    db.delete(doctor)
    db.commit()


@router.post("/workers", response_model=WorkerOut, status_code=201)
def create_worker(payload: WorkerCreate, db: db_dependency, user: admin_secretary_dependency):
    worker = Workers(**payload.model_dump())
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


@router.get("/workers", response_model=list[WorkerOut])
def list_workers(db: db_dependency, user: admin_secretary_dependency):
    return db.query(Workers).all()


@router.get("/workers/{worker_id}", response_model=WorkerOut)
def get_worker(db: db_dependency, worker_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    worker = db.query(Workers).filter(Workers.id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found.")
    return worker


@router.put("/workers/{worker_id}", response_model=WorkerOut)
def update_worker(payload: WorkerUpdate, db: db_dependency, worker_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    worker = db.query(Workers).filter(Workers.id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found.")
    apply_updates(worker, payload.model_dump(exclude_unset=True))
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


@router.delete("/workers/{worker_id}", status_code=204)
def delete_worker(db: db_dependency, worker_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    worker = db.query(Workers).filter(Workers.id == worker_id).first()
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found.")
    db.delete(worker)
    db.commit()


@router.post("/patients", response_model=PatientOut, status_code=201)
def create_patient(payload: PatientCreate, db: db_dependency, user: admin_secretary_dependency):
    patient = Patients(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/patients", response_model=list[PatientOut])
def list_patients(db: db_dependency, user: staff_dependency):
    return db.query(Patients).all()


@router.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient(db: db_dependency, patient_id: int = Path(gt=0), user: staff_dependency = None):
    patient = db.query(Patients).filter(Patients.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    return patient


@router.put("/patients/{patient_id}", response_model=PatientOut)
def update_patient(payload: PatientUpdate, db: db_dependency, patient_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    patient = db.query(Patients).filter(Patients.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    apply_updates(patient, payload.model_dump(exclude_unset=True))
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/patients/{patient_id}", status_code=204)
def delete_patient(db: db_dependency, patient_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    patient = db.query(Patients).filter(Patients.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")
    db.delete(patient)
    db.commit()


@router.post("/appointments", response_model=AppointmentOut, status_code=201)
def create_appointment(payload: AppointmentCreate, db: db_dependency, user: staff_dependency):
    appointment = Appointments(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/appointments", response_model=list[AppointmentOut])
def list_appointments(db: db_dependency, user: staff_dependency):
    return db.query(Appointments).all()


@router.get("/appointments/{appointment_id}", response_model=AppointmentOut)
def get_appointment(db: db_dependency, appointment_id: int = Path(gt=0), user: staff_dependency = None):
    appointment = db.query(Appointments).filter(Appointments.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment


@router.put("/appointments/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    payload: AppointmentUpdate,
    db: db_dependency,
    appointment_id: int = Path(gt=0),
    user: staff_dependency = None,
):
    appointment = db.query(Appointments).filter(Appointments.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    apply_updates(appointment, payload.model_dump(exclude_unset=True))
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/appointments/{appointment_id}", status_code=204)
def delete_appointment(db: db_dependency, appointment_id: int = Path(gt=0), user: staff_dependency = None):
    appointment = db.query(Appointments).filter(Appointments.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    db.delete(appointment)
    db.commit()


@router.post("/admissions", response_model=AdmissionOut, status_code=201)
def create_admission(payload: AdmissionCreate, db: db_dependency, user: admin_doctor_dependency):
    admission = Admissions(**payload.model_dump())
    db.add(admission)
    db.commit()
    db.refresh(admission)
    return admission


@router.get("/admissions", response_model=list[AdmissionOut])
def list_admissions(db: db_dependency, user: staff_dependency):
    return db.query(Admissions).all()


@router.get("/admissions/{admission_id}", response_model=AdmissionOut)
def get_admission(db: db_dependency, admission_id: int = Path(gt=0), user: staff_dependency = None):
    admission = db.query(Admissions).filter(Admissions.id == admission_id).first()
    if admission is None:
        raise HTTPException(status_code=404, detail="Admission not found.")
    return admission


@router.put("/admissions/{admission_id}", response_model=AdmissionOut)
def update_admission(payload: AdmissionUpdate, db: db_dependency, admission_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    admission = db.query(Admissions).filter(Admissions.id == admission_id).first()
    if admission is None:
        raise HTTPException(status_code=404, detail="Admission not found.")
    apply_updates(admission, payload.model_dump(exclude_unset=True))
    db.add(admission)
    db.commit()
    db.refresh(admission)
    return admission


@router.delete("/admissions/{admission_id}", status_code=204)
def delete_admission(db: db_dependency, admission_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    admission = db.query(Admissions).filter(Admissions.id == admission_id).first()
    if admission is None:
        raise HTTPException(status_code=404, detail="Admission not found.")
    db.delete(admission)
    db.commit()


@router.post("/medications", response_model=MedicationOut, status_code=201)
def create_medication(payload: MedicationCreate, db: db_dependency, user: admin_doctor_dependency):
    medication = Medications(**payload.model_dump())
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


@router.get("/medications", response_model=list[MedicationOut])
def list_medications(db: db_dependency, user: staff_dependency):
    return db.query(Medications).all()


@router.get("/medications/{medication_id}", response_model=MedicationOut)
def get_medication(db: db_dependency, medication_id: int = Path(gt=0), user: staff_dependency = None):
    medication = db.query(Medications).filter(Medications.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found.")
    return medication


@router.put("/medications/{medication_id}", response_model=MedicationOut)
def update_medication(
    payload: MedicationUpdate,
    db: db_dependency,
    medication_id: int = Path(gt=0),
    user: admin_doctor_dependency = None,
):
    medication = db.query(Medications).filter(Medications.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found.")
    apply_updates(medication, payload.model_dump(exclude_unset=True))
    db.add(medication)
    db.commit()
    db.refresh(medication)
    return medication


@router.delete("/medications/{medication_id}", status_code=204)
def delete_medication(db: db_dependency, medication_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    medication = db.query(Medications).filter(Medications.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found.")
    db.delete(medication)
    db.commit()


@router.post("/prescriptions", response_model=PrescriptionOut, status_code=201)
def create_prescription(payload: PrescriptionCreate, db: db_dependency, user: admin_doctor_dependency):
    prescription = Prescriptions(**payload.model_dump())
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


@router.get("/prescriptions", response_model=list[PrescriptionOut])
def list_prescriptions(db: db_dependency, user: admin_doctor_dependency):
    return db.query(Prescriptions).all()


@router.get("/prescriptions/{prescription_id}", response_model=PrescriptionOut)
def get_prescription(db: db_dependency, prescription_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    prescription = db.query(Prescriptions).filter(Prescriptions.id == prescription_id).first()
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    return prescription


@router.put("/prescriptions/{prescription_id}", response_model=PrescriptionOut)
def update_prescription(
    payload: PrescriptionUpdate,
    db: db_dependency,
    prescription_id: int = Path(gt=0),
    user: admin_doctor_dependency = None,
):
    prescription = db.query(Prescriptions).filter(Prescriptions.id == prescription_id).first()
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    apply_updates(prescription, payload.model_dump(exclude_unset=True))
    db.add(prescription)
    db.commit()
    db.refresh(prescription)
    return prescription


@router.delete("/prescriptions/{prescription_id}", status_code=204)
def delete_prescription(db: db_dependency, prescription_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    prescription = db.query(Prescriptions).filter(Prescriptions.id == prescription_id).first()
    if prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found.")
    db.delete(prescription)
    db.commit()


@router.post("/prescription-items", response_model=PrescriptionItemOut, status_code=201)
def create_prescription_item(payload: PrescriptionItemCreate, db: db_dependency, user: admin_doctor_dependency):
    item = PrescriptionItems(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/prescription-items", response_model=list[PrescriptionItemOut])
def list_prescription_items(db: db_dependency, user: admin_doctor_dependency):
    return db.query(PrescriptionItems).all()


@router.get("/prescription-items/{item_id}", response_model=PrescriptionItemOut)
def get_prescription_item(db: db_dependency, item_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    item = db.query(PrescriptionItems).filter(PrescriptionItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Prescription item not found.")
    return item


@router.put("/prescription-items/{item_id}", response_model=PrescriptionItemOut)
def update_prescription_item(
    payload: PrescriptionItemUpdate,
    db: db_dependency,
    item_id: int = Path(gt=0),
    user: admin_doctor_dependency = None,
):
    item = db.query(PrescriptionItems).filter(PrescriptionItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Prescription item not found.")
    apply_updates(item, payload.model_dump(exclude_unset=True))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/prescription-items/{item_id}", status_code=204)
def delete_prescription_item(db: db_dependency, item_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    item = db.query(PrescriptionItems).filter(PrescriptionItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Prescription item not found.")
    db.delete(item)
    db.commit()


@router.post("/lab-tests", response_model=LabTestOut, status_code=201)
def create_lab_test(payload: LabTestCreate, db: db_dependency, user: admin_doctor_dependency):
    test = LabTests(**payload.model_dump())
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


@router.get("/lab-tests", response_model=list[LabTestOut])
def list_lab_tests(db: db_dependency, user: admin_doctor_dependency):
    return db.query(LabTests).all()


@router.get("/lab-tests/{test_id}", response_model=LabTestOut)
def get_lab_test(db: db_dependency, test_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    test = db.query(LabTests).filter(LabTests.id == test_id).first()
    if test is None:
        raise HTTPException(status_code=404, detail="Lab test not found.")
    return test


@router.put("/lab-tests/{test_id}", response_model=LabTestOut)
def update_lab_test(payload: LabTestUpdate, db: db_dependency, test_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    test = db.query(LabTests).filter(LabTests.id == test_id).first()
    if test is None:
        raise HTTPException(status_code=404, detail="Lab test not found.")
    apply_updates(test, payload.model_dump(exclude_unset=True))
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


@router.delete("/lab-tests/{test_id}", status_code=204)
def delete_lab_test(db: db_dependency, test_id: int = Path(gt=0), user: admin_doctor_dependency = None):
    test = db.query(LabTests).filter(LabTests.id == test_id).first()
    if test is None:
        raise HTTPException(status_code=404, detail="Lab test not found.")
    db.delete(test)
    db.commit()


@router.post("/invoices", response_model=InvoiceOut, status_code=201)
def create_invoice(payload: InvoiceCreate, db: db_dependency, user: admin_secretary_dependency):
    invoice = Invoices(**payload.model_dump())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/invoices", response_model=list[InvoiceOut])
def list_invoices(db: db_dependency, user: admin_secretary_dependency):
    return db.query(Invoices).all()


@router.get("/invoices/{invoice_id}", response_model=InvoiceOut)
def get_invoice(db: db_dependency, invoice_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    invoice = db.query(Invoices).filter(Invoices.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    return invoice


@router.put("/invoices/{invoice_id}", response_model=InvoiceOut)
def update_invoice(payload: InvoiceUpdate, db: db_dependency, invoice_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    invoice = db.query(Invoices).filter(Invoices.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    apply_updates(invoice, payload.model_dump(exclude_unset=True))
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.delete("/invoices/{invoice_id}", status_code=204)
def delete_invoice(db: db_dependency, invoice_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    invoice = db.query(Invoices).filter(Invoices.id == invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found.")
    db.delete(invoice)
    db.commit()


@router.post("/invoice-items", response_model=InvoiceItemOut, status_code=201)
def create_invoice_item(payload: InvoiceItemCreate, db: db_dependency, user: admin_secretary_dependency):
    item = InvoiceItems(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/invoice-items", response_model=list[InvoiceItemOut])
def list_invoice_items(db: db_dependency, user: admin_secretary_dependency):
    return db.query(InvoiceItems).all()


@router.get("/invoice-items/{item_id}", response_model=InvoiceItemOut)
def get_invoice_item(db: db_dependency, item_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    item = db.query(InvoiceItems).filter(InvoiceItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Invoice item not found.")
    return item


@router.put("/invoice-items/{item_id}", response_model=InvoiceItemOut)
def update_invoice_item(payload: InvoiceItemUpdate, db: db_dependency, item_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    item = db.query(InvoiceItems).filter(InvoiceItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Invoice item not found.")
    apply_updates(item, payload.model_dump(exclude_unset=True))
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/invoice-items/{item_id}", status_code=204)
def delete_invoice_item(db: db_dependency, item_id: int = Path(gt=0), user: admin_secretary_dependency = None):
    item = db.query(InvoiceItems).filter(InvoiceItems.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Invoice item not found.")
    db.delete(item)
    db.commit()
