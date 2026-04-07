
from .auth import *
from .pets import *
from .users import *
from .handler import *


__all__ = [

    # User
    "UserNotFoundException",
    "UsernameAlreadyExistsException",
    "PhoneAlreadyExistsException",
    "CannotDeleteSelfException",

    # Pet
    "PetNotFoundException",
    "OwnerNotFoundException",
    "PetAlreadyExistsException",   

    # Auth
    "InvalidCredentialsException",
    "TokenInvalidException",
    "TokenExpiredException",
    "CodeRequiredException",
    "CodeInvalidException",
    "CodeExpiredException",
    "CodeSendTooFrequentlyException",
    "PhoneNotRegisteredException",
    "PhoneNotVerifiedException",
    "OldPasswordIncorrectException",


    # Handler
    "app_base_exception_handler", 
    "http_exception_handler",
    "validation_exception_handler",
    "sqlalchemy_exception_handler",
    "generic_exception_handler"
]
