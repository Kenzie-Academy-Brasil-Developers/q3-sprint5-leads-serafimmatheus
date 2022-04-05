from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, DateTime, CheckConstraint
from app.configs.database import db


@dataclass
class Leads(db.Model):
    __tablename__ = "leads_model"
    __table_args__ = (CheckConstraint("phone ~ '([0-9]{2})([0-9]{4,5})([0-9]{4})'"),)

    id: int
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    email = Column(String(), unique=True, nullable=False)
    phone = Column(String(), unique=True, nullable=False)
    creation_date = Column(DateTime)
    last_visit = Column(DateTime)
    visits = Column(Integer, default=1)
