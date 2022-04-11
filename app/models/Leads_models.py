from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, DateTime, CheckConstraint
from app.configs.database import db
from sqlalchemy.orm import validates
import re

from app.excs.excs import ValidadePhoneError


@dataclass
class Leads(db.Model):
    __tablename__ = "leads_model"

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

    @validates("phone")
    def validade_phone(self, key, phone):
        validade = "^\([1-9]{2}\)(?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"
        print(phone)
        if not re.fullmatch(validade, phone):
            raise ValidadePhoneError(
                "Formato de telefone inválido. Exemplo de formato válido: (xx)xxxxx-xxxx"
            )

        return phone

