from http import HTTPStatus

from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail=detail)
