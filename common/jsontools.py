from fastapi import status
from fastapi.responses import JSONResponse, Response  
from typing import Union


def response(code: int, message: str, data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )