from functools import wraps
from flask import jsonify

from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from .services import Services

class ValidateProfile:
    
    def __init__(self):
        self.services = Services()
    
    def candidato_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                services = Services()
                try:
                    verify_jwt_in_request()
                except ValueError as err:
                    return {"message": "No se encuentro token en la solicitud", "status": "error"}, 403
                claims = get_jwt()
                if services.salifyHash("CANDIDATO", claims["sub"]) == claims["profile"]:
                    return fn(*args, **kwargs)
                else:
                    return {"message": "No tiene permiso para acceder al recurso solicitado", "status": "error"}, 403

            return decorator

        return wrapper
    
    def empresa_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                services = Services()
                try:
                    verify_jwt_in_request()
                except ValueError as err:
                    return {"message": "No se encuentro token en la solicitud", "status": "error"}, 403
                claims = get_jwt()
                
                if services.salifyHash("EMPRESA", claims["sub"]) == claims["profile"]:
                    return fn(*args, **kwargs)
                else:
                    return {"message": "No tiene permiso para acceder al recurso solicitado", "status": "error"}, 403

            return decorator

        return wrapper
    
    def abcjobs_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                services = Services()
                try:
                    verify_jwt_in_request()
                except ValueError as err:
                    return {"message": "No se encuentro token en la solicitud", "status": "error"}, 403
                claims = get_jwt()
                if services.salifyHash("FUNCIONARIOABCJOBS", claims["sub"]) == claims["profile"]:
                    return fn(*args, **kwargs)
                else:
                    return {"mensaje": "No tiene permiso para acceder al recurso solicitado", "status": "error"}, 403

            return decorator

        return wrapper