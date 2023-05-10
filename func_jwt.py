from jwt import encode, decode
from jwt import exceptions
from os import getenv
import datetime
from flask import jsonify


def write_token(data: dict):
    payload = {**data, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)}
    token = encode(payload=payload, key=getenv("SECRET"), algorithm="HS256")
    return token.encode("UTF-8")


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

