import time
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str, email: str):
    return {
        "access_token": token,
        "time": 1200,
        "email": email
    }


def sign_jwt(userID: str):
    try:
        payload = {
            "userID": userID,
            "expiry": time.time() + 1200
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token_response(token, userID)
    except:
        return "error"


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}
