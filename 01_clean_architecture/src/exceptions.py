from fastapi import HTTPException

class TodoError(HTTPException):
    pass

class TodoNotFoundError()