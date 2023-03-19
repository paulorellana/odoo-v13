import logging
import requests
import urllib.parse
import json
import base64
import hashlib
from odoo.exceptions import UserError, ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)



url_token_fomat = "https://api-seguridad.sunat.gob.pe/v1/clientessol/{client_id}/oauth2/token/"
url_api_gre_format = "https://api-cpe.sunat.gob.pe/v1/contribuyente/gem/comprobantes/{numRucEmisor}-{codCpe}-{numSerie}-{numCpe}"
url_search_api_gre_format = "https://api-cpe.sunat.gob.pe/v1/contribuyente/gem/comprobantes/envios/{ticket}"

def generate_access_token(gre):
    gre_data = json.loads(gre.current_log_status_id.request_json)

    #Obtención de Token
    grant_type = "password"
    scope = "https://api-cpe.sunat.gob.pe"

    ICPSudo = request.env["ir.config_parameter"].sudo()
    client_id = ICPSudo.get_param("gre.client_id",default="")
    client_secret = ICPSudo.get_param("gre.client_secret",default="")
    
    if not client_id or not client_secret:
        raise UserError("El parámetro client_id o client_secrete para el envío de guías de remisión electrónica no esta configurado")

    url = url_token_fomat.format(client_id = client_id)

    ruc = gre_data["company"]["numDocEmisor"]
    sunat_user = gre_data["company"]["SUNAT_user"]
    sunat_password = gre_data["company"]["SUNAT_pass"]
    username = "{}{}".format(ruc,sunat_user)
    password = sunat_password

    if not ruc or not sunat_user or not sunat_password:
        raise UserError("El RUC,usuario y contraseña de SUNAT no se encuentra configurado.")

    payload_data = {
        "grant_type":grant_type,
        "scope":scope,
        "client_id":client_id,
        "client_secret":client_secret,
        "username":username,
        "password":password
    }
    payload = urllib.parse.urlencode(payload_data)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()

    access_token = ""
    if response.status_code == 200:
        access_token =  res.get("access_token","")
    else:
        msg = res.get("msg") + "\n"
        errors = "\n".join(list(map(lambda r:"[{}] - {}".format(r.get("codError"),r.get("desError")),res.get("errors"))))
        msg += errors
        raise UserError(msg)

    return access_token


def send_gre_api(gre):
    #Envio de Guia de remision remitente
    gre_data = json.loads(gre.current_log_status_id.request_json)
    ruc = gre_data["company"]["numDocEmisor"]
    access_token = generate_access_token(gre)

    
    numRucEmisor = ruc
    codCpe = "09"
    numSerie =  gre_data["documento"]["serie"]
    numCpe =  gre_data["documento"]["correlativo"]

    url = url_api_gre_format.format(numRucEmisor=numRucEmisor,codCpe=codCpe,numSerie=numSerie,numCpe=numCpe)
    headers = {
        "Authorization":"Bearer {}".format(access_token),
        "Content-Type":"Application/json"
    }
    h = hashlib.new('sha256')
    h.update(base64.b64decode(gre.current_log_status_id.zip_file))    

    payload_data = {
        "archivo":{
            "nomArchivo":"{numRucEmisor}-{codCpe}-{numSerie}-{numCpe}.zip".format(numRucEmisor=numRucEmisor,codCpe=codCpe,numSerie=numSerie,numCpe=numCpe),
            "arcGreZip": gre.current_log_status_id.zip_file.decode('utf-8'),
            "hashZip":h.hexdigest()
        }
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_data))
    res = response.json()

    try:
        if response.status_code != 200:
            msg = ""
            if "msg" in res:
                msg = res.get("msg") + "\n"
            if "errores" in res:
                errors = "\n".join(list(map(lambda r:"[{}] - {}".format(r.get("codError"),r.get("desError")),res.get("errors"))))
                msg += errors
            raise UserError(msg)
    except Exception as e:
        raise UserError(response.text)

    return {
        "gre_ticket":res.get("numTicket",""),
        "gre_reception_date":res.get("fecRecepcion","").replace("T"," "),
        "status":"E"
    }


def search_ticket_gre_api(gre,gre_ticket):
    # gre_data = json.loads(gre.current_log_status_id.request_json)
    # ruc = gre_data["company"]["numDocEmisor"]
    access_token = generate_access_token(gre)

    url = url_search_api_gre_format.format(ticket=gre_ticket)
    headers = {
        "Authorization":"Bearer {}".format(access_token),
    }

    response = requests.request("GET", url, headers=headers)
    res = response.json()
    
    if "error" in res:
        if res.get("codRespuesta") == "99":
            msg_error = "{} {}".format(res["error"]["numError"],res["error"]["desError"])
            raise UserError(msg_error)
    
    if res.get("codRespuesta") == "0":
        return {"response_json":json.dumps(res,indent=4),"status":"A","cdr_file":res.get("arcCdr","")}

    return {"response_json":json.dumps(res,indent=4)}