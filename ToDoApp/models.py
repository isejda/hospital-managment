from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Float, Text


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phoneNumber = Column(String)

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id'))


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    location = Column(String)


class Doctors(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    specialization = Column(String)
    department_id = Column(Integer, ForeignKey('departments.id'))
    is_active = Column(Boolean, default=True)


class Patients(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    dob = Column(Date)
    gender = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    address = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)


class Appointments(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    scheduled_at = Column(DateTime)
    reason = Column(Text)
    status = Column(String, default="scheduled")


class Admissions(Base):
    __tablename__ = 'admissions'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    attending_doctor_id = Column(Integer, ForeignKey('doctors.id'))
    admitted_at = Column(DateTime)
    discharged_at = Column(DateTime, nullable=True)
    room_number = Column(String)
    diagnosis = Column(Text)


class Medications(Base):
    __tablename__ = 'medications'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)


class Prescriptions(Base):
    __tablename__ = 'prescriptions'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    issued_at = Column(DateTime)
    notes = Column(Text)


class PrescriptionItems(Base):
    __tablename__ = 'prescription_items'

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey('prescriptions.id'))
    medication_id = Column(Integer, ForeignKey('medications.id'))
    dosage = Column(String)
    frequency = Column(String)
    duration_days = Column(Integer)


class LabTests(Base):
    __tablename__ = 'lab_tests'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    ordered_by_doctor_id = Column(Integer, ForeignKey('doctors.id'))
    test_name = Column(String, index=True)
    ordered_at = Column(DateTime)
    result = Column(Text)
    status = Column(String, default="ordered")


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    issued_at = Column(DateTime)
    total_amount = Column(Float)
    status = Column(String, default="unpaid")


class InvoiceItems(Base):
    __tablename__ = 'invoice_items'

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    description = Column(String)
    amount = Column(Float)
