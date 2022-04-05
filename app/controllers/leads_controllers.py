from http import HTTPStatus
from flask import current_app, jsonify, request
from datetime import datetime
from app.models.Leads_models import Leads
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
import re


def create_leads():
    data = request.get_json()

    try:
        if re.fullmatch("^\([1-9]{2}\)(?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$", data["phone"]):
            data["phone"] = data["phone"]
        else:
            data["phone"] = None
            return {"error": "Invalid number ex: (xx)xxxxx-xxxx"}, HTTPStatus.CONFLICT

        new_data = {
            "name": data["name"].title(),
            "email": data["email"].lower(),
            "phone": data["phone"],
            "creation_date": datetime.today(),
            "last_visit": datetime.today(),
        }

        lead = Leads(**new_data)

        current_app.db.session.add(lead)
        current_app.db.session.commit()

        return {
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        },HTTPStatus.CREATED

    except IntegrityError as e:
        return {"error": "email/phone alredy exists"}, HTTPStatus.CONFLICT
    except KeyError as e:
        return {"error": f"{e}"}, HTTPStatus.CONFLICT
    except TypeError as e:
        return {"error": f"{e}"}, HTTPStatus.CONFLICT
    except AttributeError as e:
        return {"error": f"keys other than strings"}, HTTPStatus.CONFLICT

def get_all_leads():
    lead = (
        Leads
        .query
        .order_by((Leads.visits.desc()))
        .all()
        
    )

    serializer = [
        {
            "name": leads.name,
            "email": leads.email,
            "phone": leads.phone,
            "creation_date": leads.creation_date,
            "last_visit": leads.last_visit,
            "visits": leads.visits
        } for leads in lead
    ]

    return jsonify(serializer), HTTPStatus.OK

def get_one_leads(id):
    
    try:
        lead = (
            Leads
            .query
            .get_or_404(id)
        )

        return {
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        },HTTPStatus.OK
    except NotFound:
        return {"error": f"id {id} not found"}, HTTPStatus.NOT_FOUND



def atualizando_leads():

    data = request.get_json()

    try:
        if data.get("email"):
            email = str(data["email"])
        else:
            return {"error": "just pass the key email"}, HTTPStatus.CONFLICT
        
        lead = (
            Leads
            .query
            .filter_by(email=email)
            .first()
        )

        new_lead = {
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": datetime.today(),
            "visits": lead.visits + 1
        }

        for key, value in new_lead.items():
            setattr(lead, key, value)

        current_app.db.session.add(lead)
        current_app.db.session.commit()

        return {
            "name": lead.name,
            "email": lead.email,
            "phone": lead.phone,
            "creation_date": lead.creation_date,
            "last_visit": lead.last_visit,
            "visits": lead.visits
        },HTTPStatus.OK
    except:
        return {"error": f"{email} not found!"}, HTTPStatus.NOT_FOUND



def delete_lead():
    data = request.get_json()
    try:
        if data.get("email"):
            email = str(data["email"])
        else:
            return {"error": "just pass the key email"}, HTTPStatus.CONFLICT

        lead = (
            Leads
            .query
            .filter_by(email=email)
            .first()
        )

        current_app.db.session.delete(lead)
        current_app.db.session.commit()

        return "", HTTPStatus.NO_CONTENT
    except:
        return {"error": f"email {email} not found"}, HTTPStatus.NOT_FOUND
    