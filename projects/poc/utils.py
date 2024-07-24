import requests
import json

base_url = "https://api-stg.oppna.dev"

def get_aggregated(name: str, nik: str, phone: str, address: str, email: str, city: str, district: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": name,
        "nik": nik,
        "phone": phone,
        "address": address,
        "email": email,
        "city": city,
        "district": district
    })
    ses = requests.session()
    try:
        resp = ses.post(f"{base_url}/v1/guardians/aggregated", headers=headers, data=data)
        response = resp.json()
        return response
    except Exception as e:
        return {"data": None}

def get_detailed(name: str, nik: str, phone: str, address: str, email: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": name,
        "nik": nik,
        "phone": phone,
        "address": address,
        "email": email,
        "city": "abc",
        "district": "bcsa"
    })
    ses = requests.session()
    try:
        resp = ses.post(f"{base_url}/v1/guardians/detailed", headers=headers, data=data)
        response = resp.json()
        return response
    except Exception as e:
        return {}
    
def get_detailed_retrieve_phone(name: str, phone: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "name": name,
        "nik": "-",
        "phone": phone,
        "address": "-",
        "email": "-",
        "city": "abc",
        "district": "bcsa"
    })
    ses = requests.session()
    try:
        resp = ses.post(f"{base_url}/v1/guardians/retrieve", headers=headers, data=data)
        response = resp.json()
        return response
    except Exception as e:
        return {}
    
def get_opas_by_address(address_id: str) -> dict:
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "address_id": address_id
    })
    ses = requests.session()
    try:
        resp = ses.post(f"{base_url}/v1/guardians/address/opas", headers=headers, data=data)
        response = resp.json()
        return response
    except Exception as e:
        return {}
    
def masking_static(x: str) -> str:
    if len(x) > 2:
        x = "".join([k if ind < 2 else "*" for ind, k in enumerate(x)])
    return x
    
def masking_name(name: str) -> str:
    name = name.split()
    name = [masking_static(x) for x in name]
    return " ".join(name)
    
def transform_state_court(data: list) -> list:
    data_list = []
    for dat in data:
        case = dat["case_classification"]
        location = dat["location"]
        role = dat["role"]
        for date, url in zip(dat["registration_date"], dat["url"]):
            data_list.append({"case": case, "location": location, "role": role, "date": date, "url": url})
    return data_list

def transform_addresses(data: list) -> list:
    data = [{k:l for k,l in x.items() if k not in ["address_id", "completeness_level", "address_quality_score"]} for x in data]
    return data
