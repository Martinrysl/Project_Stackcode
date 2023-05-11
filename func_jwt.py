from jwt import encode, decode
from jwt import exceptions
from os import getenv
import datetime
from flask import jsonify


# Funcion para escribir el token
def write_token(data: dict): # Recibe el data de tipo diccionario
    # Se modifica el payload para que el tiempo de expiracion sea de 1 minuto
    # **data funciona como el Script Operator ' ...data ' de JavaScript
    payload = {**data, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}
    # Se crea la variable de token usando el payload, la secret key y el algoritmo HS245 del JWT
    token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
    # Se regresa el token en encoding UTF-8
    return token.encode("UTF-8")


# Funcion para validar el Token
def auth_token(token, output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])

    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response

